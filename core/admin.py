# Register your models here.
from django.contrib import admin
from .models import Product
from .models import Company
from .models import Supplier
from .models import Category
from .models import Employee
from .models import Sale



admin.site.register(Company)
admin.site.register(Product)
admin.site.register(Supplier)
admin.site.register(Category)
admin.site.register(Employee)
admin.site.register(Sale)