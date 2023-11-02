from . import views
from django.urls import path 
from .views import *

urlpatterns = [
    path('user/followers/<int:user_id>/', GetAllUserFollowersView.as_view()),
    path('user/following/<int:user_id>/', GetAllUserFollowingView.as_view())
]