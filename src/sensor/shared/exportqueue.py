'''
queue that holds flows ready for export, but haven't been written yet
  written to by process.py
  consumed by export.py
'''


from collections import deque
import logging
from sensor.shared.types import Flow
from sensor.config import Config


log = logging.getLogger(__name__)

class ExportQueue:
  
  def __init__(self, cfg: Config):
    self.cfg = cfg
    self.data = deque()


  def append(self, flow: Flow):
    if not flow:
      return
    self.data.append(flow)


  def purge(self) -> list[Flow]:
    res = []
    while self.data:
      flow = self.data.popleft()
      res.append(flow)
    if not res:
      log.debug("attempted to purge empty export queue")
    return res

  
  def __len__(self):
    return len(self.data)
