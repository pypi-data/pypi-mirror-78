
import os
import pytorch_lightning as pl
from iatorch.audio.utils import make_labels, join_labels, split_labels, encode_labels, AudioDataset
# from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader

########################
# AudioDataModule
########################
class AudioDataModule(pl.LightningDataModule):

    def __init__(self, data_dir, labels=None, resplit=True, transforms=None, batch_size=32, shuffle=True, num_workers=None):
        super().__init__()
        
        # Make labels
        labels = join_labels(data_dir, labels) if labels else make_labels(data_dir)
        
        # Split labels
        if resplit or ('split' not in labels.columns):
            split = {'train': 0.7, 'val': 0.15, 'test': 0.15}
            labels = split_labels(labels, split, stratify=True, verbose=False)
        
        # Encode labels
        self.labels, self.encoder, self.decoder = encode_labels(labels, verbose=False)

        # Parameters
        self.num_classes = len(self.encoder)
        self.transforms = transforms
        self.eval_transforms = transforms.copy()
        self.eval_transforms.update({'augments': None})
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.num_workers = num_workers if num_workers else os.cpu_count()//2

    def setup(self, stage):
        eval_transforms = self.transforms
        
        if stage == 'fit' or stage is None:
            # dataset for fit
            self.train_dataset = AudioDataset(self.labels[self.labels['split']=='train'], transforms=self.transforms)
            self.val_dataset = AudioDataset(self.labels[self.labels['split']=='val'], transforms=self.eval_transforms)
        if stage == 'test' or stage is None:
            self.test_dataset = AudioDataset(self.labels[self.labels['split']=='test'], transforms=self.eval_transforms)

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=self.shuffle, num_workers=self.num_workers)

    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size, num_workers=self.num_workers)

    def test_dataloader(self):
        return DataLoader(self.test_dataset, batch_size=self.batch_size, num_workers=self.num_workers)
