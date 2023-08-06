# Copyright (c) 2020
# Author: xguo

import datetime


def to_prev_mid_night(timestamp) -> datetime.datetime:
  prev_mid_night = datetime.datetime.fromtimestamp(timestamp / 1e9).date()
  prev_mid_night = datetime.datetime.combine(prev_mid_night, datetime.time())
  return prev_mid_night


def to_next_mid_night(timestamp) -> datetime.datetime:
  next_mid_night = to_prev_mid_night(timestamp) + datetime.timedelta(days=1)
  return next_mid_night
