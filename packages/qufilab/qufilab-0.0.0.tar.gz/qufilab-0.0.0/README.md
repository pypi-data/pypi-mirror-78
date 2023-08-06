# QufiLab
Qufilab is a fast and modern technical indicators library 
implemented in c++.

## Features
* Wide array of technical indicators.

## Installation
```bash
Not yet implemented
```
Documentation for QufiLab can be found at: <https://qufilab.readthedocs.io>

## Usage
> **WARNING**: All of qufilab's technical indicators are implemented in c++
and a big part of the speed performance comes from the fact that no 
type conversion exist between python and c++. In order for this to work, numpy arrays
of type **numpy.dtype.float64 (double) or numpy.dtype.float32 (float)** are preferably used. Observe that all other types of numpy arrays still are accepted, however the retured numpy array will be converted into the type **numpy.dtype.float64**.

#### Indicators
```python
import qufilab as ql
import numpy as np

# Creates an ndarray with element type float64.
data = np.random.rand(1000000)

# Calculate sma with a period of 200.
sma = ql.sma(data, period = 200)

# Calculate bollinger bands with a period of 20 and two standard deviations from the mean.
upper_band, middle_band, lower_band = ql.bbands(data, period = 20, deviation = 2)
```



