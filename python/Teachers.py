# This example class has been written by Arya Winther,
# 2022.

import matplotlib.pyplot as plt
import numpy
import textwrap

class TeacherJessica(object):

	def __init__(
			self, 
			student_math_grades, 
			student_art_grades=None,
			students_getting_along_matrix=None):
		"""
		This class implements an object called teacher Jessica, which
		takes the names of her students as input, and the
		grades of each students in math and potentially in art. Jessica
		most often teaches mathematics, and sometimes art.

		:param student_math_grades:
			The grade for each student in math. The grade must be an integer
			number between 1 and 10. 
		:type student_math_grades:
			dict of type {str: int}

		param student_art_grades:
			The grade for each student in art. The names must match
			the ones in ```student_math_grades```. By default,
			the grade 8 is given for each student specified
			in ``student_math_grades``.  
			|DEFAULT| ``8`` for each student.
		:type student_art_grades:
			dict of type {str: float}

		:param students_getting_along_matrix:
			A matrix which describes how well each student gets along with each
			other and themselves. The getting-along metric is a float between
			0 and 1: 1 is perfect and 0 not hating each other. The matrix can be given 
			as a full symmetric matrix, or an upper-triangular one.
			|DEFAULT| An upper-triangular matrix with 1's on the diagonal and 0.5 
					  (getting along OK-ish on the off-diagonals).
		:type students_getting_along_matrix:
			```numpy.ndarray``
		"""
		# Check and set the math grades.
		if not isinstance(student_math_grades, dict):
			raise Exception('Invalid type of student_math_grades!')
		self._student_math_grades = student_math_grades

		# Check and set the art grades, if given.
		if student_art_grades is None:
			self._student_art_grades = {name: 8 for name in student_math_grades.keys()}
		else:
			if not isinstance(student_art_grades, dict):
				raise Exception(
					'student_art_grades must be given as a dict with student names as keys and grades as values.')

			# Check that all names match the ones in the math grades.
			names_are_valid = (student_math_grades.keys() == student_art_grades.keys())
			if not names_are_valid:
				raise Exception('Mismatch between the student names for math and art grades.')

			# All good, set the art grades.
			self._student_art_grades = student_art_grades

		self._students_getting_along_matrix = students_getting_along_matrix

	def studentMathGrades(self):
		"""
		:returns:
			The math grades for each student.
		:rtype:
			dict of type {str: int}
		"""
		return self._student_math_grades

	def studentArtGrades(self):
		"""
		:returns:
			The art grades for each student.
		:rtype:
			dict of type {str: int}
		"""
		return self._student_art_grades

	def studentsGettingAlongMatrix(self):
		return self._students_getting_along_matrix

	def studentNames(self):
		""" 
		:returns:
			The names of all students:
		:rtype:
			list of str
		"""
		return list(self.studentMathGrades().keys())

	def determineAverageGrade(self, weights=None):
		"""
		Method for calculating the average grade for each student, taking a
		weighted average between math and art, according to the given
		```weights.``
		"""
		if weights is None:
			weights_array = numpy.array([0.5, 0.5])
		else:
			weights_array = numpy.array(weights)

		# Fetch the math and art grades.
		math_grades_dict = self.studentMathGrades()
		art_grades_dict = self.studentArtGrades()

		# Calculate the average grade for each student and return it.
		# First gather the math and art grades of each student in a list
		# of tuples.
		grades_math_art = [
			(math_grade, art_grade) for math_grade, art_grade in zip(
				math_grades_dict.values(), art_grades_dict.values())
		]

		# Then calculate the average grades using the given weights. Using
		# numpy is unnecessary here performance-wise, but let's use it for 
		# demonstrative purposes.
		average_grades = {
			student_name: numpy.average(numpy.array(grades), weights=weights)
			for student_name, grades in zip(math_grades_dict.keys(), grades_math_art)
		}

		return average_grades

	def calculateTeacherSuccess(self):
		"""
		Method for calculating how successful the teacher has been with her
		students. The Frobenius norm of the ```students_getting_along_matrix``
		is used as the metric to determine teacher success: the closer to 1,
		the better. The returned success value is in percentages.

		:returns:
			The success of the teacher, i.e. how happy the students are about themselves
			and each other.
		:rtype:
			float
		"""
		# Determine the initial success for taking the Fro-norm of the
		# students getting along matrix.
		students_getting_along_norm = numpy.linalg.norm(
			self.studentsGettingAlongMatrix())

		# Normalize it according to the number of students, multiply by 100
		# to convert to percentages, and round to include 2 decimals only.
		students_getting_along_norm /= len(self.studentNames())
		students_getting_along_norm = numpy.round(100 * students_getting_along_norm, decimals=2)

		return students_getting_along_norm

	def generateHtmlVisualization(
			self, 
			html_filename,
			show_grades_image=False):
		"""
		Method for generating a visualization of the student grades as an
		image in an html file.

		:param html_filename:
			The name of the generated html file name.
		:type html_filename:
			str

		:param show_grades_image:
			Whether the visualization of the grades will also be shown on
			the screen. Note that the html file is not generated, until the
			image is closed.
			|DEFAULT| False
		:type show_grades_images:
			bool
		"""
		# Fetch names and grades.
		student_names = self.studentNames()
		math_grades = list(self.studentMathGrades().values())
		art_grades = list(self.studentArtGrades().values())
		  
		# Set up the x axis and create a bar plot with both grades
		# shown for each student.
		x_axis = numpy.arange(len(student_names))
		plt.bar(x_axis - 0.2, math_grades, 0.4, label = 'Math')
		plt.bar(x_axis + 0.2, art_grades, 0.4, label = 'Art')
		  
		# Set up the ticks, labels and a legend.
		plt.xticks(x_axis, student_names, fontsize=14)
		plt.yticks(fontsize=14)
		plt.xlabel("Student", fontsize=18)
		plt.ylabel("Grade", fontsize=18)
		plt.legend(fontsize=14, loc='upper center')

		# Set limit to 1 to 10 + a little extra.
		plt.ylim(1.0, 10.1)

		# Save it and fetch the figure dimensions in pixels.
		plt.savefig('grades.png', dpi=200)
		fig = plt.gcf()
		fig_width, fig_height = fig.get_size_inches() * fig.dpi

		# If requested, show the image.
		if show_grades_image:
			plt.show()

		# Define a html template and add the correct figure dimensions.
		html_image = textwrap.dedent("""\
			<html>
			<head>
			<title>Grades of Jessica's students</title>
			</head>
			<body>
			<h2>Visualization of grades</h2>
			  
			<img src="grades.png" alt="Grades" width="{}" height="{}">
			  
			</body>
			</html>""").format(fig_width, fig_height)

		# Write the image to the given html file.
		with open(html_filename, 'w') as f:
			f.write(html_image)

	@staticmethod
	def wiseQuotes():
		"""
		:returns:
			Wise quotes from different philosophers, ones that teacher
			Jessica is very fond of.
		:rtype:
			dict of type {str: str}
		"""
		# Hard-coded here a few different ones from Confucius, Plato and 
		# the Sage in Tao Te Ching from Lao Tzu.
		wise_quotes_initial = {
			'Confucius': 'If you make a mistake and do not correct it, that is called a mistake',
			'Plato': 'I am the wisest man alive, for I know one thing, and that is that I know nothing',
			'Sage in Tao Te Ching': 'True greatness is to not seek greatness'
		}

		# Format the wise quotes from the philosophers in a nicer, presentable way.
		names = list(wise_quotes_initial.keys())
		quotes = list(wise_quotes_initial.values())
		wise_quotes_final = textwrap.dedent("""\

			The wise quotes here are from the following philosophers: %s.

			%s""") % (', '.join(names), '.\n\n'.join(quotes)) + '.'

		return wise_quotes_final

