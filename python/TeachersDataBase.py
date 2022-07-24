# This example class has been written by Arya Winther,
# 2022.

""" Module implementing a database of teachers in a school """

import json
import numpy
import textwrap

from Teachers import TeacherArya
from Teachers import TeacherJessica


class TeachersDataBase(object):

	def __init__(self, teachers, teacher_ids):
		"""
		This class implements an object which is a database of teachers.
		It takes a list of teachers as input, and is able to determine 
		and report different types of information about the teachers.
		Teachers and also be added and removed from the database. Each
		teacher must be given a unique ID.

		:param teachers:
			A list of teachers to be added into the database. 
		:type student_math_grades:
			list of :class:`TeacherJessica` | :class:`TeacherArya`

		:param teacher_ids:
			A list of strings which uniquely identify each teacher.
		:type teacher_ids:
			list of str
		"""
		# Set up a dictionary which contains teacher IDs as keys and the teacher
		# objects as values.
		self._teachers_and_ids = {
			teacher_id: teacher for teacher_id, teacher in zip(teacher_ids, teachers)
		}

	def retrieveTeacher(self, teacher_id):
		"""
		:returns:
			The teacher corresponding to the given ID if found in the database,
			None otherwise.
		:rtype:
			None | :class:`TeacherJessica` | :class`TeacherArya`
		"""
		return self._teachers_and_ids[teacher_id] if teacher_id in self._teachers_and_ids.keys() else None

	def addTeacher(self, teacher_id, teacher):
		"""
		A method for adding a teacher to the database.

		:param teacher_id:
			An ID that uniquely determines the teacher.
		:type teacher_id:
			str

		:param teacher:
			The teacher to add to the database.
		:type teacher:
			:class:`TeacherJessica` | :class:`TeacherArya`
		"""
		if teacher_id in self._teachers_and_ids.keys():
			raise Exception('The given teacher ID is already in use.')

		if not isinstance(teacher, (TeacherJessica, TeacherArya)):
			raise Exception('Teacher must be an instance of either TeacherJessica or TeacherArya.')

		# All good, add to the database.
		self._teachers_and_ids[teacher_id] = teacher

	def removeTeacher(self, teacher_id):
		"""
		A method for removing a teacher from the database.

		:param teacher_id:
			An ID that uniquely determines the teacher to remove.
		:type teacher_id:
			str
		"""
		if teacher_id not in self._teachers_and_ids.keys():
			raise Exception('The given teacher ID is not in the database.')

		del self._teachers_and_ids[teacher_id]

	def numberOfEntries(self):
		"""
		:returns:
			The number of teacher entries in the database.
		:rtype:
			int
		"""
		return len(self._teachers_and_ids)

	def determineSuccessAverage(self):
		"""
		:returns:
			The average success rate of the teachers in the database.
		:rtype:
			float
		"""
		teachers = list(self._teachers_and_ids.values())
		teacher_successes = [teacher.calculateTeacherSuccess() for teacher in teachers]
		average_success_rate = sum(
			[teacher.calculateTeacherSuccess() for teacher in teachers]) / len(teachers)

		return average_success_rate

	def determineSuccessStandardDeviation(self):
		"""
		:returns:
			The standard deviation of the success rate of the teachers.
		:rtype:
			float
		"""
		teachers = list(self._teachers_and_ids.values())
		success_rates = numpy.array([teacher.calculateTeacherSuccess() for teacher in teachers])
		
		return numpy.std(success_rates)

	def totalNumberOfStudents(self):
		"""
		:returns:
			The total number of students across all teachers.
		:rtype:
			int
		"""
		students_per_teacher = [len(teacher.studentNames()) for teacher in self._teachers_and_ids.values()]
		return int(sum(students_per_teacher))

	def reportInfo(self):
		""" 
		A method for reporting all the information about the teachers in the database.
		"""

		# Determine the number of teachers and total number of students.
		number_of_teachers = len(self._teachers_and_ids)
		total_number_of_students = self.totalNumberOfStudents()
		average_students_per_teacher = numpy.round(
			total_number_of_students / number_of_teachers, decimals=2)

		# Determine the average success and std deviation.
		average_success_rate = self.determineSuccessAverage()
		success_std_deviation = self.determineSuccessStandardDeviation()

		# Create a database info template and fill it.
		info = textwrap.dedent("""\
			Summary of the teachers database.

			Number of teachers in the database: {}
			Average number of students per teacher: {}
			Number of students in total: {}

			Average success rate of the teachers: {} %
			Standard deviation of success rate: {} 
			"""
		).format(
			number_of_teachers, 
			average_students_per_teacher,
			total_number_of_students, 
			average_success_rate,
			success_std_deviation)

		print(info)

	def saveToFile(self, json_filename):
		"""
		Method for writing the contents of the database to a JSON file. The
		data of the database is stored in dicts which have the following format:

		{
			teacherid1: {
				"teacher_type": 'TeacherArya',
				"names": ['Jaxx', 'Thomas'],
				"math_grades": [7, 8],
				"art_grades": [9, 10],
				"science_grades": [6, 7],
			},

			teacherid2: {
				"teacher_type": 'TeacherJessica',
				"names": ['Colin', 'Nadine'],
				"math_grades": [7, 8],
				"art_grades": [9, 10],
				"science_grades": [],
			},
		}
		"""
		# Initialize the dict to be stored in the JSON file.
		json_dict = {}

		# Loop through the teacher Ids.
		for teacher_id, teacher in self._teachers_and_ids.items():
			# Initialize the dict for this teacher.
			teacher_info_dict = {}

			# Fetch all the parameters.
			teacher_name = type(teacher).__name__
			student_names = teacher.studentNames()
			math_grades = teacher.studentMathGrades()
			art_grades = teacher.studentArtGrades()
			getting_along_matrix = teacher._studentsGettingAlongMatrix().tolist()

			# Fetch science grades if Arya, else empty list.
			science_grades = (
				teacher.studentScienceGrades() if isinstance(teacher, TeacherArya) else [])

			# Populate the dict.
			teacher_info_dict['teacher_type'] = teacher_name
			teacher_info_dict['names'] = student_names
			teacher_info_dict['math_grades'] = math_grades
			teacher_info_dict['art_grades'] = art_grades
			teacher_info_dict['science_grades'] = science_grades
			teacher_info_dict['students_getting_along_matrix'] = getting_along_matrix

			# Add to the json dict.
			json_dict[teacher_id] = teacher_info_dict

		# Write to the file.
		with open(json_filename, 'w') as f:
			json.dump(json_dict, f, indent=4)

	def populateFromFile(self, json_filename):
		"""
		Method for populating the teachers database from the given JSON file.

		:param json_filename:
			The JSON file from which the teachers data should be read from.
		:type json_filename:
			str
		"""
		# Empty the current data.
		self._teachers_and_ids = {}

		# Read and json-load the data from the given file.
		with open(json_filename, 'r') as f:
			read_data = json.load(f)

		# Loop through the read dict and set up the database on this object.
		for teacher_id, data in read_data.items():
			# Fetch the data for this teacher.
			math_grades = data['math_grades']
			art_grades = data['art_grades']
			science_grades = data['science_grades']
			getting_along_matrix = numpy.array(data['students_getting_along_matrix'])

			# Fetch class type and setup input args.
			class_type = data['teacher_type']
			teacher_args = {
				'student_math_grades': math_grades,
				'student_art_grades': art_grades,
				'students_getting_along_matrix': getting_along_matrix
			}

			# If Arya, add also the science grades.
			if class_type == 'TeacherArya':
				teacher_args['student_science_grades'] = science_grades

			# Instantiate using eval and add to the dict.
			teacher_instance = eval(class_type)(**teacher_args)
			self._teachers_and_ids[teacher_id] = teacher_instance
