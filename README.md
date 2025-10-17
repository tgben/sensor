# Sensor

A network flow sensor in Python.

## Overview

Captures packets, aggregates them into flows based on 5-tuples, and exports the results. Built with a multi-threaded pipeline architecture to test out free-threading in Python 3.14 without GIL restrictions.

Four threads communicate via shared data structures:
- **Capture**: Reads packets → ring buffer
- **Process**: Processes packets → flow table
- **Evict**: Expires old flows → export queue
- **Purge**: Writes flows to output

## Installation

Requires Python >= 3.14

```bash
pip install -e .
```

## Usage

```bash
sensor
```

Edit `config.yaml` to configure.

## Testing

```bash
pytest
```

## License

MIT License
