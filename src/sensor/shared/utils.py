from functools import wraps
from typing import Callable
from pathlib import Path
from dataclasses import dataclass, replace
from sensor.config import load_config

def sync(func: Callable) -> Callable:
  # make a function thread-safe.
  @wraps(func)
  def wrapper(self, *args, **kwargs):
    with self.lock:
      res = func(self, *args, **kwargs)
    return res
  return wrapper
