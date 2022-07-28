""" Module implementing a type of object which can be saved to an HDF5 file """

from abc import ABC, abstractmethod
import ast
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
		hdf5_dataset_value = hdf5_dataset_value.decode("utf-8")

	# If the value is a string, it can also be a dict saved as a string.
	# Thus, call literal eval of ast to make sure the final data type
	# is correct.
	if isinstance(hdf5_dataset_value, str):
		hdf5_dataset_value = ast.literal_eval(hdf5_dataset_value)

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
			# Convert dicts to string, since hdf5 doesn't natively support them.
			if isinstance(value, dict):
				value = str(value)
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
