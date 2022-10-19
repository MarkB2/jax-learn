# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_datamodule.ipynb.

# %% auto 0
__all__ = ['Desc', 'noop', 'Transform', 'Compose', 'ToFloat', 'DataModule']

# %% ../nbs/01_datamodule.ipynb 2
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Tuple, List, Mapping, Callable
import numpy as np
from fastcore.test import test_eq, ExceptionExpected
from torch.utils.data import Dataset, DataLoader

# %% ../nbs/01_datamodule.ipynb 5
class Desc(Enum):
  IMAGE = 1
  LABEL = 2

def noop(x): return x

class Transform:
  dtype:np.dtype = np.float32
  kinds:Mapping[Desc, Callable] = {}

  def do(self, item, desc:Desc):
    'Transform only items declared in `self.kinds`'
    func = self.kinds.get(desc, noop)
    return func(item)

  def __call__(self, items: List[Any], descriptor: Tuple[str] = None) -> Any:
    descriptor = descriptor or self.descriptor
    if not descriptor:
      raise Exception(f'{self.__class__.__name__} got empty descriptor')
    return [self.do(item, desc) for item, desc in zip(items, descriptor)]

class Compose(Transform):
  transforms:List[Transform]

  def __init__(self, transforms:List[Transform]) -> None:
    self.transforms = transforms

  def __call__(self, items: List[Any], descriptor:Tuple[Desc]) -> Any:
    return [transform(items, descriptor) for transform in self.transforms]

class ToFloat(Transform):

  def __init__(self, descriptor:Tuple[Desc] = None) -> None:
    self.kinds = {Desc.IMAGE:self.image_to_float}
    self.descriptor = descriptor

  def image_to_float(self, item):
    return np.array(item, dtype=self.dtype) / 255

# %% ../nbs/01_datamodule.ipynb 11
class DataModule(ABC):
  pass

