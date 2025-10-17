'''
tests for exportqueue
'''


import datetime
from sensor.config import ExportConfig
from sensor.shared.exportqueue import ExportQueue
from sensor.shared.types import Flow, FiveTuple


def flow_generator(n: int):
  for i in range(n):
    f = Flow(
      fivetuple=FiveTuple(sip=1,dip=2,sport=3,dport=4,proto=5),
      timestamp=datetime.datetime.utcnow)
    yield f


def test_append_purge():
  flows = flow_generator(5)
  eq = ExportQueue(ExportConfig())

  for flow in flows:
    eq.append(flow)
  assert len(eq) == 5

  purged = eq.purge()
  assert len(purged) == 5
  assert len(eq) == 0
