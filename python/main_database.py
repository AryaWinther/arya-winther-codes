"""
Main module for running the Python code defined in TeachersDataBase.py
"""
from Teachers import TeacherArya
from Teachers import TeacherJessica
from TeachersDataBase import TeachersDataBase
import numpy

# Define some custom math and art grades for Arya and Jessica.
math_grades = {'Arya': 6, 'Jessica': 7}
student_art_grades = {'Arya': 10, 'Jessica': 7}
getting_along_jessica = 0.7 * numpy.ones((2, 2))
teacher_jessica = TeacherJessica(
	student_math_grades=math_grades,
	student_art_grades=student_art_grades,
	students_getting_along_matrix=getting_along_jessica)

# Define some custom math, art and science grades for Hakim and Erica.
math_grades = {'Hakim': 8, 'Erica': 9}
student_art_grades = {'Hakim': 9, 'Erica': 10}
student_science_grades = {'Hakim': 10, 'Erica': 7}

# Create a teacher Arya which is their teacher.
getting_along_arya = 0.5 * numpy.ones((2, 2))
teacher_arya = TeacherArya(
	student_math_grades=math_grades,
	student_art_grades=student_art_grades,
	student_science_grades=student_science_grades,
	students_getting_along_matrix=getting_along_arya)

# Set up a teacher database. First only add Jessica.
teachers_database = TeachersDataBase(teachers=[teacher_jessica], teacher_ids=['teacher1'])

# Use the add method to add Arya.
teachers_database.addTeacher(teacher_id='teacher2', teacher=teacher_arya)

# Print info.
teachers_database.reportInfo()

# Save and load and print info again.
teachers_database.saveToFile(json_filename='teachers_database1.json')
teachers_database.populateFromFile('teachers_database1.json')
teachers_database.reportInfo()


