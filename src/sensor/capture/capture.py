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

def captureLoop(cfg: Config, ringbuffer: RingBuffer):

  def parseIpv4(packet: Packet, buf):
    packet.fivetuple.sip = buf.src
    packet.fivetuple.dip = buf.dst
    packet.fivetuple.proto = buf.p
    if buf.p == UDP_PROTO:
      parseUdp(packet, buf.data)
    elif buf.p == TCP_PROTO:
      parseUdp(packet, buf.data)
    else:
      raise ParsingError('unknown protocol {buf.p}', layer='ip')

    
  def parseIpv6(packet: Packet, buf):
    raise NotImplementedError


  def parseUdp(packet: Packet, buf):
    packet.fivetuple.sport = buf.sport
    packet.fivetuple.dport = buf.dport


  def parseTcp(packet: Packet, buf):
    packet.fivetuple.sport = buf.sport
    packet.fivetuple.dport = buf.dport


  def parseEth(packet: Packet, buf):
    try:
      eth = dpkt.ethernet.Ethernet(buf)
      if eth.type == IPV4_ETHERTPE:
        parseIpv4(packet, eth.data)
      elif eth.type == IPV4_ETHERTPE:
        parseIpv6(packet, eth.data)
      else:
        raise ParsingError("unknown eth type {eth.type}")
    except:
      log.debug('Unknown Parsing Error')


  def parsePacket(timestamp: datetime.datetime, buf) -> Packet:
    timestamp = datetime.datetime.utcfromtimestamp(timestamp)
    packet = Packet(timestamp=timestamp, fivetuple=FiveTuple())
    parseEth(packet, buf)
    packet.validate()
    return packet


  def capturePcap():
    with open(cfg.capture.input_pcap, "rb") as f:
      pcap = dpkt.pcap.Reader(f)
      for timestamp, buf in pcap:
        packet = parsePacket(timestamp, buf)
        ringbuffer.push(packet)
    
  if cfg.capture.input_mode == 'pcap':
    capturePcap()