from django.contrib import admin

# Register your models here.

from .models import Student, Class, Image, Attendance

admin.site.register(Student)
admin.site.register(Class)
admin.site.register(Image)
admin.site.register(Attendance)
