from django.contrib import admin

# Register your models here.

from .models import User, Student, Class, Image

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Class)
admin.site.register(Image)
