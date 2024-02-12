#!/usr/bin/python3
"""Defines unittests for models/review.py.

Unittest classes:
    TestReviewInstantiation
    TestReviewSave
    TestReviewToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class TestReviewInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Review class."""

    def setUp(self):
        self.review_instance = Review()

    def test_no_args_instantiates(self):
        self.assertEqual(Review, type(self.review_instance))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(self.review_instance, models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(self.review_instance.id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(self.review_instance.created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(self.review_instance.updated_at))

    def test_place_id_is_public_class_attribute(self):
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(self.review_instance))
        self.assertNotIn("place_id", self.review_instance.__dict__)

    def test_user_id_is_public_class_attribute(self):
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(self.review_instance))
        self.assertNotIn("user_id", self.review_instance.__dict__)

    def test_text_is_public_class_attribute(self):
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(self.review_instance))
        self.assertNotIn("text", self.review_instance.__dict__)

    def test_two_reviews_unique_ids(self):
        new_review_instance = Review()
        self.assertNotEqual(self.review_instance.id, new_review_instance.id)

    def test_two_reviews_different_created_at(self):
        new_review_instance = Review()
        sleep(0.05)
        self.assertLess(self.review_instance.created_at, new_review_instance.created_at)

    def test_two_reviews_different_updated_at(self):
        new_review_instance = Review()
        sleep(0.05)
        self.assertLess(self.review_instance.updated_at, new_review_instance.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        self.review_instance.id = "123456"
        self.review_instance.created_at = self.review_instance.updated_at = dt
        review_str = str(self.review_instance)
        self.assertIn("[Review] (123456)", review_str)
        self.assertIn("'id': '123456'", review_str)
        self.assertIn("'created_at': " + dt_repr, review_str)
        self.assertIn("'updated_at': " + dt_repr, review_str)

    def test_args_unused(self):
        self.assertNotIn(None, self.review_instance.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        review_instance = Review(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(review_instance.id, "345")
        self.assertEqual(review_instance.created_at, dt)
        self.assertEqual(review_instance.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReviewSave(unittest.TestCase):
    """Unittests for testing save method of the Review class."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def setUp(self):
        self.review_instance = Review()

    def test_one_save(self):
        first_updated_at = self.review_instance.updated_at
        sleep(0.05)
        self.review_instance.save()
        self.assertLess(first_updated_at, self.review_instance.updated_at)

    def test_two_saves(self):
        first_updated_at = self.review_instance.updated_at
        sleep(0.05)
        self.review_instance.save()
        second_updated_at = self.review_instance.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        self.review_instance.save()
        self.assertLess(second_updated_at, self.review_instance.updated_at)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            self.review_instance.save(None)

    def test_save_updates_file(self):
        self.review_instance.save()
        review_id = "Review." + self.review_instance.id
        with open("file.json", "r") as f:
            self.assertIn(review_id, f.read())


class TestReviewToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the Review class."""

    def setUp(self):
        self.review_instance = Review()

    def test_to_dict_type(self):
        self.assertTrue(dict, type(self.review_instance.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        self.assertIn("id", self.review_instance.to_dict())
        self.assertIn("created_at", self.review_instance.to_dict())
        self.assertIn("updated_at", self.review_instance.to_dict())
        self.assertIn("__class__", self.review_instance.to_dict())

    def test_to_dict_contains_added_attributes(self):
        self.review_instance.middle_name = "Holberton"
        self.review_instance.my_number = 98
        self.assertEqual("Holberton", self.review_instance.middle_name)
        self.assertIn("my_number", self.review_instance.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        review_dict = self.review_instance.to_dict()
        self.assertEqual(str, type(review_dict["id"]))
        self.assertEqual(str, type(review_dict["created_at"]))
        self.assertEqual(str, type(review_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        self.review_instance.id = "123456"
        self.review_instance.created_at = self.review_instance.updated_at = dt
        expected_dict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(self.review_instance.to_dict(), expected_dict)

    def test_contrast_to_dict_dunder_dict(self):
        self.assertNotEqual(self.review_instance.to_dict(), self.review_instance.__dict__)

    def test_to_dict_with_arg(self):
        with self.assertRaises(TypeError):
            self.review_instance.to_dict(None)


if __name__ == "__main__":
    unittest.main()

