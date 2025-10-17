'''
thread loop:
  have a sleep timer
  when sleep ends:
    write all flows in exportqueue to disc in json
    clear exportqueue
'''


import logging
import time
import json
from sensor.config import Config
from sensor.shared.exportqueue import ExportQueue
from sensor.shared.flowtable import FlowTable


log = logging.getLogger(__name__)

def purge_loop(cfg: Config, exportqueue: ExportQueue):
  # thread that purges the exportqueue and writes it to output.

  def output_to_file():
    if not cfg.export.output_file:
      raise ConfigError('output mode is file and no output file was specified.')
    with open(cfg.export.output_file, 'w') as f:
      purged = exportqueue.purge()
      log.debug(f'purged {len(purged)} flows.')
      for flow in purged:
        log.debug(flow.toJSON())


  def purge():
    if cfg.export.output_mode == 'file':
      output_to_file()


  num_purges = 0
  while True:
    time.sleep(cfg.export.purge_interval)
    purge()
    num_purges += 1
    log.debug(f'Purged exportqueue. {num_purges}.')


def evict_loop(
  cfg: Config,
  flowtable: FlowTable,
  exportqueue: ExportQueue):
  # evict expired flows from the flowtable
  # & add them to the exportqueue

  while True:
    time.sleep(cfg.export.evict_interval)
    evicted_flows = flowtable.evictExpiredFlows()
    log.debug(f'evicted {len(evicted_flows)} expired flows.')
    for flow in evicted_flows:
      exportqueue.append(flow)
