#!/usr/bin/python3
"""Defines unittests for models/state.py.

Unittest classes:
    TestStateInstantiation
    TestStateSave
    TestStateToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestStateInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the State class."""

    def setUp(self):
        self.state = State()

    def tearDown(self):
        del self.state

    def test_no_args_instantiates(self):
        self.assertEqual(State, type(self.state))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(self.state, models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(self.state.id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(self.state.created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(self.state.updated_at))

    def test_name_is_public_class_attribute(self):
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(self.state))
        self.assertNotIn("name", self.state.__dict__)

    def test_two_states_unique_ids(self):
        new_state = State()
        self.assertNotEqual(self.state.id, new_state.id)

    def test_two_states_different_created_at(self):
        new_state = State()
        sleep(0.05)
        self.assertLess(self.state.created_at, new_state.created_at)

    def test_two_states_different_updated_at(self):
        new_state = State()
        sleep(0.05)
        self.assertLess(self.state.updated_at, new_state.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        self.state.id = "123456"
        self.state.created_at = self.state.updated_at = dt
        state_str = str(self.state)
        self.assertIn("[State] (123456)", state_str)
        self.assertIn("'id': '123456'", state_str)
        self.assertIn("'created_at': " + dt_repr, state_str)
        self.assertIn("'updated_at': " + dt_repr, state_str)

    def test_args_unused(self):
        new_state = State(None)
        self.assertNotIn(None, new_state.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        new_state = State(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(new_state.id, "345")
        self.assertEqual(new_state.created_at, dt)
        self.assertEqual(new_state.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestStateSave(unittest.TestCase):
    """Unittests for testing save method of the State class."""

    def setUp(self):
        self.state = State()

    def tearDown(self):
        del self.state

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
        first_updated_at = self.state.updated_at
        self.state.save()
        self.assertLess(first_updated_at, self.state.updated_at)

    def test_two_saves(self):
        first_updated_at = self.state.updated_at
        self.state.save()
        second_updated_at = self.state.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        self.state.save()
        self.assertLess(second_updated_at, self.state.updated_at)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            self.state.save(None)

    def test_save_updates_file(self):
        self.state.save()
        state_id = "State." + self.state.id
        with open("file.json", "r") as f:
            self.assertIn(state_id, f.read())


class TestStateToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the State class."""

    def setUp(self):
        self.state = State()

    def tearDown(self):
        del self.state

    def test_to_dict_type(self):
        self.assertTrue(dict, type(self.state.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        self.assertIn("id", self.state.to_dict())
        self.assertIn("created_at", self.state.to_dict())
        self.assertIn("updated_at", self.state.to_dict())
        self.assertIn("__class__", self.state.to_dict())

    def test_to_dict_contains_added_attributes(self):
        self.state.middle_name = "Holberton"
        self.state.my_number = 98
        self.assertEqual("Holberton", self.state.middle_name)
        self.assertIn("my_number", self.state.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        state_dict = self.state.to_dict()
        self.assertEqual(str, type(state_dict["id"]))
        self.assertEqual(str, type(state_dict["created_at"]))
        self.assertEqual(str, type(state_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        self.state.id = "123456"
        self.state.created_at = self.state.updated_at = dt
        t_dict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(self.state.to_dict(), t_dict)

    def test_contrast_to_dict_dunder_dict(self):
        self.assertNotEqual(self.state.to_dict(), self.state.__dict__)

    def test_to_dict_with_arg(self):
        with self.assertRaises(TypeError):
            self.state.to_dict(None)


if __name__ == "__main__":
    unittest.main()

