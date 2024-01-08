from django.contrib import admin
from .models import Student, StudentCourse, AddCourse, Attendance, Lecturer

# Register your models here.

admin.site.register([
    StudentCourse, AddCourse, Student, Attendance, Lecturer
])
