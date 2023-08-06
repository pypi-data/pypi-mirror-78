import torch

from . import Distribution
from .. import util


class VonMises(Distribution):
    def __init__(self, loc, concentration):
        loc = util.to_tensor(loc)
        concentration = util.to_tensor(concentration)
        super().__init__(name='VonMises', address_suffix='VonMises', torch_dist=torch.distributions.VonMises(loc, concentration))

    def __repr__(self):
        return 'VonMises(loc={}, concentration={})'.format(self.loc.cpu().numpy().tolist(), self.concentration.cpu().numpy().tolist())

    @property
    def loc(self):
        return self._torch_dist.loc

    @property
    def concentration(self):
        return self._torch_dist.concentration
