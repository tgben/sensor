'''
configuration
  stores configuration in a basic data class
  loaded by main.py
'''


from dataclasses import dataclass, field
import logging
import yaml
from pathlib import Path
from sensor.exceptions import ConfigError


log = logging.getLogger(__name__)

@dataclass
class FlowTableConfig:
  capacity: int = 0
  max_flow_duration: int = 0

  def validate(self):
    if (
      self.capacity <= 0 or
      not isinstance(self.capacity, int)):
      raise ConfigError(self.capacity, 'capacity is not a positive integer.')
    if (
      self.max_flow_duration <=0 or
      not isinstance(self.max_flow_duration, int)):
      raise ConfigError(self.max_flow_duration, 'max_flow_duration is not a positive integer.')

  
@dataclass
class CaptureConfig:
  input_mode: str = ''
  input_pcap: str = ''

  def __post_init__(self):
    self.input_mode = self.input_mode.lower()

  def validate(self):
    input_mode_options = ['pcap']
    if (not self.input_mode or
        self.input_mode not in input_mode_options or
        not isinstance(self.input_mode, str)):
      raise ConfigError(self.input_mode, f'input mode is invalid. options: {input_mode_options}')
    if self.input_mode == 'pcap':
      if not self.input_pcap:
        raise ConfigError(self.input_pcap, 'input_mode is defined but input pcap is not.')
      if not Path(self.input_pcap).exists():
        raise ConfigError(self.input_pcap, 'input_pcap is not a valid path.')

@dataclass
class LoggingConfig:
  level: int | str = logging.INFO

  def __post_init__(self):
    if isinstance(self.level, str):
      self.level = getattr(logging, self.level.upper(), None)

  def validate(self):
    pass


@dataclass
class ProcessConfig:
  export_interval: float = 0.01

  def validate(self):
    pass


@dataclass
class ExportConfig:
  purge_interval: int = 360 # interval that export() flushes buffer to a log file.
  evict_interval: int = 10
  output_mode: str = ''
  output_file: str = ''

  def validate(self):
    pass


@dataclass
class Config:
  flowtable: FlowTableConfig = field(default_factory=FlowTableConfig)
  capture: CaptureConfig = field(default_factory=CaptureConfig)
  logging: LoggingConfig = field(default_factory=LoggingConfig)
  process: ProcessConfig = field(default_factory=ProcessConfig)
  export: ExportConfig = field(default_factory=ExportConfig)

  def validate(self):
    self.flowtable.validate()
    self.capture.validate()
    self.logging.validate()
    self.process.validate()
    self.export.validate()

def load_config(path: Path = Path("../config.yaml")) -> Config:
  if not path.exists():
    raise ConfigError(path, 'config path does not exist.')
  
  with open(path, 'r') as f:
    data = yaml.safe_load(f)
  cfg = Config()

  try:
    cfg.flowtable = FlowTableConfig(**data['flowtable'])
    cfg.capture = CaptureConfig(**data['capture'])
    cfg.logging = LoggingConfig(**data['logging'])
    cfg.process = ProcessConfig(**data['process'])
    cfg.export = ExportConfig(**data['export'])
  except Exception as e:
    e.add_note('Failed to load config. Missing a config category')
    raise e

  cfg.validate()
  return cfg
