![Build Status](https://github.com/l-johnston/ha7000d/workflows/publish/badge.svg)
# `ha7000d`
Python interface to the Holzworth HA7000D series Phase Noise Analyzer

## Installation
```linux
$ pip install ha7000d
```  

## Usage
```python
>>> from ha7000d import CommChannel
>>> import matplotlib.pyplot as plt
>>> with CommChannel("<ip address>") as pna:
>>>     x, y = pna.read()
>>> plt.semilogx(x, y)
[<matplotlib.lines.Line2D object at ...]
>>> plt.show()
>>>
```

## Supported
- Configuration
- Acquisition
- Not supported: LO calibration
