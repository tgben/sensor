'''
generic ringbuffer
  holds packets that have been ingested and parsed by capture
  process reads packets from this ringbuffer
technically can hold any data, but typehinted to hold Packets
'''


import logging
import threading
from sensor.config import Config
from sensor.shared.utils import sync


log = logging.getLogger(__name__)

# enforce singleton pattern with a metaclass
class RingBuffer:
  
  def __init__(self, cfg: Config):
    self.cfg = cfg
    self.data = [None] * self.cfg.capture.min_buffer
    self.head, self.tail = -1, 0
    self.size = 0
    self.capacity = self.cfg.capture.min_buffer
    self.lock = threading.Lock()
    
  @sync
  def push(self, element: Packet) -> bool:
    # pushes an item into the RB.
    if not element:
      return False
    if self.size >= self.capacity:
      self.__expand()
    self.head = (self.head + 1) % self.capacity
    self.data[self.head] = element
    self.size += 1
    return True

  @sync
  def pop(self):
    if not self.size:
      return None
    res = self.data[self.tail]
    self.data[self.tail] = None
    self.tail = (self.tail + 1) % self.capacity
    self.size -= 1
    if self.size < (self.capacity // 2):
      self.__shrink()
    return res

  def __shrink(self):
    if self.capacity > self.cfg.capture.min_buffer * 2:
      self.__copydata(self.capacity // 2)

  @sync
  def __str__(self):
    arr = []
    for i in range(self.size):
      index = (self.tail + i) % self.capacity
      arr.append(self.data[index])
    return f"{str(arr)}\n\tsize={self.size}\n\tcapacity={self.capacity}"

  @sync
  def __len__(self):
    return self.size
      
  def __expand(self):
    self.__copydata(self.capacity * 2)

  def __copydata(self, new_capacity):
    new_data = [None] * new_capacity
    for i in range(self.size):
      index = (self.tail + i) % self.capacity
      new_data[i] = self.data[index]
    self.data = new_data
    self.capacity = new_capacity
    self.tail = 0
    self.head = self.size - 1
