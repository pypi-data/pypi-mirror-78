import torch

from . import Distribution
from .. import util


class Gamma(Distribution):
    def __init__(self, concentration, rate):
        concentration = util.to_tensor(concentration)
        rate = util.to_tensor(rate)
        super().__init__(name='Gamma', address_suffix='Gamma', torch_dist=torch.distributions.Gamma(concentration=concentration, rate=rate))

    def __repr__(self):
        return 'Gamma(concentration={}, rate={})'.format(self.concentration.cpu().numpy().tolist(), self.rate.cpu().numpy().tolist())

    @property
    def concentration(self):
        return self._torch_dist.concentration

    @property
    def rate(self):
        return self._torch_dist.rate
