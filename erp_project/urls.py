from django.contrib import admin
from django.urls import path,include
from core.views import dashboard, login_view, logout_view, company_profile, inventory, employee_list,sales_list,leave,role_select,register_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('company/', company_profile, name='company'),
    path('inventory/', inventory, name='inventory'),
    path('employee/', employee_list, name='employee_list'),
    path('sales/', sales_list, name='sales_list'),
    path('leave/', leave, name='leave'),
    path('', role_select, name='role_select'),

    #     # ✅ YE BILKUL SAHI HAI
    # path('manager/', include('manager.urls')),



]
