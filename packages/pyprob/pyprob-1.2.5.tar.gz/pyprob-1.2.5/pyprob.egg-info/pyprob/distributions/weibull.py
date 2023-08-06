import torch

from . import Distribution
from .. import util


class Weibull(Distribution):
    def __init__(self, scale, concentration):
        scale = util.to_tensor(scale)
        concentration = util.to_tensor(concentration)
        super().__init__(name='Weibull', address_suffix='Weibull', torch_dist=torch.distributions.Weibull(scale=scale, concentration=concentration))

    def __repr__(self):
        return 'Weibull(scale={}, concentration={})'.format(self.scale.cpu().numpy().tolist(), self.concentration.cpu().numpy().tolist())

    @property
    def concentration(self):
        return self._torch_dist.concentration

    @property
    def scale(self):
        return self._torch_dist.scale
