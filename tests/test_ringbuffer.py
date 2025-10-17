'''
tests for ringbuffer
'''


import pytest
from sensor.shared.ringbuffer import RingBuffer


def test_size():
  for i in range(0, 50, 10):
    rb = RingBuffer(i)
    assert rb.capacity == max(rb._min_size, i)


def test_push_pop():
  rb = RingBuffer(30)
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