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
    
    def __init__(self, labels, load_func=librosa.load, sr=None, transforms=None, dtypes=(torch.float32, torch.int64)):
        self.filename = labels.filename.tolist()
        self.filepath = labels.filepath.tolist()
        self.label = labels.label.tolist()
        self.load_func = load_func
        self.sr = sr
        self.transforms = transforms
        self.data_dtype, self.target_dtype = dtypes
    
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
            x = self.transforms(y, sr)
        else:
            x = y
        
        #### CHANGE DTYPE ####
        data = torch.tensor(x.transpose(2, 0, 1), dtype=self.data_dtype)
        target = torch.tensor(label, dtype=self.target_dtype)
        
        return data, target, filename
