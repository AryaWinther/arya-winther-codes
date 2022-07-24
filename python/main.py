"""
Main module for running the Python code defined in Teachers.py
"""
from Teachers import TeacherArya
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

# Define some custom invalid math and art grades for Arya and Jessica.
math_grades = {'Arya': 0, 'Jessica': 7}
student_art_grades = {'Arya': 10, 'Jessica': 11}

# Catch the exception to make sure the program runs, print
# the content of the exception instead.
try:
	teacher3 = TeacherJessica(
		student_math_grades=math_grades,
		student_art_grades=student_art_grades)
except Exception as ex:
	print('\nTeacher 3 could not be instantiated because:', ex)

# Define some custom math, art and science grades for Hakim and Erica.
math_grades = {'Hakim': 8, 'Erica': 9}
student_art_grades = {'Hakim': 9, 'Erica': 10}
student_science_grades = {'Hakim': 10, 'Erica': 7}

# Create a teacher Arya which is their teacher.
teacher_arya1 = TeacherArya(
	student_math_grades=math_grades,
	student_art_grades=student_art_grades,
	student_science_grades=student_science_grades)

# Print the math grades.
print('Math (Teacher Arya):', teacher_arya1.studentMathGrades())

# Print the average grade.
print('Average (Teacher Arya):', teacher_arya1.determineAverageGrade())

# Catch the exception from trying to create a visualization.
try:
	teacher_arya1.generateHtmlVisualization(html_filename='new.html')
except Exception as ex:
	print("""\n Teacher Arya's grades could not be visualized because:""", ex)


