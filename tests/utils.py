
import socket
import datetime
from sensor.shared.types import Packet, FiveTuple

def packet_generator(num_packets, num_flows):
  for i in range(num_packets):
    ft = FiveTuple(
      sip=socket.inet_aton(f'255.0.0.{i}'),
      dip=socket.inet_aton(f'192.0.0.{i}'),
      sport=i,
      dport=i,
      proto=17,)
    packet = Packet(timestamp=datetime.datetime.utcnow, fivetuple=ft)
    yield packet

# # testing
# def with_config(path: Path, **overrides) -> Callable:
#   # decorator factory
#   def decorator(func: Callable) -> Callable:
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#       cfg = load_config(path)
#       if 'capture' in overrides:
#         new_capture = replace(cfg.capture, **overrides['capture'])
#         cfg = replace(cfg, capture=new_capture)
#       return func(*args, **kwargs)
#     return wrapper
#   return decorator