from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("task/<str:pk>/",views.task, name="task"),
    path("delete/<str:pk>",views.delete_task, name="delete"),
    path("create-task/",views.create_task, name="create-task"),
    path("login-register/",views.loginPage, name="login-register"),
    path("logout/",views.logoutPage, name="logout"),
    path("register/",views.registerPage, name="register")

]
