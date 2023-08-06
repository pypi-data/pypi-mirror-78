import torch

from . import Distribution
from .. import util


class LogNormal(Distribution):
    def __init__(self, loc, scale):
        loc = util.to_tensor(loc)
        scale = util.to_tensor(scale)
        super().__init__(name='LogNormal', address_suffix='LogNormal', torch_dist=torch.distributions.LogNormal(loc, scale))

    def __repr__(self):
        return 'LogNormal({}, {})'.format(self.loc.cpu().numpy().tolist(), self.scale.cpu().numpy().tolist())

    @property
    def loc(self):
        return self._torch_dist.loc

    @property
    def scale(self):
        return self._torch_dist.scale
