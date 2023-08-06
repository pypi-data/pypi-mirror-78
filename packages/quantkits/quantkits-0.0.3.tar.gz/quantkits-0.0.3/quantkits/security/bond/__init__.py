# -*- coding: utf-8 -*-
# @Time    : 29/4/2020 11:20 AM
# @Author  : Joseph Chen
# @Email   : josephchenhk@gmail.com
# @FileName: __init__.py.py
# @Software: PyCharm

import pandas as pd
from datetime import datetime
from scipy.optimize import fsolve

from quantkits.security import Security
from quantkits.time.conversion import from_timeperiod_to_relativedelta


class Bond(Security):
    """Bond with essential features"""
    N: int
    IY: float
    PMT: float
    FV: float
    PV: float
    variables = ("N", "IY", "PMT", "FV", "PV", "tenor", "issued_date", "maturity_date")
    def __init__(self, **kwargs):
        for var in self.variables:
            if kwargs.get(var) is not None:
                setattr(self, var, kwargs.get(var))

    def _PV(self, PMT, IY, FV, N):
        """"""
        PV = 0
        for n in range(1,N+1):
            PV += PMT / (1 + IY*0.01) ** n
        PV += FV / (1 + IY*0.01) ** n
        return PV

    def __getattr__(self, item):
        """"""
        # >> > x = Symbol('x')
        # >> > solve(x ** 2 - 1, x)
        if item not in self.variables:
            return None
        elif item=="PV":
            return self._PV(PMT=self.PMT, IY=self.IY, FV=self.FV, N=self.N)
        elif item=="PMT":
            return fsolve(lambda x: self._PV(PMT=x, IY=self.IY, FV=self.FV, N=self.N)-self.PV, 0)[0]
        elif item=="IY":
            return fsolve(lambda x: self._PV(PMT=self.PMT, IY=x, FV=self.FV, N=self.N)-self.PV, 0)[0]
        elif item=="FV":
            return fsolve(lambda x: self._PV(PMT=self.PMT, IY=self.IY, FV=x, N=self.N)-self.PV, 0)[0]
        elif item=="N":
            return fsolve(lambda x: self._PV(PMT=self.PMT, IY=self.IY, FV=self.FV, N=x)-self.PV, 0)[0]

    def __str__(self):
        return f"Bond[{self.__dict__}]"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    __repr__=__str__


def get_all_coupon_dates(bond:Bond, freq:str="6M")->list:
    """Given a bond, and its coupon frequency, we obtain all coupon dates"""
    delta = from_timeperiod_to_relativedelta(period=freq)
    coupon_dates = []
    coupon_date = bond.issued_date + delta
    while coupon_date<=bond.maturity_date:
        coupon_dates.append(coupon_date)
        coupon_date += delta
    if coupon_dates[-1]!=bond.maturity_date:
        coupon_dates.append(bond.maturity_date)
    return coupon_dates

def get_next_coupon_date(cur_date:datetime, all_coupon_dates:list)->datetime:
    """Given current date, get next coupon date"""
    if cur_date>all_coupon_dates[-1]:
        return None
    elif cur_date<all_coupon_dates[0]:
        return all_coupon_dates[0]
    else:
        for coupon_date in all_coupon_dates:
            if coupon_date>=cur_date:
                return coupon_date

def get_previous_coupon_date(cur_date:datetime, all_coupon_dates:list)->datetime:
    """Given current date, get previous coupon date"""
    if cur_date<all_coupon_dates[0]:
        return None
    elif cur_date>all_coupon_dates[-1]:
        return all_coupon_dates[-1]
    else:
        for coupon_date in all_coupon_dates:
            if coupon_date<cur_date:
                return coupon_date

def get_number_of_future_coupon_dates(next_coupon_date:datetime, all_coupon_dates:list)->int:
    """Count coupon dates on or after next coupon date"""
    return sum(c >= next_coupon_date for c in all_coupon_dates)

def adjust_pv_to_current_date(cur_time:datetime, bond:Bond, data:pd.Series)->float:
    """adjust bond price to current date"""
    if cur_time >= bond.maturity_date:
        pv = 100
    elif bond.tenor <= 12:  # Treasury Bill
        remaining_period = (bond.maturity_date - cur_time).days / (bond.maturity_date - bond.issued_date).days
        pv = 100 / (1 + data[bond.tenor] * 0.01) ** (remaining_period)
    else:  # Treasury Note/Bond (default semi-annual payments)
        all_coupon_dates = get_all_coupon_dates(bond, freq="6M")
        next_coupon_date = get_next_coupon_date(cur_time, all_coupon_dates)
        number_of_future_coupon_dates = get_number_of_future_coupon_dates(next_coupon_date, all_coupon_dates)
        # pv at next coupon date
        pv = Bond(N=number_of_future_coupon_dates - 1,  # exclude next coupon date
                  IY=data[bond.tenor] * 6 / 12,
                  PMT=bond.PMT,
                  FV=100,
                  tenor=bond.tenor,
                  issued_date=bond.issued_date,
                  maturity_date=bond.maturity_date).PV
        # Discount to current date (clean price)
        previous_coupon_date = get_previous_coupon_date(cur_time, all_coupon_dates)
        period_start = previous_coupon_date if previous_coupon_date else bond.issued_date
        remaining_period = (next_coupon_date - cur_time).days / (next_coupon_date - period_start).days
        pv = (pv + bond.PMT) / (1 + data[bond.tenor] * 0.01 * 6 / 12) ** (remaining_period)

        # Accrued interest, Assume deposit in cash (do not reinvest)
        accrued_interest = bond.PMT * (len(all_coupon_dates) - number_of_future_coupon_dates)

        # dirty price
        pv += accrued_interest
    return pv