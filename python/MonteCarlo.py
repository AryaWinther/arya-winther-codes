""" Module implementing a class which can be used to calculate various things used Monte Carlo-methods """

import math
import numpy


class MonteCarlo(object):

	def __init__(self, sample_size=None, seed=None):
		"""
		A class which can calculate various things using Monte Carlo-based
		methods.

		:param sample_size:
			The size of the sampling used for the Monte-Carlo estimates.
		:type sample_size:
			int

		:param seed:
			The seed for the random number generator.
			|DEFAULT| No seed, always fresh numbers.
		:type seed:
			None | int
		"""
		self._sample_size = sample_size
		self._seed = seed

		self._random_number_generator = numpy.random.default_rng(seed)

	def setSampleSize(self, sample_size):
		"""
		Change the sample simple in the Monte Carlo estimate.

		:param sample_size:
			The new sample size:
		:type sample_size:
			int
		"""
		self._sample_size = sample_size

	def errorEstimate(self):
		"""
		:returns:
			An error estimate for the Monte Carlo estimate, it is propotial to 1 / sqrt(N).
		:rtype:
			float
		"""
		return 1 / numpy.sqrt(self._sample_size)

	def calculateCoinTossProbability(self, heads=True):
		"""
		Calculate the probability of a coin toss. Heads or tails.
		"""
		# Calculate random numbers between 0 and 1.
		random_vector = self._random_number_generator.random(self._sample_size)

		if heads:
			probability = len(numpy.where(random_vector > 0.5)[0]) / self._sample_size
		else:
			probability = len(numpy.where(random_vector <= 0.5)[0]) / self._sample_size

		return probability

	def sphereInsideCubeRatio(self):
		"""
		Calculate the ratio of the volume of the sphere vs the volume of
		the cube using Monte-Carlo. The side length of the cube is assumed to
		be the same as the radius of the sphere.

		:returns:
			The Monte-Carlo estimate for the ratio and the exact answer.
		:rtype:
			tuple of (float, float)
		"""
		# Utility for checking if the given coordinates are inside a unit sphere.
		sphere_radius = 0.5
		def isInsideSphere(coordinates):
			center_point = numpy.array([0.5] * 3)
			distance_to_center = numpy.linalg.norm(center_point - coordinates)
			return distance_to_center <= sphere_radius

		# Assume unit radius.
		coordinates_list = self._random_number_generator.random((self._sample_size, 3))
		is_inside_sphere_points = len([
			coordinates for coordinates in coordinates_list if isInsideSphere(coordinates)])
		ratio = is_inside_sphere_points / self._sample_size

		# The reference ration (unit cube volume is 1).
		ref_ratio = 4 * math.pi / 3.0 * sphere_radius**3.0
		relative_error = abs((ratio - ref_ratio) / ref_ratio)

		return ratio, relative_error

	def gaussianIntegral(self, cutoff_value=3.0):
		"""
		Estimate the value of the Gaussian integral exp(-x^2 -y^2) from -inf to + inf,
		using Monte-Carlo techniques.

		:param cutoff_value:
			The x and y axis absolute max value, beyond which numbers will not be sampled anymore.
		:type cutof_value:
			float

		:returns:
			An estimate for the integral using Monte Carlo, and the relative error
			wrt the exact result: Pi.
		:rtype:
			tuple
		"""
		# Generate a list of random values from [-v_cut, v_cut] along both x
		# and y axis.
		rectangle_width = 2 * cutoff_value
		random_xy_values = [
			rectangle_width * (
				self._random_number_generator.random(self._sample_size) - 0.5)
			for _ in range(2)
		]

		# An estimate for the integral can be obtained be calculated the
		# average over all the rectangular cuboids with f(x, y) as the height.
		volume_values = (
			rectangle_width**2.0 * numpy.exp(-random_xy_values[0]**2.0) * 
			numpy.exp(-random_xy_values[1]**2.0)
		)
		integral = numpy.average(volume_values)

		# Determine the relative error wrt exact answer.
		relative_error = abs((integral - math.pi) / math.pi)

		return integral, relative_error

# Define a seed. Then the result will not change very time when this is run.
seed = 7

# Create a Monte Carlo object.
monte_carlo = MonteCarlo(sample_size=10000, seed=7)

print('Heads probability in coin toss:', monte_carlo.calculateCoinTossProbability())
print('Monte Carlo estimate + error:', monte_carlo.sphereInsideCubeRatio())
print('Monte Carlo, Gaussian integral + error', monte_carlo.gaussianIntegral())
print('Monte Carlo, Gaussian integral, large cutoff + error', monte_carlo.gaussianIntegral(cutoff_value=100))

# Increase sample size. Accuracy should've increased.
monte_carlo.setSampleSize(10**7)
print('Error estimate:', monte_carlo.errorEstimate())
print('Monte Carlo, Gaussian integral + error', monte_carlo.gaussianIntegral())
print('Coin toss:', monte_carlo.calculateCoinTossProbability(heads=False))
