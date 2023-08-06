import skopt
from skopt.space import Real, Categorical, Integer

from hpogrid.search_space.base_space import BaseSpace

class SkOptSpace(BaseSpace):

	def __init__(self, search_space = None):
		self.library = 'skopt'
		super().__init__(search_space)	
		

	def reset_space(self):
		self.search_space = []

	def append(self, space_value):
		self.search_space.append(space_value)

	def categorical(self, label, categories, grid_search = False):
		if grid_search != False:
			raise ValueError('{} does not allow grid search'.format(self.library))
		return Categorical(name=label, categories=categories)

	def uniformint(self, label, low, high):
		return Integer(name=label, low=low, high=high, prior="uniform")

	def uniform(self, label, low, high):
		return Real(name=label, low=low, high=high, prior='uniform')

	def loguniform(self, label, low, high, base=10):
		return Real(name=label, low=low, high=high, prior='log-uniform', base=base)

	def loguniformint(self, label, low, high, base=10):
		return Integer(name=label, low=low, high=high, prior="log-uniform", base=base)

	def fixed(self, label, value):
		return self.categorical(label=label, categories=[value])