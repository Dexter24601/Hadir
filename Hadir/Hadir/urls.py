"""Hadir URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from HadirApp import views  # . = current folder
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    path('admin/', admin.site.urls),
    # http://localhost:8000/admin/

    path('', views.temp, name="temp"),
    # http://localhost:8000/Hadir/


    path('Hadir/', views.index, name="index"),
    # http://localhost:8000/Hadir/

    path('Hadir/detail', views.detail, name="detail"),
    # http://localhost:8000/Hadir/detail


    path('Hadir/student_enrollment/<str:class_name>-<int:class_id>',
         views.student_enrollment, name="student_enrollment"),
    # http://localhost:8000/Hadir/student_enrollment

    path('Hadir/Create_class', views.create_class, name="create_class"),
    # http://localhost:8000/Hadir/Create_class


    path('Hadir/Classes', views.Classes, name="Classes"),
    # http://localhost:8000/Hadir/Classes


    path('Hadir/Classes/<str:class_name>-<int:class_id>', views.clas, name="clas"),
    # http://localhost:8000/Hadir/math-103

    path('Hadir/Classes/<str:class_name>-<int:class_id>/Dashboard',
         views.dashboard, name="dashboard"),
    # http://localhost:8000/Hadir/Dashboard

    path('Hadir/Classes/<str:class_name>-<int:class_id>/Attendance',
         views.attendance, name="attendance"),
    # http://localhost:8000/Hadir/Attendance


    path('Hadir/Classes/<str:class_name>-<int:class_id>/Results',
         views.attendanceResult, name="attendanceResult"),
    # http://localhost:8000/Hadir/--


    path('Hadir/images', views.images, name='images'),
    # http://localhost:8000/Hadir/images

    path('Hadir/register', views.registerPage, name="registerPage"),
    # http://localhost:8000/Hadir/register


    path('Hadir/login', views.loginPage, name="loginPage"),
    # http://localhost:8000/Hadir/login


    path('Hadir/logout', views.LogoutUser, name="LogoutUser"),


    path('Hadir/main', views.mainPage, name="mainPage"),
    # http://localhost:8000/Hadir/main


    path('Hadir/404', views.PageNotFound, name="PageNotFound")
    # http://localhost:8000/Hadir/404

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# X:\TU\Capstone project\Engine\Django\Project\Hadir\HadirApp\views.py
# X:\TU\Capstone project\Engine\Django\Project\Hadir\Hadir\urls.py
