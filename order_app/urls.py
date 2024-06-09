from . import views
from django.urls import path 
from .views import *


urlpatterns = [
    path('get-assignmnet-answer/', get_assignment_solution.as_view())   
]