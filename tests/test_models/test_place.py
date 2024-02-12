#!/usr/bin/python3
"""Defines unittests for models/place.py.

Unittest classes:
    TestPlaceInstantiation
    TestPlaceSave
    TestPlaceToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlaceInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Place class."""

    def setUp(self):
        self.place = Place()

    def test_no_args_instantiates(self):
        self.assertEqual(Place, type(self.place))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(self.place, models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(self.place.id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(self.place.created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(self.place.updated_at))

    def test_attributes_are_public_class_attributes(self):
        attributes = ['city_id', 'user_id', 'name', 'description', 'number_rooms',
                      'number_bathrooms', 'max_guest', 'price_by_night',
                      'latitude', 'longitude', 'amenity_ids']
        for attr in attributes:
            self.assertEqual(str, type(getattr(Place, attr)))
            self.assertIn(attr, dir(self.place))
            self.assertNotIn(attr, self.place.__dict__)

    def test_two_places_unique_ids(self):
        new_place = Place()
        self.assertNotEqual(self.place.id, new_place.id)

    def test_two_places_different_created_at(self):
        new_place = Place()
        sleep(0.05)
        self.assertLess(self.place.created_at, new_place.created_at)

    def test_two_places_different_updated_at(self):
        new_place = Place()
        sleep(0.05)
        self.assertLess(self.place.updated_at, new_place.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        self.place.id = "123456"
        self.place.created_at = self.place.updated_at = dt
        place_str = self.place.__str__()
        self.assertIn("[Place] (123456)", place_str)
        self.assertIn("'id': '123456'", place_str)
        self.assertIn("'created_at': " + dt_repr, place_str)
        self.assertIn("'updated_at': " + dt_repr, place_str)

    def test_args_unused(self):
        self.assertNotIn(None, self.place.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        place = Place(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(place.id, "345")
        self.assertEqual(place.created_at, dt)
        self.assertEqual(place.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlaceSave(unittest.TestCase):
    """Unittests for testing save method of the Place class."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def setUp(self):
        self.place = Place()

    def test_one_save(self):
        sleep(0.05)
        first_updated_at = self.place.updated_at
        self.place.save()
        self.assertLess(first_updated_at, self.place.updated_at)

    def test_two_saves(self):
        sleep(0.05)
        first_updated_at = self.place.updated_at
        self.place.save()
        second_updated_at = self.place.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        self.place.save()
        self.assertLess(second_updated_at, self.place.updated_at)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            self.place.save(None)

    def test_save_updates_file(self):
        self.place.save()
        place_id = "Place." + self.place.id
        with open("file.json", "r") as f:
            self.assertIn(place_id, f.read())


class TestPlaceToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the Place class."""

    def setUp(self):
        self.place = Place()

    def test_to_dict_type(self):
        self.assertTrue(isinstance(self.place.to_dict(), dict))

    def test_to_dict_contains_correct_keys(self):
        keys = ['id', 'created_at', 'updated_at', '__class__']
        place_dict = self.place.to_dict()
        for key in keys:
            self.assertIn(key, place_dict)

    def test_to_dict_contains_added_attributes(self):
        self.place.middle_name = "Holberton"
        self.place.my_number = 98
        self.assertEqual("Holberton", self.place.middle_name)
        self.assertIn("my_number", self.place.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        place_dict = self.place.to_dict()
        self.assertEqual(str, type(place_dict["id"]))
        self.assertEqual(str, type(place_dict["created_at"]))
        self.assertEqual(str, type(place_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        self.place.id = "123456"
        self.place.created_at = self.place.updated_at = dt
        expected_dict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(self.place.to_dict(), expected_dict)

    def test_contrast_to_dict_dunder_dict(self):
        self.assertNotEqual(self.place.to_dict(), self.place.__dict__)

    def test_to_dict_with_arg(self):
        with self.assertRaises(TypeError):
            self.place.to_dict(None)


if __name__ == "__main__":
    unittest.main()

