'''
test flowtable
'''


import pytest
import socket
import datetime
import random
from sensor.config import FlowTableConfig
from sensor.shared.flowtable import FlowTable
from sensor.shared.types import Packet, FiveTuple


def packet_generator(num_packets, num_flows):
  for i in range(num_packets):
    ft = FiveTuple(
      sip=socket.inet_aton(f'255.0.0.{i}'),
      dip=socket.inet_aton(f'192.0.0.{i}'),
      sport=i,
      dport=i,
      proto=17,)
    packet = Packet(ft, datetime.datetime.utcnow)
    yield packet

def test_size_eviction():
  packets = list(packet_generator(20, 20))
  ftc = FlowTableConfig()
  flowtable = FlowTable(ftc)
  for _ in range(0, flowtable.capacity + 2):
    flowtable.put(packets.pop())

  assert flowtable.size == flowtable.capacity
  assert flowtable.evict()
  assert flowtable.evict()
  assert flowtable.size == flowtable.capacity - 2
  
  p = packets.pop()
  flowtable.put(p)
  assert flowtable.size == flowtable.capacity - 1
  flowtable.put(p)
  assert flowtable.size == flowtable.capacity - 1