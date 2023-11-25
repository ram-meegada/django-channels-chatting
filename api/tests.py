from django.test import TestCase
from datetime import datetime
from api.models import User
import random

class StudentTestCase(TestCase):
    def setUp(self):
        start_time = datetime.now()
        students = []
        batch_size = 500
        for i in range(100000):
            student = User()
            student.first_name = str(i)
            student.email = f"duplicate{i}@yopmail.com"
            student.last_name = str(i)
            student.created_at = datetime.now()
            student.role_of_user = '2' if i in range(0, 5000) else '1' 
            students.append(student)
        User.objects.bulk_create(students, batch_size)
        end_time = datetime.now()
        print(f" Created in {end_time - start_time}")

    def test_lookup(self):
        start_time = datetime.now()
        user = User.objects.get(first_name="4999")
        end_time = datetime.now()
        print(f"Looked up in {end_time - start_time}")