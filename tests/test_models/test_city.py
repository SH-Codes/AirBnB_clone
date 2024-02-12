#!/usr/bin/python3
"""Defines unittests for models/city.py.

Unittest classes:
    TestCityInstantiation
    TestCitySave
    TestCityToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCityInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the City class."""

    def setUp(self):
        self.city = City()

    def tearDown(self):
        del self.city

    def test_no_args_instantiates(self):
        self.assertEqual(City, type(self.city))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(self.city, models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(self.city.id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(self.city.created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(self.city.updated_at))

    def test_state_id_is_public_class_attribute(self):
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(self.city))
        self.assertNotIn("state_id", self.city.__dict__)

    def test_name_is_public_class_attribute(self):
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(self.city))
        self.assertNotIn("name", self.city.__dict__)

    def test_two_cities_unique_ids(self):
        new_city = City()
        self.assertNotEqual(self.city.id, new_city.id)

    def test_two_cities_different_created_at(self):
        new_city = City()
        sleep(0.05)
        self.assertLess(self.city.created_at, new_city.created_at)

    def test_two_cities_different_updated_at(self):
        new_city = City()
        sleep(0.05)
        self.assertLess(self.city.updated_at, new_city.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        self.city.id = "123456"
        self.city.created_at = self.city.updated_at = dt
        city_str = str(self.city)
        self.assertIn("[City] (123456)", city_str)
        self.assertIn("'id': '123456'", city_str)
        self.assertIn("'created_at': " + dt_repr, city_str)
        self.assertIn("'updated_at': " + dt_repr, city_str)

    def test_args_unused(self):
        new_city = City(None)
        self.assertNotIn(None, new_city.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        new_city = City(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(new_city.id, "345")
        self.assertEqual(new_city.created_at, dt)
        self.assertEqual(new_city.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCitySave(unittest.TestCase):
    """Unittests for testing save method of the City class."""

    def setUp(self):
        self.city = City()

    def tearDown(self):
        del self.city

    def test_one_save(self):
        first_updated_at = self.city.updated_at
        self.city.save()
        self.assertLess(first_updated_at, self.city.updated_at)

    def test_two_saves(self):
        first_updated_at = self.city.updated_at
        self.city.save()
        second_updated_at = self.city.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        self.city.save()
        self.assertLess(second_updated_at, self.city.updated_at)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            self.city.save(None)

    def test_save_updates_file(self):
        self.city.save()
        city_id = "City." + self.city.id
        with open("file.json", "r") as f:
            self.assertIn(city_id, f.read())


class TestCityToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the City class."""

    def setUp(self):
        self.city = City()

    def tearDown(self):
        del self.city

    def test_to_dict_type(self):
        self.assertTrue(dict, type(self.city.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        self.assertIn("id", self.city.to_dict())
        self.assertIn("created_at", self.city.to_dict())
        self.assertIn("updated_at", self.city.to_dict())
        self.assertIn("__class__", self.city.to_dict())

    def test_to_dict_contains_added_attributes(self):
        self.city.middle_name = "Holberton"
        self.city.my_number = 98
        self.assertEqual("Holberton", self.city.middle_name)
        self.assertIn("my_number", self.city.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        city_dict = self.city.to_dict()
        self.assertEqual(str, type(city_dict["id"]))
        self.assertEqual(str, type(city_dict["created_at"]))
        self.assertEqual(str, type(city_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        self.city.id = "123456"
        self.city.created_at = self.city.updated_at = dt
        t_dict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(self.city.to_dict(), t_dict)

    def test_contrast_to_dict_dunder_dict(self):
        self.assertNotEqual(self.city.to_dict(), self.city.__dict__)

    def test_to_dict_with_arg(self):
        with self.assertRaises(TypeError):
            self.city.to_dict(None)


if __name__ == "__main__":
    unittest.main()

