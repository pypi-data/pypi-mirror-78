
import os, time
from functools import partial
import pytorch_lightning as pl
import torchvision.models as models
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from pytorch_lightning.metrics import functional as FM
import mlflow.pytorch

class TransferModel(pl.LightningModule):

    def __init__(self, num_classes, batch_size=None, precision=None, base_model=models.mobilenet_v2(True), optimizer=optim.Adam, criterion=F.cross_entropy):
        super().__init__()
        
        # Model
        self.base_model = base_model
        self.num_classes = num_classes
        self.classifier = nn.Linear(base_model.classifier[-1].state_dict()['weight'].shape[0], self.num_classes)
        
        # Optimizer
        self.optimizer = optimizer
        self.criterion = criterion
        
        # Hyper Parameters
        self.hparams = {
            'num_classes': num_classes,
            'base_model': base_model.__class__.__name__,
            'classifier': str(self.classifier),
            'batch_size': batch_size,
            'precision': precision,
            'criterion': criterion.__name__,
            'optimizer': optimizer.func.__name__ if type(optimizer) is partial else optimizer.__class__.__name__,
            **optimizer.keywords
        }
    
    #### MODEL - forward ####
    def forward(self, x):
        x = self.base_model(x)
        x = F.relu(x)
        x = self.classifier(x)
        return x
    
    #### OPTIMIZER ####
    def configure_optimizers(self):
        optimizer = self.optimizer(self.parameters())
        return optimizer
    
    #### SAVE MODEL ####
    ## save when test is done
    def teardown(self, stage):
        if stage == 'test':
            for logger in self.logger:
                if logger.__class__.__name__ == 'MLFlowLogger':
                    run_id = logger.run_id
                    mlflow.pytorch.save_model(self, f'./results/{run_id}')
                    logger.experiment.log_artifacts(logger.run_id, f'./results/{run_id}')
                    print('Artifacts Saved on MLflow Server')
        
    #### LEARNING LOOP - training ####
    def training_step(self, batch, batch_idx):
        x, y, f = batch
        y_hat = self(x)
        loss = self.criterion(y_hat, y)
        accuracy = FM.accuracy(y_hat, y, self.num_classes)
        result = pl.TrainResult(loss)
        result.log('train_loss', loss, on_step=True, on_epoch=True, reduce_fx=torch.mean, sync_dist=True)
        result.log('train_accuracy', accuracy, on_step=True, on_epoch=True, reduce_fx=torch.mean)
        return result

    #### LEARNING LOOP - validation ####
    def validation_step(self, batch, batch_idx):
        x, y, f = batch
        y_hat = self(x)
        loss = self.criterion(y_hat, y)
        accuracy = FM.accuracy(y_hat, y, self.num_classes)
        result = pl.EvalResult(checkpoint_on=loss)
        result.log('val_loss', loss, ) # , on_step=False, on_epoch=True, reduce_fx=torch.mean)
        result.log('val_accuracy', accuracy, ) #, on_step=False, on_epoch=True, reduce_fx=torch.mean)
        return result

    #### LEARNING LOOP - test ####
    def test_step(self, batch, batch_idx):
        x, y, f = batch
        y_hat = self(x)
        loss = self.criterion(y_hat, y)   # F.cross_entropy
        accuracy = FM.accuracy(y_hat, y, self.num_classes)
        result = pl.EvalResult()
        result.log('test_loss', loss, prog_bar=False)
        result.log('test_accuracy', accuracy, prog_bar=False)
        return result
        
