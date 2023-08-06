
import os, librosa, cv2
from functools import partial
import pytorch_lightning as pl
from iatorch.audio.utils import encode_labels, AudioDataset
from torch.utils.data import DataLoader

########################
# AudioDataModule
########################
class AudioDataModule(pl.LightningDataModule):

    def __init__(self, labels, load_func=librosa.load, transforms=None, batch_size=32, shuffle=True, num_workers=None):
        super().__init__()
        
        # Encode labels
        self.labels, self.encoder, self.decoder = encode_labels(labels, verbose=False)
        
        # File load function
        self.load_func = load_func

        # Parameters
        self.num_classes = len(self.encoder)
        self.transforms = partial(transforms, augment=True)
        self.eval_transforms = partial(transforms, augment=False)
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.num_workers = num_workers if num_workers else os.cpu_count()//2

    def setup(self, stage):
        
        if stage == 'fit' or stage is None:
            # dataset for fit
            self.train_dataset = AudioDataset(self.labels[self.labels['split']=='train'], self.load_func, transforms=self.transforms)
            self.val_dataset = AudioDataset(self.labels[self.labels['split']=='val'], self.load_func, transforms=self.eval_transforms)

        if stage == 'test' or stage is None:
            self.test_dataset = AudioDataset(self.labels[self.labels['split']=='test'], self.load_func, transforms=self.eval_transforms)

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=self.shuffle, num_workers=self.num_workers)

    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size, num_workers=self.num_workers)

    def test_dataloader(self):
        return DataLoader(self.test_dataset, batch_size=self.batch_size, num_workers=self.num_workers)
