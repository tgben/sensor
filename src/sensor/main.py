'''
sensor entry point
  1. loads config
  2. creates shared data structures:
    ringbuffer
    flowtable
    exportqueue
  3. starts threads:
    capture.py
    process.py
    export.py

  threads:
    capture:
      reads raw packets from input
      creates packets from them
      writes packets to ringbuffer
    process:
      reads packets from ringbuffer
      creates flows using packets
      adds them to flowtable LRU
    evict:
      on a timer...
      evicts expired flows from the flowtable
      adds them flows to exportqueue
    purge:
      an a (different) timer...
      runs one last eviction
      purges the exportqueue to output
'''


import threading
import logging
import datetime
from sensor.config import loadConfig
from sensor.capture.capture import captureLoop
from sensor.process.process import processLoop
from sensor.export.export import evictLoop, purgeLoop
from sensor.shared.ringbuffer import RingBuffer
from sensor.shared.flowtable import FlowTable
from sensor.shared.exportqueue import ExportQueue


def main():
  # main loop
  cfg = loadConfig()
  logging.basicConfig(level=cfg.logging.level)
  log = logging.getLogger(__name__)
  ringbuffer = RingBuffer(cfg)
  flowtable = FlowTable(cfg)
  exportqueue = ExportQueue(cfg)

  capture_thread = threading.Thread(
    target=captureLoop,
    args=(cfg, ringbuffer))

  process_thread = threading.Thread(
    target=processLoop,
    args=(cfg, ringbuffer, flowtable))

  evict_thread = threading.Thread(
    target=evictLoop,
    args=(cfg, flowtable, exportqueue))

  purge_thread = threading.Thread(
    target=purgeLoop,
    args=(cfg, exportqueue))

  threads = [
    capture_thread,
    process_thread,
    evict_thread,
    purge_thread,]

  [t.start() for t in threads]
  [t.join() for t in threads]

if __name__ == "__main__":
  main()