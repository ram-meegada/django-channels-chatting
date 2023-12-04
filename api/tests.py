from django.test import TestCase
from datetime import datetime
from api.models import User, RandomModel
import random

class RandomTestCase(TestCase):
    def setUp(self):
        start_time = datetime.now()
        objects = []
        batch_size = 500
        for i in range(1000000):
            obj = RandomModel()
            obj.name = f"random_{i}"
            objects.append(obj)
        RandomModel.objects.bulk_create(objects, batch_size)
        end_time = datetime.now()
        print(f" Created in {end_time - start_time}")

    def test_lookup(self):
        start_time = datetime.now()
        random_obj = RandomModel.objects.get(id=99999)
        end_time = datetime.now()
        print(f"Looked up in {end_time - start_time}")