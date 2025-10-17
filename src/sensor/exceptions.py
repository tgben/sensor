'''
custom exceptions
'''

class ParsingError(Exception):
  def __init__(self, message="failed to parse packet.", layer='unknown'):
    self.layer = layer
    super().__init__(message)

class ConfigError(Exception):
  def __init__(self, option, message: str):
    super().__init__(f"Error setting {option}. {message}")
