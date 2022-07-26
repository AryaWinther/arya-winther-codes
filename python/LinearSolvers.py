""" This module implements methods for solving linear matrix equations """

import numpy


class LinearSolvers(object):

	def __init__(
			self, 
			iterative_solver_tolerance=1e-8,
			direct_inverse_cholesky=True):
		"""
		A class which can solve the linear matrix equation defined by the
		given lhs_matrix A and rhs_vector b, Ax = b. The class can either
		solve it by direct inversion, or the conjugate gradient method.
		The latter method only works for matrices which are symmetric
		and positive definite.

		:param iterative_solver_tolerance:
			The absolute tolerance for the iterative solver, at which the
			iteration will be terminated.
		:type iterative_solver_tolerance:
			float

		:param direct_inverse_cholesky:
			Whether a Choleskly decomposition will be used for the direct inversion,
			if possible.
		:type direct_inverse_cholesky:
			bool
		"""
		self._iterative_solver_tolerance = iterative_solver_tolerance
		self._direct_inverse_cholesky = direct_inverse_cholesky

	def directInverseCholesky(self):
		""":
		:returns:
			Whether a Choleskly decomposition will be used for the direct inversion,
			if possible.
		:rtype:
			bool
		"""
		return self._direct_inverse_cholesky

	def directInverseCholesky(self):
		""":
		:returns:
			Whether a Choleskly decomposition will be used for the direct inversion,
			if possible.
		:rtype:
			bool
		"""
		return self._direct_inverse_cholesky

	def solveDirectInverse(self, lhs_matrix, rhs_vector):
		"""
		Method for solving the linear equation Ax = b. If the cholesky
		flag has been set to True, the method first checks whether it
		is possible to use the more efficient Cholesky decomposition 
		method to solve the problem.

		:param lhs_matrix:
			The left-hand matrix A.
		:type lhs_matrix:
			``numpy.ndarray`` which represents a square matrix.

		:param rhs_vector:
			The right-hand side vector b.
		:type rhs_vector:

		:returns:
			The solution, accurate up to the iteration tolerance.
		:rtype:
			``numpy.ndarray``
		"""
		# Attempt to perform a Cholesky decomposition for the input matrix. If
		# the matrix is not positive definite, this will raise an exception.
		cholesky_L = None
		try:
			cholesky_L = numpy.linalg.cholesky(lhs_matrix)
		except numpy.linalg.LinAlgError:
			pass

		# Check whether we can use cholesky.
		use_cholesky = (cholesky_L is not None and self.directInverseCholesky())

		if use_cholesky:
			# We already have the decomposition; thus solve L y = b for y first.
			y = numpy.linalg.solve(cholesky_L, rhs_vector)

			# Then L^T x = y for x.
			solution_vector = numpy.linalg.solve(numpy.transpose(cholesky_L), y)
		else:
			# Simply solve directly.
			solution_vector = numpy.linalg.solve(lhs_matrix, rhs_vector)

		return solution_vector

	def _checkCholesky(self, lhs_matrix):
		""" """
		"""
		Utility method for checking whether a Choleskly decomposition is possible.
		"""
		# Attempt to perform a Cholesky decomposition for the input matrix. If
		# the matrix is not positive definite, this will raise an exception.
		lhs_matrix_valid = True
		try:
			numpy.linalg.cholesky(lhs_matrix)
		except numpy.linalg.LinAlgError:
			lhs_matrix_valid = False

		return lhs_matrix_valid

	def solveGradientDescent(self, lhs_matrix, rhs_vector):
		"""
		Method for solving the linear equation Ax = b using the
		a simple gradient descent method.

		:param lhs_matrix:
			The left-hand matrix A.
		:type lhs_matrix:
			``numpy.ndarray`` which represents a square matrix.

		:param rhs_vector:
			The right-hand side vector b.
		:type rhs_vector:
			``numpy.ndarray``

		:returns:
			The solution, accurate up to the iteration tolerance.
		:rtype:
			``numpy.ndarray``
		"""
		lhs_matrix_valid = self._checkCholesky(lhs_matrix)
		if not lhs_matrix_valid:
			raise Exception(
				'lhs_matrix must be symmetric and positive definite for the descent method.')

		# Start with an random initial guess.
		dimension = len(rhs_vector)
		previous_solution = numpy.random.uniform(low=0.0, high=1.0, size=(dimension,))

		# Run the steepest descent iteration.
		max_iterations = 20
		for _ in range(max_iterations):
			direction = rhs_vector - numpy.dot(lhs_matrix, previous_solution)
			lhs_matrix_times_d = numpy.dot(lhs_matrix, direction)
			alpha = numpy.dot(direction, direction) / numpy.dot(
				direction, lhs_matrix_times_d)

			# Update the solution, x_{k + 1} = x_k + \alpha_k d_k.
			solution = previous_solution + alpha * direction
			
			error = numpy.linalg.norm(solution - previous_solution)

			# Stop if converged enough.
			if numpy.linalg.norm(error) < self._iterative_solver_tolerance:
				break

			# Update the previous solution for the next iteration.
			previous_solution = solution[:]

		return solution

	def solveConjugateGradient(self, lhs_matrix, rhs_vector):
		"""
		Method for solving the linear equation Ax = b using the
		conjugate gradient iterative method. The input matrix must be symmetrix
		and positive definite.

		:param lhs_matrix:
			The left-hand matrix A.
		:type lhs_matrix:
			``numpy.ndarray`` which represents a square matrix.

		:param rhs_vector:
			The right-hand side vector b.
		:type rhs_vector:

		:returns:
			The solution, accurate up to the iteration tolerance.
		:rtype:
			``numpy.ndarray``
		"""
		# Stop if the input matrix isn't valid for CG.
		lhs_matrix_valid = self._checkCholesky(lhs_matrix)
		if not lhs_matrix_valid:
			raise Exception('lhs_matrix must be symmetric and positive definite for the CG method.')

		# Start with an random initial guess.
		dimension = len(rhs_vector)
		previous_solution = numpy.random.uniform(low=0.0, high=1.0, size=(dimension,))

		previous_residual = rhs_vector - numpy.dot(lhs_matrix, previous_solution)
		p_vector = numpy.array(previous_residual)

		# Run the conjugate gradient.
		max_iterations = 20
		for _ in range(max_iterations):
			lhs_matrix_times_p = numpy.dot(lhs_matrix, p_vector)
			alpha = numpy.dot(previous_residual, previous_residual) / numpy.dot(p_vector, lhs_matrix_times_p)

			# Update solution and residual according to CG scheme.
			solution = previous_solution + alpha * p_vector
			residual = previous_residual - alpha * lhs_matrix_times_p

			if numpy.linalg.norm(residual) < self._iterative_solver_tolerance:
				break

			# Update p vector.
			beta = numpy.dot(residual, residual) / numpy.dot(previous_residual, previous_residual)
			p_vector = residual + beta * p_vector

			# Update the previous solution and residual for the next iteration.
			previous_residual = residual[:]
			previous_solution = solution[:]

		return solution

# Define matrix dimension and reate an identity matrix first.
dimension = 25
A = numpy.eye(dimension)

# Make it tridiagonal but still diagonally dominent (to keep it positive def.).
for index in range(23):
	A[index, index + 1] = 0.1 * numpy.random.uniform(low=0.0, high=1.0, size=(1,))
	A[index + 1, index] = A[index, index + 1]

# Random vector as b.
b = numpy.random.uniform(low=0.0, high=1.0, size=(dimension,))

# Create a solvers object and solve the problem using direct inverse w/ Cholesky
# decomposition and then CG and gradient descent method.
solvers = LinearSolvers(
	direct_inverse_cholesky=True, 
	iterative_solver_tolerance=1e-10)
solution_direct_cholesky = solvers.solveDirectInverse(A, b)
solution_cg = solvers.solveConjugateGradient(A, b)
solution_descent = solvers.solveGradientDescent(A, b)

ref_solution = numpy.linalg.solve(A, b)

print('CG vs ref', numpy.linalg.norm(ref_solution - solution_cg))
print('Gradient vs ref', numpy.linalg.norm(ref_solution - solution_descent))
print('Direct cholesky vs ref', numpy.linalg.norm(ref_solution - solution_direct_cholesky))

		
