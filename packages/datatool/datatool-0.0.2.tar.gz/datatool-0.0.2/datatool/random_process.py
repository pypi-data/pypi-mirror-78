# Copyright (c)
# Author: xguo

import math
import itertools
import collections
import numpy as np
import matplotlib.pyplot as plt

from recordclass import recordclass


def get_series(iterator, num):
  s = []
  t = []
  for state in itertools.islice(iterator, 0, num, 1):
    s.append(state.s)
    t.append(state.t)
  return s, t


class RandomProcess(object):
  ParamType = None
  StateType = recordclass('Simple_state', ['s', 't'])

  def __init__(self, param, state):
    self._param = param
    self._state = state

  def __iter__(self):
    return type(self)(self.param, self.state)

  @classmethod
  def create(cls, **kwargs):
    param_kwargs = {key: value for key, value in kwargs.items() if key in cls.ParamType._fields}
    state_kwargs = {key: value for key, value in kwargs.items() if key in ['s', 't']}
    return cls(cls.ParamType(**param_kwargs), cls.StateType(**state_kwargs))

  @property
  def param(self):
    return self._param

  @property
  def state(self):
    return self._state


class GBMotion(RandomProcess):
  ParamType = collections.namedtuple('GBMotion_param', ['mu', 'sigma', 'dt'])

  def __next__(self):
    dw = np.random.normal(loc=0.0, scale=math.sqrt(self.param.dt))
    ds = self.param.mu * self.state.s * self.param.dt + self.param.sigma * self.state.s * dw
    self.state.s += ds
    self.state.t += self.param.dt
    return self.state


# dxt=θ(μ−xt)dt+σdWt
class OUProcess(RandomProcess):
  ParamType = collections.namedtuple('OUProcess_param', ['theta', 'mu', 'sigma', 'dt'])

  def __next__(self):
    dw = np.random.normal(loc=0.0, scale=math.sqrt(self.param.dt))
    ds = self.param.theta * (self.param.mu - self.state.s) * self.param.dt + self.param.sigma * dw
    self.state.s += ds
    self.state.t += self.param.dt
    return self.state


def main():
  from hurst import compute_Hc

  dt = 0.1
  x = GBMotion.create(mu=0.000, sigma=0.02, dt=0.1, s=0.1, t=0)
  # x = OUProcess.create(theta=1, mu=2, sigma=0.01, dt=0.1, s=2, t=0)
  s, t = get_series(x, 10000)
  b = np.diff(np.log(s))
  c1 = np.std(b) / math.sqrt(dt)
  # const = 4*math.log(2)
  const = 1
  c2 = math.sqrt(np.mean(b * b) / const) / math.sqrt(dt)
  print(c1, c2)

  plt.figure()
  plt.plot(t, s, marker='.')
  plt.show()

  H, c, data = compute_Hc(s, kind='random_walk', simplified=False)
  print("H={:.4f}, c={:.4f}".format(H,c))


if __name__ == '__main__':
  main()
