#!/usr/bin/python3
"""Defines unittests for models/user.py.

Unittest classes:
    TestUserInstantiation
    TestUserSave
    TestUserToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestUserInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the User class."""

    def setUp(self):
        self.user = User()

    def tearDown(self):
        del self.user

    def test_no_args_instantiates(self):
        self.assertEqual(User, type(self.user))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(self.user, models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(self.user.id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(self.user.created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(self.user.updated_at))

    def test_email_is_public_str(self):
        self.assertEqual(str, type(User.email))

    def test_password_is_public_str(self):
        self.assertEqual(str, type(User.password))

    def test_first_name_is_public_str(self):
        self.assertEqual(str, type(User.first_name))

    def test_last_name_is_public_str(self):
        self.assertEqual(str, type(User.last_name))

    def test_two_users_unique_ids(self):
        new_user = User()
        self.assertNotEqual(self.user.id, new_user.id)

    def test_two_users_different_created_at(self):
        new_user = User()
        sleep(0.05)
        self.assertLess(self.user.created_at, new_user.created_at)

    def test_two_users_different_updated_at(self):
        new_user = User()
        sleep(0.05)
        self.assertLess(self.user.updated_at, new_user.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        self.user.id = "123456"
        self.user.created_at = self.user.updated_at = dt
        user_str = str(self.user)
        self.assertIn("[User] (123456)", user_str)
        self.assertIn("'id': '123456'", user_str)
        self.assertIn("'created_at': " + dt_repr, user_str)
        self.assertIn("'updated_at': " + dt_repr, user_str)

    def test_args_unused(self):
        new_user = User(None)
        self.assertNotIn(None, new_user.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        new_user = User(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(new_user.id, "345")
        self.assertEqual(new_user.created_at, dt)
        self.assertEqual(new_user.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUserSave(unittest.TestCase):
    """Unittests for testing save method of the User class."""

    def setUp(self):
        self.user = User()

    def tearDown(self):
        del self.user

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

    def test_one_save(self):
        first_updated_at = self.user.updated_at
        self.user.save()
        self.assertLess(first_updated_at, self.user.updated_at)

    def test_two_saves(self):
        first_updated_at = self.user.updated_at
        self.user.save()
        second_updated_at = self.user.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        self.user.save()
        self.assertLess(second_updated_at, self.user.updated_at)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            self.user.save(None)

    def test_save_updates_file(self):
        self.user.save()
        user_id = "User." + self.user.id
        with open("file.json", "r") as f:
            self.assertIn(user_id, f.read())


class TestUserToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the User class."""

    def setUp(self):
        self.user = User()

    def tearDown(self):
        del self.user

    def test_to_dict_type(self):
        self.assertTrue(dict, type(self.user.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        self.assertIn("id", self.user.to_dict())
        self.assertIn("created_at", self.user.to_dict())
        self.assertIn("updated_at", self.user.to_dict())
        self.assertIn("__class__", self.user.to_dict())

    def test_to_dict_contains_added_attributes(self):
        self.user.middle_name = "Holberton"
        self.user.my_number = 98
        self.assertEqual("Holberton", self.user.middle_name)
        self.assertIn("my_number", self.user.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        user_dict = self.user.to_dict()
        self.assertEqual(str, type(user_dict["id"]))
        self.assertEqual(str, type(user_dict["created_at"]))
        self.assertEqual(str, type(user_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        self.user.id = "123456"
        self.user.created_at = self.user.updated_at = dt
        t_dict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(self.user.to_dict(), t_dict)

    def test_contrast_to_dict_dunder_dict(self):
        self.assertNotEqual(self.user.to_dict(), self.user.__dict__)

    def test_to_dict_with_arg(self):
        with self.assertRaises(TypeError):
            self.user.to_dict(None)


if __name__ == "__main__":
    unittest.main()

