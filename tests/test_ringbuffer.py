'''
tests for ringbuffer
'''


import pytest
from pathlib import Path
from sensor.shared.ringbuffer import RingBuffer
from sensor.config import loadConfig
from tests.utils import packet_generator


def test_resize():
  cfg = loadConfig(Path('tests/config.yaml'))
  cfg.capture.min_buffer = min_buffer = 25
  cfg.capture.max_buffer = max_buffer = 100

  rb = RingBuffer(cfg)

  expected_len = 0
  expected_capacity = min_buffer

  assert rb.capacity == expected_capacity
  assert len(rb) == expected_len

  packets = packet_generator(
    num_packets=max_buffer + 2,
    num_flows=max_buffer + 2)

  for _ in range(min_buffer):
    rb.push(next(packets))
    expected_len += 1
    assert len(rb) == expected_len
    assert rb.capacity == expected_capacity

  for _ in range(max_buffer - min_buffer):
    rb.push(next(packets))
    expected_len += 1
    assert len(rb) == expected_len
    if len(rb) > expected_capacity:
      expected_capacity *= 2
    assert rb.capacity == expected_capacity


def test_push_pop():
  cfg = loadConfig(Path('tests/config.yaml'))
  rb = RingBuffer(cfg)
  rb.push(1)
  assert rb.size == 1
  rb.push(2)
  assert rb.size == 2

  assert rb.pop()
  assert rb.pop()
  assert rb.size == 0
  assert not rb.pop()
  
  assert not rb.push(None)
  assert not rb.pop()