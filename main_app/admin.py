from django.contrib import admin
# import your models here
from .models import Gorilla, Feeding, Toy

# Register your models here
admin.site.register(Gorilla)
admin.site.register(Feeding)
admin.site.register(Toy)