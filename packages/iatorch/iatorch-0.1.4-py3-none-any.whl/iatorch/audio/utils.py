import os, textwrap
from pathlib import Path
import dask
import pandas as pd
import numpy as np
from torch.utils.data import Dataset
import torch, librosa, cv2
from nptdms import TdmsFile


################################################################
# make labels inferred from subdirs
################################################################
def make_labels(filepath, exts=["wav", "tdms"], use_dask=False):
    subdirs = [Path(d) for d in os.scandir(filepath) if os.path.isdir(d)]

    if use_dask:
        @dask.delayed
        def search(path, ext):
            return list(path.glob(f"*.{ext.lstrip('.')}"))      
        @dask.delayed
        def merge(lst):
            files = []
            for e in lst:
                files.extend(e)
            return files
        files = []
        for subdir in subdirs:
            for ext in exts:
                files.append(search(subdir, ext))
        files = merge(files).compute()
        
    else:
        files = []
        for subdir in subdirs:
            for ext in exts:
                files.extend(subdir.glob(f"**/*.{ext.lstrip('.')}"))
        
    labels = pd.DataFrame({
        'filename': [f.name for f in files],
        'filepath': [str(f) for f in files],
        'label': [f.parent.name for f in files]
    })
    
    return labels


################################################################
# prep labels
################################################################
def prep_labels(datadir, labels=None, split={'train': 0.6, 'val': 0.2, 'test': 0.2}, exts=["wav", "tdms"], use_dask=False, min_sample=1, random_state=777, verbose=True):
    
    path = labels
    
    # labels inferred from subdirs
    labels = make_labels(datadir, exts=exts, use_dask=use_dask)
    
    # replace label column if labels.csv is given
    if path:
        labels_from_path = pd.read_csv(path) 
        if 'filename' not in labels_from_path.columns:
            labels_from_path['filename'] = [f.rsplit('/', 1)[-1] for f in labels_from_path['filepath']]
        labels = pd.merge(labels.drop(columns='label'), labels_from_path[['filename', 'label']], "inner", "filename")
        
    # split labels
    if 'split' not in labels.columns:
        labs = sorted(labels['label'].unique())
        sorted_split = {k: v for k, v in sorted(split.items(), key=lambda item: item[1])}
        dfs = []
        for lab in labs:
            dfLab = labels[labels['label']==lab]
            denom = 1
            for i, (split_key, split_ratio) in enumerate(sorted_split.items()):
                n_remains = len(dfLab)
                n = min(n_remains, max(round(n_remains* split_ratio/denom), min_sample))
                dfSplit = dfLab.sample(n=n, random_state=random_state)
                dfSplit['split'] = split_key
                dfs.append(dfSplit)
                dfLab = dfLab.drop(dfSplit.index)
                denom = denom - split_ratio
        labels = pd.concat(dfs)
    
    if verbose:
        print(f'<DATA> {datadir}')
        print(labels.pivot_table('filepath', 'label', 'split', aggfunc='count')[split.keys()].to_markdown())
        print('')
    
    return labels.sort_index()


################################################################
# encode labels
################################################################
def encode_labels(labels, reverse=False, verbose=True):
    names = sorted(labels['label'].unique(), reverse=reverse)
    encoder = {name: code for code, name in enumerate(names)}
    decoder = {code: name for code, name in enumerate(names)}
    labels['label'] = [encoder[x] for x in labels['label']]
    
    if verbose:
        print(f'<LABELS> {len(names)} classes')
        print(f'encoder = {encoder}')
        print(f'decoder = {decoder}')
        print('')
        
    return labels, encoder, decoder


################################################################
# load_tmds
################################################################
def load_tdms(filepath, sr_new=None, channel='CPsignal1'):
    try:
        ch = TdmsFile(filepath).groups()[0][channel]
        y = ch[:]
        sr = 1//ch.properties['dt']
    except Exception as ex:
        print('ERROR!!! {ex}')
        return None, None
    return y, sr


################################################################
# make_confusion_matrix
################################################################
def make_confusion_matrix(truth, predict):
    cm = pd.crosstab(truth, predict)
    for l in cm.index:
        if l not in cm.columns:
            cm[l] = 0
    return cm[cm.index]

        
################################################################
#### AudioDataset (DEFAULT)
################################################################
class AudioDataset(Dataset):
    
    def __init__(self, labels, load_func=librosa.load, sr=None, transforms=None, dtypes=(torch.FloatTensor, np.int64), np_order='hwc'):
        self.filename = labels.filename.tolist()
        self.filepath = labels.filepath.tolist()
        self.label = labels.label.tolist()
        self.load_func = load_func
        self.sr = sr
        self.transforms = transforms
        self.np_order = np_order.lower()
        self.dtypes = dtypes
    
    def __len__(self):
        return len(self.label)
    
    def __getitem__(self, idx):
        #### GET INDEX ####
        idx = idx.tolist() if torch.is_tensor(idx) else idx
        filename = self.filename[idx]
        filepath = self.filepath[idx]
        label = self.label[idx]
        
        #### LOAD DATA ####
        y, sr = self.load_func(filepath, self.sr)
                
        #### TRANSFORM DATA ####
        if self.transforms:
            
            if not all(self.transforms[ch] is None for ch in ['r', 'g', 'b']):
                x = []
                for ch in ['r', 'g', 'b']:
                    if self.transforms[ch]:
                        ch_transforms = self.transforms[ch]
                        ch_transforms = ch_transforms if type(ch_transforms) is list else [ch_transforms]
                        for transform in ch_transforms:
                            y, _ = transform(y, sr)
                    x.append(y)
                x = np.stack(x, axis=self.np_order.index('c'))
                
            if 'resize' in self.transforms.keys():
                if self.transforms['resize']:
                    transforms = self.transforms['resize']
                    transforms = transforms if type(transforms) is list else [transforms]
                    np_order = self.np_order
                    for transform in transforms:
                        x, np_order = transform(x, np_order)
                        
            if 'augment' in self.transforms.keys():
                if self.transforms['augment']:
                    transforms = self.transforms['augment']
                    transforms = transforms if type(transforms) is list else [transforms]
                    np_order = self.np_order
                    for transform in transforms:
                        x, np_order = transform(x, np_order)
        
            #### To Tensor
            dtype_data, dtype_target = self.dtypes
            if np_order == 'chw':
                x = x
            elif np_order == 'hwc':
                x = np.transpose(x, (2, 0, 1))
            else:
                print("np_order options are 'chw' and 'hwc'")
            data = dtype_data(x)
            target = dtype_target(label)
        
        else:
            data = (y, sr)
            target = label
        
        return data, target, filename    
