""" Module implementing a type of object which can be saved to an HDF5 file """

from abc import ABC, abstractmethod
import h5py
import numpy
import re


def toCamelCase(chars):
	"""
	Utility method for converting the given characters to camel case.
	"""
	word_regex_pattern = re.compile("[^A-Za-z]+")
	words = word_regex_pattern.split(chars)
	return ''.join(w.lower() if i == 0 else w.title() for i, w in enumerate(words))


def processHdf5Data(hdf5_dataset_value):
	"""
	Utility method for processing data in an hdf5 dataset. If the data
	is a byte-string, the method will decode it. Else, the data will
	be returned as it is.
	"""
	if isinstance(hdf5_dataset_value, bytes):
		return hdf5_dataset_value.decode("utf-8")

	return hdf5_dataset_value


class Serializable(ABC):

	@abstractmethod
	def _serializableProperties(cls):
		"""
		A method which returns the properties of the class which should be
		saved, as a list of strings. Must be implemented by an inherited class.
		The properties must all be such that they can be written to an hdf5 file,
		such as numpy arrays, strings and lists.

		:returns:
			The properties of the class which should be saved in an hdf5 file.
		:rtype:
			list of str
		"""

	def saveToFile(self, hdf5_filename):
		"""
		A method for saving the serializable properties to a file.
		"""
		# Fetch the names of the serializable properties.
		properties_names = self._serializableProperties()

		# Reduce the properties to those which have a getter.
		existing_properties = [
			name for name in properties_names
			if getattr(self, toCamelCase(name), None) is not None
		]

		# Fetch the property values which are there.
		properties_values = [getattr(self, toCamelCase(name))() for name in existing_properties]

		# Save the data to an hdf5 file and close it.
		h5_file = h5py.File(hdf5_filename, "w")
		for name, value in zip(existing_properties, properties_values):
			h5_file.create_dataset(name, data=value)
		h5_file.close()

	@classmethod
	def instantiateFromFile(cls, hdf5_filename):
		"""
		Create a new instance of this class by reading the data from an hdf5 file.
		"""
		properties_names = cls._serializableProperties()
		read_h5 = h5py.File(hdf5_filename, 'r')

		# Check which names actually exist in the file and fetch the values.
		existing_properties_dict = {
			key: processHdf5Data(read_h5[key][()])
			for key in read_h5.keys() if key in properties_names
		}

		read_h5.close()

		# Return a new instance.
		return cls(**existing_properties_dict)


class SerializableClass(Serializable):

	@classmethod
	def _serializableProperties(cls):
		"""
		Define the properties which should be serialized.
		"""
		return ['my_string', 'numpy_array', 'my_integer_list']

	def __init__(self, my_string, numpy_array, my_integer_list):
		"""
		An example class deriving from Serializable which can be serialized
		to an hdf5 file.
		"""
		self._my_string = my_string
		self._numpy_array = numpy_array
		self._my_integer_list = my_integer_list

	def myString(self):
		return self._my_string

	def numpyArray(self):
		return self._numpy_array

	def myIntegerList(self):
		return self._my_integer_list


# Create a serializable class object.
exp_array = numpy.exp(0.1 * numpy.arange(1, 10))
test_object = SerializableClass(
	my_string='this_is_a_string', 
	numpy_array=exp_array,
	my_integer_list=[-5, 5, 25, 11])

# Define an hdf5 file name and save and read the object.
hdf5_file = 'test.hdf5'
test_object.saveToFile(hdf5_file)
read_object = SerializableClass.instantiateFromFile(hdf5_file)

print(read_object.myString())
print(read_object.numpyArray())
print(read_object.myIntegerList())

print('correctly saved?', numpy.linalg.norm(exp_array - read_object.numpyArray()) == 0.0)



