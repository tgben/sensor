'''
custom datatypes:
  FiveTuple
  Packet
  Flow
'''


from dataclasses import dataclass, field
import datetime
import socket
import json


'''
five tuple representation
'''
@dataclass
class FiveTuple:
  sip: bytes = None
  dip: bytes = None
  sport: int = None
  dport: int = None
  proto: int = None
  
  def __str__(self):
    return str({
      'sip': socket.inet_ntoa(self.sip),
      'dip': socket.inet_ntoa(self.dip),
      'sport': self.sport,
      'dport': self.dport,
      'proto': self.proto})

  def validate(self):
    if (not self.sip or
        not self.dip or
        not self.sport or
        not self.dport or
        not self.proto):
        raise ParsingError(f'malformed fivetuple {self.__str__()}')
  
'''
packet definition
'''
@dataclass
class Packet:
  timestamp: datetime.datetime
  fivetuple: FiveTuple = None
  
  def __hash__(self):
    return hash((
      self.fivetuple.sip,
      self.fivetuple.dip,
      self.fivetuple.proto,
      self.fivetuple.sport,
      self.fivetuple.dport))
  
  def __str__(self):
    return f'''
    timestamp:\t{self.timestamp}
    sip:\t{socket.inet_ntoa(self.fivetuple.sip)}
    dip:\t{socket.inet_ntoa(self.fivetuple.dip)}
    sport:\t{self.fivetuple.sport}
    dport:\t{self.fivetuple.dport}
    proto:\t{self.fivetuple.proto}
    '''

  def validate(self):
    self.fivetuple.validate()
    if not self.timestamp:
      log.debug(f'malformed timestamp: {self.timestamp}')
      raise ParsingError(f'malformed timestamp: {self.timestamp}')

'''
flow definition
'''
@dataclass
class Flow:
  fivetuple: FiveTuple
  timestamp: datetime.datetime
  packet_count: int = 1
    
  def __hash__(self):
    return hash((
      self.fivetuple.sip,
      self.fivetuple.dip,
      self.fivetuple.sport,
      self.fivetuple.dport,
      self.fivetuple.proto
    ))

  def toJSON(self):
    return json.dumps({
      'timestamp': self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
      'sip': socket.inet_ntoa(self.fivetuple.sip),
      'dip': socket.inet_ntoa(self.fivetuple.dip),
      'sport': self.fivetuple.sport,
      'dport': self.fivetuple.dport,
      'proto': self.fivetuple.proto,
      'packet_count': self.packet_count})
