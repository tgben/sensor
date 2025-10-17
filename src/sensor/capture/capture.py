'''
thread loop:
  reads from pcap file or NIC
  writes packets to ringbuffer to be processed
'''


import time, logging, datetime
import dpkt
from sensor.config import Config
from sensor.shared.ringbuffer import RingBuffer
from sensor.shared.types import Packet, FiveTuple
from sensor.exceptions import ParsingError


IPV4_ETHERTPE = 0x800
IPV6_ETHERTYPE = 0x86DD
UDP_PROTO = 17
TCP_PROTO = 6


log = logging.getLogger(__name__)

def capture_loop(cfg: Config, ringbuffer: RingBuffer):

  def parse_ipv4(packet: Packet, buf):
    packet.fivetuple.sip = buf.src
    packet.fivetuple.dip = buf.dst
    packet.fivetuple.proto = buf.p
    if buf.p == UDP_PROTO:
      parse_udp(packet, buf.data)
    elif buf.p == TCP_PROTO:
      parse_udp(packet, buf.data)
    else:
      raise ParsingError('unknown protocol {buf.p}', layer='ip')

    
  def parse_ipv6(packet: Packet, buf):
    raise NotImplementedError


  def parse_udp(packet: Packet, buf):
    packet.fivetuple.sport = buf.sport
    packet.fivetuple.dport = buf.dport


  def parse_tcp(packet: Packet, buf):
    packet.fivetuple.sport = buf.sport
    packet.fivetuple.dport = buf.dport


  def parse_eth(packet: Packet, buf):
    try:
      eth = dpkt.ethernet.Ethernet(buf)
      if eth.type == IPV4_ETHERTPE:
        parse_ipv4(packet, eth.data)
      elif eth.type == IPV4_ETHERTPE:
        parse_ipv6(packet, eth.data)
      else:
        raise ParsingError("unknown eth type {eth.type}")
    except:
      log.debug('Unknown Parsing Error')


  def parse_packet(timestamp: datetime.datetime, buf) -> Packet:
    timestamp = datetime.datetime.utcfromtimestamp(timestamp)
    packet = Packet(timestamp=timestamp, fivetuple=FiveTuple())
    parse_eth(packet, buf)
    packet.validate()
    return packet


  def capture_pcap():
    with open(cfg.capture.input_pcap, "rb") as f:
      pcap = dpkt.pcap.Reader(f)
      for timestamp, buf in pcap:
        packet = parse_packet(timestamp, buf)
        ringbuffer.push(packet)
    
  if cfg.capture.input_mode == 'pcap':
    capture_pcap()