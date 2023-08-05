
import numpy as np
import torch, librosa, cv2

################################
#### Mel Spectrogram
################################
class MelSpectrogram(object):
    
    def __init__(self, height=128, sqsecs=2.56):
        self.height = height
        self.aspect = sqsecs / height
    
    def __call__(self, y, sr):
        hop_length = int(self.aspect * sr)
        n_fft = hop_length*4
        y = librosa.feature.melspectrogram(y, sr, None, n_fft, hop_length, n_mels=self.height)
        y = librosa.power_to_db(y)
        return y, sr
    
################################
#### STFT
################################
class STFT(object):
    
    def __init__(self, n_fft=1000, sqsecs=2.56, normalize=None):
        self.n_fft = n_fft
        self.aspect = sqsecs / (n_fft//2 + 1)
        self.normalize = normalize
        
    def __call__(self, y, sr):
        self.hop_length = int(self.aspect * sr)
        y = librosa.stft(y, self.n_fft, self.hop_length)
        y = np.abs(y)
        return y, sr

################################
#### DWT
################################



################################
#### CWT
################################


    
################################
#### Scale
################################
# 0 ~ 1 float
# 0 ~ 255 uint8
class Scale(object):
    def __init__(self, mean=None, std=None, cutoff=(-3, 3)):
        self.mean = mean
        self.std = std
        self.cutoff = cutoff
    def __call__(self, y, sr):
        if all([x is not None for x in [self.mean, self.std]]):
            y = (y - self.mean) / self.std
            cutL, cutH = self.cutoff
            y = np.clip(y, cutL, cutH)
            y = (y - cutL) / (cutH - cutL) 
        return y, sr
    

################################
#### Square Crop
################################
class SquareCrop(object):   
    def __init__(self, position='left'):
        self.position = position
    
    def __call__(self, x, np_order):
        if np_order == 'chw':
            x = np.transpose(x, (1, 2, 0))
        elif np_order == 'hwc':
            x = x
        else:
            print('ERROR!!!')
        h, w, c = x.shape
            
        #### if width is smaller than height, drop the data 
        if w <= h:
            return x
        #### do crop
        if self.position == 'left':
            x = x[:, :h, :]
        elif self.position == 'center':
            x = x[:, w//2-h//2:w//2+h//2, :]
        elif self.position == 'right':
            x = x[:, -h:, :]
        elif self.position == 'random':
            l = np.random.randint(0, w - h)
            x = x[:, l:l+h, :]
        else:
            print('ERROR!!! crop options: [left, center, right, random]')  
            
        #####
        if np_order == 'chw':
            x = np.transpose(x, (2, 0, 1))
        return x, np_order


################################
#### Resize
################################
class Resize(object):
    def __init__(self, height=224, width='fixed_aspect'):
        self.height = height
        self.width = width
        
    def __call__(self, x, np_order):
        
        #### REORDER
        if np_order == 'chw':
            x = np.transpose(x, (1, 2, 0))
        elif np_order == 'hwc':
            x = x
        else:
            print('ERROR!!!')
        h, w, c = x.shape
        
        #### SET WIDTH
        if self.width == 'fixed_aspect':
            width = int(w * self.height / h)
        elif self.width == 'fixed_width':
            width = w
        elif type(width) is int:
            width = width
        else:
            print('ERROR!!! resize options: "fixed_aspect", "fixed_width", int()')
        
        #### RESIZE
        cv2.setNumThreads(0)
        x = cv2.resize(x, (width, self.height))
        
        #### REORDER
        if np_order == 'chw':
            x = np.transpose(x, (2, 0, 1))
        
        return x, np_order

    
################################
#### Rolling
################################
class Rolling(object):
    def __init__(self, shift='random'):
        self.shift = shift
    
    def __call__(self, x, np_order):
        axis = np_order.index('w')
        width = x.shape[axis]
        if self.shift == 'random':
            shift = np.random.randint(0, width)
        elif type(self.shift) is int:
            shift = self.shift
        else:
            print("ERROR!!! only 'random' is available now")
        x = np.roll(x, shift, axis)
        return x, np_order
