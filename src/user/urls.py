from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserList.as_view()),
    path('<str:email>', views.UserDetail.as_view()),
    path('login/', views.user_login),
]
