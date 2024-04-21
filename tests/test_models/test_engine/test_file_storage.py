#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
from models.engine.file_storage import FileStorage

FileStorage = file_storage.FileStorage
classes = {
    "Amenity": Amenity,
    "BaseModel": BaseModel,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User,
}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(["models/engine/file_storage.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
            [
                "tests/test_models/test_engine/\
test_file_storage.py"
            ]
        )
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(
            file_storage.__doc__, None, "file_storage.py needs a docstring"
        )
        self.assertTrue(
            len(file_storage.__doc__) >= 1, "file_storage.py needs a docstring"
        )

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(
            FileStorage.__doc__, None, "FileStorage class needs a docstring"
        )
        self.assertTrue(
            len(FileStorage.__doc__) >= 1,
            "FileStorage class needs a docstring"
        )

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(
                func[1].__doc__, None,
                "{:s} method needs a docstring".format(func[0])
            )
            self.assertTrue(
                len(func[1].__doc__) >= 1,
                "{:s} method needs a docstring".format(func[0]),
            )

    def test_doc_file(self):
        """... documentation for the file"""
        expected = ("\nHandles I/O, writing and reading, of JSON for storage ")

    class TestFileStorageDocs(unittest.TestCase):
        """Tests to check the documentation and style of FileStorage class"""

        @classmethod
        def setUpClass(cls):
            """Set up for the doc tests"""
            cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

        def test_doc_class(self):
            """... documentation for the class"""
            expected = 'handles long term storage of all class instances'
            actual = FileStorage.__doc__
            self.assertEqual(expected, actual)

        def test_doc_all(self):
            """... documentation for all function"""
            expected = 'returns private attribute: __objects'
            actual = FileStorage.all.__doc__
            self.assertEqual(expected, actual)

        def test_doc_new(self):
            """... documentation for new function"""
            expected = ("sets / updates in __objects the\
                        obj with key <obj class "
                        "name>.id")
            actual = FileStorage.new.__doc__
            self.assertEqual(expected, actual)
        expected = ("sets / updates in __objects the\
            obj with key <obj class "
                    "name>.id")
        actual = FileStorage.new.__doc__
        self.assertEqual(expected, actual)

    def test_doc_save(self):
        """... documentation for save function"""
        expected = 'serializes __objects to the JSON file (path: __file_path)'
        actual = FileStorage.save.__doc__
        self.assertEqual(expected, actual)

    def test_doc_reload(self):
        """... documentation for reload function"""
        expected = ("if file exists, deserializes JSON file to __objects, "
                    "else nothing")
        actual = FileStorage.reload.__doc__
        self.assertEqual(expected, actual)

    def test_doc_delete(self):
        """... documentation for delete function"""
        expected = 'delete obj from __objects if it exists'
        actual = FileStorage.delete.__doc__
        self.assertEqual(expected, actual)

    def test_doc_close(self):
        """... documentation for close function"""
        expected = 'call reload() method for deserializing the JSON file'
        actual = FileStorage.close.__doc__
        self.assertEqual(expected, actual)


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    @unittest.skipIf(models.storage_t == "db", "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == "db", "not testing file storage")
    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == "db", "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))

    @unittest.skipIf(models.storage_t == "db",
                     "not testing file storage")
    def test_get(self):
        """Test that the get method properly retrievs objects"""
        storage = FileStorage()
        self.assertIs(storage.get("User", "blah"), None)
        self.assertIs(storage.get("blah", "blah"), None)
        new_user = User()
        new_user.save()
        self.assertIs(storage.get("User", new_user.id), new_user)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                     "not testing file storage")
    def test_count(self):
        """Test the count() function"""
        state = State()
        state.name = "State_name"
        storage = models.storage
        storage.new(state)
        storage.save()
        self.assertTrue(storage.count(State) > 0)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                     "not testing file storage")
    def test_delete(self):
        """Test the delete method"""
        storage = FileStorage()
        new_user = User()
        new_user.save()
        storage.delete(new_user)
        self.assertIs(storage.get("User", new_user.id), None)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                     "not testing file storage")
    def test_close(self):
        """Test the close method"""
        storage = FileStorage()
        storage.reload()
        storage.close()
        self.assertTrue(os.path.exists("file.json"))

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                     "not testing file storage")
    def test_reload(self):
        """Test the reload method"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        storage.reload()
        for key, value in new_dict.items():
            self.assertTrue(value == storage.all()[key])
