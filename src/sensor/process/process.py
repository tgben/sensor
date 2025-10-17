'''
thread loop:
  consume raw packet from ringbuffer
  creates packet class instance from raw packet
  extracts data and adds it to the packet class
  calls flowtable add packet to flow with packet
'''


import logging, time
from sensor.shared.ringbuffer import RingBuffer
from sensor.shared.flowtable import FlowTable
from sensor.config import Config


def process_loop(
  config: Config,
  ringbuffer: RingBuffer,
  flowtable: FlowTable):
  # pop packets from ringbuffer
  # add packets to flowtable
  
  log = logging.getLogger(__name__)

  while True:
    time.sleep(0.1)
    packet = ringbuffer.pop()
    if packet:
      flowtable.put(packet)
