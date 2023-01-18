# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_checkers.ipynb.

# %% auto 0
__all__ = ['is_list', 'is_tuple', 'list_or_tuple', 'is_iter', 'is_dict', 'is_df', 'is_str', 'is_int', 'is_float', 'is_array',
           'is_pilimage', 'is_tensor', 'is_set', 'is_path', 'path_or_str', 'is_norm', 'is_frozen', 'is_unfrozen',
           'is_subscriptable', 'is_sequential', 'is_clip']

# %% ../nbs/01_checkers.ipynb 3
from .core import *
from .imports import *

# %% ../nbs/01_checkers.ipynb 4
def is_list(x):
    return isinstance(x, list)

def is_tuple(x):
    return isinstance(x, tuple)

def list_or_tuple(x):
    return (is_list(x) or is_tuple(x))

def is_iter(o):
    "Test whether `o` can be used in a `for` loop"
    #Rank 0 tensors in PyTorch are not really iterable
    return isinstance(o, (Iterable,Generator)) and getattr(o,'ndim',1)

def is_dict(x):
    return isinstance(x, dict)

def is_df(x):
    return isinstance(x, pd.core.frame.DataFrame)

def is_str(x):
    return isinstance(x, str)

def is_int(x):
    return isinstance(x, int)    

def is_float(x):
    return isinstance(x, float)

def is_array(x):
    return isinstance(x, np.ndarray)

def is_pilimage(x):
    return 'PIL' in str(type(x))

def is_tensor(x):
    return isinstance(x, torch.Tensor)

def is_set(x):
    return isinstance(x, set)

def is_path(x):
    return isinstance(x, Path)

def path_or_str(x):
    return is_str(x) or is_path(x)

def is_norm(x):
    return type(x).__name__ == 'Normalize'

def is_frozen(model):
    return np.array([not p.requires_grad for p in (params(model))]).all()

def is_unfrozen(model):
    return np.array([p.requires_grad for p in (params(model))]).all()

def is_subscriptable(x):
    return hasattr(x, '__getitem__')

def is_sequential(x):
    return isinstance(x, nn.Sequential)

def is_clip(x):
    return type(x).__name__ == 'ProntoClip' or 'moviepy' in str(type(x))