from django.test import TestCase
from datetime import datetime
from api.models import *
import random

class RandomTestCase(TestCase):
    def setUp(self):
        start_time = datetime.now()
        objects = []
        batch_size = 1000
        for i in range(26000):  
            obj = Borrowers()
            obj.borrower = f"random_{i}"
            objects.append(obj)
        Borrowers.objects.bulk_create(objects, batch_size)
        end_time = datetime.now()
        print(f" Created in {end_time - start_time}")

    def test_lookup(self):
        start_time = datetime.now()
        for i in range(18000):
            random_obj = Borrowers.objects.get(borrower = f"random_{i}")
        end_time = datetime.now()
        print(f"Looked up in {end_time - start_time}")