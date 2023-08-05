from abc import ABC
from copy import deepcopy
import numpy as np
from collections import OrderedDict


class DistMachine(object):

    # This is a state engine that has a ppf function
    # Example of usage: SequentialStreamCrawler

    def __init__(self, state, params: OrderedDict = None):
        self.params = params
        self.state = state

    def update(self, value=None, dt=None, **kwargs):
        # Incorporate new value, time passing, or both
        # Typically will update the state but not params
        raise NotImplementedError

    def inv_cdf(self, p: float) -> float:
        # Something like StatsConventions.norminv(p)
        raise NotImplementedError


class LossDist(DistMachine):

    # A distribution machine with a loss function

    def __init__(self, state: dict, params: OrderedDict = None):
        super().__init__(state=state, params=params)

    def log_likelihood(self, value: float) -> float:
        """ Likelihood for one value """
        raise NotImplementedError

    # Likelihood Distribution Machine comes with a default loss function, though you could
    # choose to augment or override this by adding other penalties (for instance adding penalty
    # for moving too much)

    def loss(self, lagged_values, lagged_times, params):
        """ Loss function for a series of values """
        # Lower the better
        saved_params = deepcopy(self.params)
        self.params = deepcopy(params)
        chronological_values = list(reversed(lagged_values))
        chronological_times = list(reversed(lagged_times))
        chronological_dt = [1.0] + list(np.diff(chronological_times))

        ll = 0.0
        for value, dt in zip(chronological_values, chronological_dt):
            self.update(dt=dt)
            ll += -self.log_likelihood(value=value)
            self.update(value=value)
        self.params = saved_params
        return ll
