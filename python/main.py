"""
Main module for running the Python code defined in Teachers.py
"""
from Teachers import TeacherJessica
import numpy

# Define some custom math and art grades for Arya and Jessica.
math_grades = {'Arya': 6, 'Jessica': 7}
student_art_grades = {'Arya': 10, 'Jessica': 7}
teacher_erica = TeacherJessica(
	student_math_grades=math_grades,
	student_art_grades=student_art_grades)

# Print them, and also the calculated average grade.
weights = [0.1, 0.9]
print('Math grades:', teacher_erica.studentMathGrades())
print('Art grades:', teacher_erica.studentArtGrades())
print('Average grades (weights [{}, {}]):'.format(weights[0], weights[1]), 
	teacher_erica.determineAverageGrade(weights=[0.1, 0.9]))

# Don't specify art and leave weights to default. Now Jessica should
# have a better average than Arya. Also specify a getting along matrix.
# Arya likes herself more than Jessica, hence a higher value on the diagonal.
getting_along_matrix = numpy.array([[0.8, 0.7], [0, 0.6]])
teacher2 = TeacherJessica(
	student_math_grades=math_grades,
	students_getting_along_matrix=getting_along_matrix)
print('Average grades (default art grades): ', teacher2.determineAverageGrade())

# Print the successs.
print('Teacher success (%):', teacher2.calculateTeacherSuccess())

# Print the wise quotes from the philosophers. This is a static method, since
# all teachers named Jessica have the same philosophy.
print(TeacherJessica.wiseQuotes())

# Generate a visualization in an html file. Also show the visualization on screen.
teacher2.generateHtmlVisualization(
	html_filename='test.html',
	show_grades_image=True)