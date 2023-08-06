# Copyright (c) 2020
# Author: xguo

import collections
import enum
import logging
import math
import numpy as np

# 20742009047
# 44110

TimeWindowDataEntry = collections.namedtuple(
    'TimeWindowDataEntry', ['timestamp', 'value'])

ONE_DAY_NANO_SECONDS = int(3600 * 24 * 1e9)


class WindowDataIterator(object):
  def __init__(self, window_data_container):
    self._iter = iter(window_data_container.data)

  def __next__(self):
    data = next(self._iter)
    return data.value


class MovingWindowData(object):
  def __init__(self, window_sec: float):
    self._window = int(window_sec * 1e9)
    self._deque = collections.deque()
    self._outdated = []

  def __len__(self):
    return len(self._deque)

  def __iter__(self):
    return WindowDataIterator(self)

  @property
  def window_size(self):
    return self._window

  @property
  def data(self):
    return self._deque

  @property
  def outdated(self):
    return self._outdated

  @property
  def time_range(self):
    return self._deque[0].timestamp, self._deque[-1].timestamp

  def has_outdated_in_deque(self, timestamp):
    if not self._deque:
      return False
    return timestamp - self._deque[0].timestamp >= self._window

  def update(self, timestamp: int, value):
    self._outdated.clear()
    while self.has_outdated_in_deque(timestamp):
      elem = self._deque[0]
      self._deque.popleft()
      self._outdated.append(elem)

    # Append new entry.
    new_entry = TimeWindowDataEntry(timestamp, value)
    self._deque.append(new_entry)


def get_window_index(timestamp, window):
  return int(timestamp // window)


class PeriodicWindowData(object):
  def __init__(self, window_sec: float, regular_grid=True):
    window = int(window_sec * 1e9)

    if regular_grid:
      assert window < ONE_DAY_NANO_SECONDS
      assert ONE_DAY_NANO_SECONDS % window == 0

    self._window = window
    self._regular_grid = regular_grid
    self._deque = collections.deque()
    self._ready_data = None
    self._current_window_index = 0
    self._current_timestamp = 0
    self._is_window_index_changed = False
    self._is_window_data_full = False

  def __len__(self):
    return len(self._deque)

  def __iter__(self):
    return WindowDataIterator(self)

  @property
  def window_size(self):
    return self._window

  @property
  def window_index(self):
    return self._current_window_index

  @property
  def data(self):
    return self._deque

  @property
  def ready_data(self):
    return self._ready_data

  @property
  def time_range(self):
    return self._deque[0].timestamp, self._deque[-1].timestamp

  def update_timestamp(self, timestamp: int):
    window_index = int(timestamp // self._window)

    if timestamp < self._current_timestamp:
      logging.error(
          "Wrong timestamp, ts: %s, current_ts: %s",
          timestamp, self._current_timestamp)
      return

    if window_index < self._current_window_index:
      logging.error(
          "Wrong window index, window index: %s, current window index %s",
          window_index, self._current_window_index)
      return

    if self._current_window_index > 0 and window_index > self._current_window_index:
      self._is_window_index_changed = True
    else:
      self._is_window_index_changed = False

    if self._deque and timestamp - self._deque[0].timestamp >= self._window:
      self._is_window_data_full = True
    else:
      self._is_window_data_full = False

    self._current_timestamp = timestamp
    self._current_window_index = window_index

  def is_data_ready(self):
    if not self._deque:
      return False
    return self._is_window_index_changed if self._regular_grid else self._is_window_data_full

  def update(self, timestamp: int, value):
    self.update_timestamp(timestamp)
    new_entry = TimeWindowDataEntry(timestamp, value)
    if self.is_data_ready():
      self._ready_data = self._deque
      self._deque = collections.deque()
    self._deque.append(new_entry)


class PeriodicCalculator(object):
  def __init__(self, window_sec, maxlen=None):
    self._data = PeriodicWindowData(window_sec, regular_grid=True)
    self._deque = collections.deque(maxlen=maxlen)
    self._maxlen = maxlen

  def __len__(self):
    return len(self._deque)

  @property
  def window_index(self):
    return self._data.window_index

  @property
  def window_size(self):
    return self._data.window_size

  @property
  def data(self):
    return self._deque

  def is_full(self):
    return len(self) == self._maxlen  # maxlen can be None

  def update(self, timestamp, value):
    self._data.update(timestamp, value)
    if self._data.is_data_ready():
      ohlc_data = self.process()
      self._deque.append(ohlc_data)


class OhlcCalculator(PeriodicCalculator):
  OhlcData = collections.namedtuple(
      'OhlcData',
      ['open', 'high', 'low', 'close', 'rtn', 'timestamp'])

  def process(self):
    values = [item.value for item in self._data.ready_data]
    ts = (self.window_index-1) * self.window_size
    data = self.OhlcData(
        open=values[0],
        high=max(values),
        low=min(values),
        close=values[-1],
        rtn=math.log(values[-1] / values[0]),
        timestamp=ts)
    return data


class PeriodicAccumulator(PeriodicCalculator):
  SumData = collections.namedtuple('SumData', ['value', 'timestamp'])

  def process(self):
    values = [item.value for item in self._data.ready_data]
    ts = (self.window_index-1) * self.window_size
    sum_data = self.SumData(value=sum(values), timestamp=ts)
    return sum_data


class VolatilityEstimator(enum.Enum):
  CLOSE_TO_CLOSE = 'close_to_close'
  PARKINSON = 'parkinson'
  GARMAN_KLASS = 'garman_klass'
  ROGER_SATCHELL_YOON = 'roger_satchell_yoon'
  YANG_ZHANG = 'yang_zhang'


class VolatilityCalculator(object):
  def __init__(self, window_sec, required_data_len=30):
    self._required_data_len = required_data_len
    self._ohlc_calculator = OhlcCalculator(window_sec=window_sec, maxlen=required_data_len)

  @property
  def window_size(self):
    return self._ohlc_calculator.window_size

  def is_ready(self):
    return len(self._ohlc_calculator.data) == self._required_data_len

  def update(self, timestamp, price):
    self._ohlc_calculator.update(timestamp, price)

  def get_volatility(self, method=VolatilityEstimator.CLOSE_TO_CLOSE):
    if not self.is_ready():
      return None
    return getattr(self, method.value)(self._ohlc_calculator.data)

  def close_to_close(self, ohlc_list):
    close_list = [ohlc.close for ohlc in ohlc_list]
    time_scale = math.sqrt(self.window / 1e9)
    return np.std(np.diff(np.log(close_list))) / time_scale

  def roger_satchell_yoon(self, ohlc_list):
    open_list = []
    high_list = []
    low_list = []
    close_list = []
    for ohlc in ohlc_list:
      open_list.append(ohlc.open)
      high_list.append(ohlc.high)
      low_list.append(ohlc.low)
      close_list.append(ohlc.close)
    open_array = np.array(open_list)
    high_array = np.array(high_list)
    low_array = np.array(low_list)
    close_array = np.array(close_list)

    sigma = np.mean(
        np.log(high_array / open_array) * np.log(high_array / close_array)
        + np.log(low_array / open_array) * np.log(low_array / close_array))
    sigma = np.sqrt(sigma) / math.sqrt(self.window / 1e9)
    return sigma
