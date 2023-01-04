from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

from datetime import date

from django.contrib.auth.models import User

# Create your models here.


class Class(models.Model):

    instructor = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class_id = models.CharField(primary_key=True, max_length=3, validators=[
                                RegexValidator(r'\d{3}')])
    class_name = models.CharField(max_length=50)
    # students = models.ForeignKey(Student, null=True)
    classImgs = models.FileField(max_length=300, null=True)
    # num_of_students = models.PositiveIntegerField()
    # present_students = models.

    def __str__(self):
        return (f'{self.class_name}-{self.class_id}')


class Student(models.Model):
    name = models.CharField(max_length=60)
    student_id = models.CharField(
        primary_key=True, max_length=8, validators=[RegexValidator(r'^(4)(\d{7})$')])

    student_absence = models.IntegerField(default=0)
    reg_date = models.DateTimeField('date registered',  auto_now_add=True)
    # null=True, on_delete=models.SET_NULL
    classes = models.ManyToManyField(Class)
    precense = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Image(models.Model):
    img_id = models.AutoField(primary_key=True)
    images = models.FileField(
        max_length=300, null=True)
    student = models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)
# CASCADE: When the referenced object is deleted, also delete the objects that have references to it (when you remove a blog post for instance, you might want to delete comments as well). SQL equivalent: CASCADE.

    def __str__(self):
        return self.images.name


class Attendance(models.Model):
    presence_date = models.DateField(primary_key=True, default=date.today)
    # verbose_name='%Y-%M-%D'

    student = models.ManyToManyField(Student)

    clas = models.ForeignKey(Class, null=True, on_delete=models.SET_NULL)
    # abcent = models.IntegerField()

    def __str__(self):
        return (f'{self.clas}-{self.presence_date}')
