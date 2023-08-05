import sys, getpass, socket, torch
from torchvision import models
import torch.nn.functional as F
import torch.optim as optim
from functools import partial
from pytorch_lightning.callbacks import Callback, EarlyStopping, GpuUsageLogger, ModelCheckpoint
from pytorch_lightning.loggers import MLFlowLogger, TensorBoardLogger

def parser(data_dir, labels, experiment_name, run_name, model, criterion, optimizer, lr, momentum, betas, weight_decay, 
           batch_size, epochs, monitor, early_stop, patience, tracking_uri, tensorboard, cpu, half_precision, seed):    
    
    ################################################################
    # 0. Parser
    ################################################################
    
    if optimizer.lower() == 'adam':
        optimizer = 'Adam'
        optimizer_params = {'lr': lr, 'betas': betas, 'weight_decay': weight_decay}
    elif optimizer.lower() == 'adamw':
        optimizer = 'AdamW'
        optimizer_params = {'lr': lr, 'betas': betas, 'weight_decay': weight_decay}
    elif optimizer.lower() == 'sparseadam':
        optimizer = 'SparseAdam'
        optimizer_params = {'lr': lr, 'betas': betas, 'weight_decay': weight_decay}
    elif optimizer.lower() == 'sgd':
        optimizer = 'SGD'
        optimizer_params = {'lr': lr, 'momentum': momentum, 'weight_decay': weight_decay}
    else:
        print(f"ERROR!!! optimizer {optimizer} not available")
    
    if not cpu:
        gpus = torch.cuda.device_count()
        precision = 16 if half_precision else 32
        distributed_backend = 'ddp' if gpus > 1 else None
            
    min_delta = early_stop
    
    ################################################################
    # 1. SET DATA
    ################################################################
    args_data = {
        'batch_size': batch_size
    }
    
    ################################################################
    # 2. SET MODEL
    ################################################################
    
    # loss function
    criterion = eval(f'F.{criterion}')
    optimizer = partial(eval(f'optim.{optimizer}'), **optimizer_params)
        
    args_model = {
        'base_model': models.mobilenet_v2(True),
        'batch_size': batch_size,
        'precision': f'{precision}-bit',
        'criterion': criterion,
        'optimizer': optimizer,
    }
    
    ################################################################
    # 3. SET LOGGER
    ################################################################
    
    loggers = []

    # MLflow Logger
    if True:
        loggers.append(
            MLFlowLogger(
                experiment_name=experiment_name,
                tracking_uri=tracking_uri,
                tags={
                    'mlflow.runName': run_name,
                    'mlflow.user': getpass.getuser(),
                    'mlflow.source.name': sys.argv[0],
                    'data_dir': f'{socket.getfqdn()}:{data_dir}',
                    'labels': labels if labels else 'inferred from subdir name',
                }
            )
        )
        
    # Tensorboard logger
    if tensorboard:
        loggers.append(
            TensorBoardLogger(
                save_dir='./logs',
            )
        )
    
    ################################################################
    # 4. SET TRAINER
    ################################################################
    
    # Early stopping
    early_stop_callback = EarlyStopping(monitor, min_delta, patience)
    
    # Checkpoint
    checkpoint_callback = ModelCheckpoint(
        filepath='./ckpts/|{epoch:03d}|{val_loss:.3f}|{val_accuracy:.3f}',
        prefix=f'{experiment_name}|{run_name}',
    )
    
    # Callbacks
    callbacks = []
    
    # SET TRAINER
    args_trainer = {
        'gpus': gpus,
        'precision': precision,
        'max_epochs': epochs,
        'checkpoint_callback': checkpoint_callback,
        'early_stop_callback': early_stop_callback,
        'callbacks': callbacks,
        'logger': loggers,
    }
    
    if distributed_backend:
        arg_trainer['distributed_backend'] = distributed_backend
    
    return args_data, args_model, args_trainer
