""" A module containing unit tests for the classes defined in Teachers module """

import unittest
import numpy

from Teachers import TeacherJessica

class TeacherJessicaTest(unittest.TestCase):
    """ Test class for the class TeacherJessica """

    def testConstruction(self):
        """ Test the construction of the object """
        # Set up a student math grade dict and create a teacher.
        math_grades = {'Kim': 7, 'Nadine': 8}
        teacher1 = TeacherJessica(student_math_grades=math_grades)

        # Check that the grades have been correctly set and that the
        # default art grade is 8.
        self.assertEqual(math_grades, teacher1.studentMathGrades())
        self.assertEqual({'Kim': 8, 'Nadine': 8}, teacher1.studentArtGrades())

        # Create another teacher and test custom art grades.
        art_grades = {'Kim': 6, 'Nadine': 9}
        teacher2 = TeacherJessica(
            student_math_grades=math_grades, 
            student_art_grades=art_grades)
        self.assertEqual(art_grades, teacher2.studentArtGrades())

        # Check the getter for student names.
        self.assertEqual(['Kim', 'Nadine'], teacher2.studentNames())

        # Check a custom getting along matrix.
        getting_along_matrix = numpy.array([[0.9, 0.6], [0.0, 0.8]])
        teacher3 = TeacherJessica(
            student_math_grades=math_grades,
            students_getting_along_matrix=getting_along_matrix)
        self.assertTrue(
            numpy.array_equal(
                getting_along_matrix, teacher3._studentsGettingAlongMatrix()))

    def testDetermineAverageGrade(self):
        """ Test the method for calculating the average grade for the students """
        # Set up math grades and art grades for three students and
        # create a teacher.
        math_grades = {'Kim': 7, 'Nadine': 8, 'Jacob': 9}
        art_grades = {'Kim': 8, 'Nadine': 10, 'Jacob': 5}
        teacher = TeacherJessica(
            student_math_grades=math_grades,
            student_art_grades=art_grades)

        # Check that the averages match expectations.
        expected_averages = {'Kim': 7.5, 'Nadine': 9.0, 'Jacob': 7.0}
        averages = teacher.determineAverageGrade()
        self.assertEqual(expected_averages, averages)

        # Check with custom weights.
        expected_averages = {'Kim': 7.9, 'Nadine': 9.8, 'Jacob': 5.4}
        averages = teacher.determineAverageGrade(weights=[0.1, 0.9])
        self.assertEqual(expected_averages, averages)

    def testCalculateTeacherSuccess(self):
        """ Test the method for calculating the success of a teacher """
        # Set up math grades and a perfectly getting along set of students.
        math_grades = {'Kim': 7, 'Nadine': 8}
        getting_along_matrix = numpy.ones((2, 2))
        teacher = TeacherJessica(
            student_math_grades=math_grades,
            students_getting_along_matrix=getting_along_matrix)

        # Check that the teacher success is equal to 100 %.
        teacher_success = teacher.calculateTeacherSuccess()
        self.assertEqual(teacher_success, 100.0)

        # Set up a not getting along at all set of students.
        math_grades = {'Kim': 7, 'Nadine': 8}
        getting_along_matrix = numpy.zeros((2, 2))
        teacher = TeacherJessica(
            student_math_grades=math_grades,
            students_getting_along_matrix=getting_along_matrix)

        # Check that the teacher success is equal to 0 %.
        teacher_success = teacher.calculateTeacherSuccess()
        self.assertEqual(teacher_success, 0.0)

        # Check with something more realistic: in between.
        math_grades = {'Kim': 7, 'Nadine': 8}
        getting_along_matrix = numpy.array([[0.9, 0.6], [0.6, 0.7]])
        teacher = TeacherJessica(
            student_math_grades=math_grades,
            students_getting_along_matrix=getting_along_matrix)

        # Check that the teacher success is more than 60 % but less than 90.
        teacher_success = teacher.calculateTeacherSuccess()
        self.assertGreater(teacher_success, 60)
        self.assertLess(teacher_success, 90)

    # TODO: a unit test for html image generation and tests for TeacherArya.


if __name__ == '__main__':
    unittest.main()