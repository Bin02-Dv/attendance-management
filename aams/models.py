from statistics import mode
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
# Create your models here.

class StudentCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    # course_1_code = models.CharField(max_length=1000, blank=True)
    course_1 = models.CharField(max_length=1000, blank=True)
    # course_1_unit = models.CharField(max_length=1000, blank=True)

    # course_2_code = models.CharField(max_length=1000, blank=True)
    course_2 = models.CharField(max_length=1000, blank=True)
    # course_2_unit = models.CharField(max_length=1000, blank=True)

    # course_3_code = models.CharField(max_length=1000, blank=True)
    course_3 = models.CharField(max_length=1000, blank=True)
    # course_3_unit = models.CharField(max_length=1000, blank=True)

    # course_4_code = models.CharField(max_length=1000, blank=True)
    course_4 = models.CharField(max_length=1000, blank=True)
    # course_4_unit = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    profileImg = models.ImageField(upload_to='students-pics', default='user.png')
    student_name = models.CharField(max_length=1000, blank=True)
    student_level = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.user.username

class Lecturer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    lecturer_name = models.CharField(max_length=1000, blank=True)
    course_taking = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.user.username


class AddCourse(models.Model):
    course_code = models.CharField(max_length=1000, blank=True)
    course_title = models.CharField(max_length=1000, blank=True)
    unit = models.IntegerField()

    def __str__(self):
        return self.course_code


class Attendance(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # id_user = models.IntegerField()
    lecturer = models.CharField(max_length=1000, default=0)
    course_title = models.CharField(max_length=1000, blank=True)
    # course_code = models.CharField(max_length=1000, blank=True)
    student_regis = models.CharField(max_length=1000, blank=True)
    # student_name = models.CharField(max_length=1000, blank=True)
    first_CA = models.CharField(max_length=1000, blank=True)
    second_CA = models.CharField(max_length=1000, blank=True)
    exams = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.student_regis
