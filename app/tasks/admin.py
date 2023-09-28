from django.contrib import admin
from .models import CPUTest, MemoryTest

# Register your models here.
admin.site.register(CPUTest)
admin.site.register(MemoryTest)