'''
flow table class implemented with an LRU
  each element in the LRU is a Node that holds a flow
  The LRU manages itself by:
    evicts packets when LRU is too long (or size is too big)
    evicts packets when they expire (max flow size)
  flows are added by process_loop
  flows are manually evicted by export_loop
    (in addition to auto-evicted by expiration or LRU hitting capacity)
'''


import logging
import datetime
from sensor.config import Config
from sensor.shared.types import Packet, Flow


log = logging.getLogger(__name__)

class Node:
  # A node that holds flows and extra information used to manage the LRU

  def __init__(self, flow, key, prev=None, next=None):
    self.flow = flow
    self.key = key
    self.prev = prev
    self.next = next

class FlowTable:
  # The flowtable implemented by an LRU cache.

  def __init__(self, cfg: Config):
    self.cfg = cfg
    self.capacity = self.cfg.flowtable.capacity
    self.size = 0
    self.mem = {}
    self.head = self.tail = None

  def __str__(self):
    flows = []
    cur = self.head
    while cur:
      flows.append(str(cur.flow))
      cur = cur.next
    res = {
      'capacity': self.capacity,
      'size': self.size,
      # 'flows': flows,
    }
    return str(res)

  def __remove(self, n):
    # remove a node n from the LRU
    # return the romeved node if we removed it, else return None
    if n == self.head == self.tail:
      self.head, self.tail = None, None
    elif n == self.head:
      self.head = self.head.next
      self.head.prev = None
    elif n == self.tail:
      self.tail = self.tail.prev
      self.tail.next = None
    else:
      n.prev.next = n.next
      n.next.prev = n.prev
    return n

  def __insert(self, n):
    # insert a node into the LRU
    if not self.head:
      self.head = self.tail = n
      n.next = None
      n.prev = None
      return
    self.head.prev = n
    n.next = self.head
    n.prev = None
    self.head = n

  def __get(self, key: int) -> int:
    # given a key, get the value
    # returns -1 if key not in LRU
    if key not in self.mem:
      return -1
    n = self.mem[key]
    self.__remove(n)
    self.__insert(n)
    return n.flow

  def put(self, packet: Packet) -> None:
    # given a key & flow, insert the node
    # packet and flow keys should be the same if same 5-tuple
    key = hash(packet)

    # flow exists in the LRU, update it.
    if key in self.mem:
      n = self.mem[key]
      self.__remove(n)
      self.__insert(n)
      self.update_flow(n.flow, packet)
      return
    
    # flow does not exist in the LRU, create an new one and add it.
    flow = Flow(packet.fivetuple , packet.timestamp)
    n = Node(flow, key)
    self.mem[key] = n
    if self.size == self.capacity:
      self.evict(self.tail)
    self.__insert(n)
    self.size += 1 
 
  def update_flow(self, flow: Flow, packet: Packet):
    # update an existing flow with a packet information
    flow.packet_count += 1

  def evict(self, n=None):
    # evicts a node. Defaults to evicting the tail.
    if not n: n = self.tail
    del_n = self.__remove(n)
    del self.mem[del_n.key]
    self.size -= 1
    return del_n.flow

  def evictExpiredFlows(self):
    # evict all expired flows
    res = []
    flows_to_evict = []
    for key, node in self.mem.items():
      timestamp = node.flow.timestamp
      delta = datetime.timedelta(seconds=self.cfg.flowtable.max_flow_duration)
      expire_timestamp = timestamp + delta
      if expire_timestamp < datetime.datetime.now():
        flows_to_evict.append((key, node))
    for key, node in flows_to_evict:
      flow = self.evict(node)
      res.append(flow)
    return res
