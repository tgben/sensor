'''
test flowtable
'''


import pytest
import socket
import datetime
import random
from pathlib import Path
from sensor.config import load_config
from sensor.shared.flowtable import FlowTable
from sensor.shared.types import Packet, FiveTuple
from tests.utils import packet_generator



def test_size_eviction():
  cfg = load_config(Path('tests/config.yaml'))
  flowtable = FlowTable(cfg)
  packets = packet_generator(flowtable.capacity + 10, flowtable.capacity + 10)
  for packet in packets:
    flowtable.put(packet)

  assert flowtable.size == flowtable.capacity
  assert flowtable.evict()
  assert flowtable.evict()
  assert flowtable.size == flowtable.capacity - 2
  
  # eviction
  packets = packet_generator(3, 3)
  flowtable.put(next(packets))
  assert flowtable.size == flowtable.capacity - 1

  # refill
  flowtable.put(next(packets))
  assert flowtable.size == flowtable.capacity
  flowtable.put(next(packets))
  assert flowtable.size == flowtable.capacity