from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# ================= COMPANY =================
class Company(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    gst_number = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


# ================= CATEGORY =================
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# ================= SUPPLIER =================
class Supplier(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name


# ================= PRODUCT =================
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return self.name


# ================= EMPLOYEE =================
class Employee(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('Staff', 'Staff'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Staff')
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    is_active = models.BooleanField(default=True)
    joining_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username


# ================= SALE =================
class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    total_price = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.total_price and self.product:
            self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)


# ================= ATTENDANCE =================
STATUS_CHOICES = (
    ('Present', 'Present'),
    ('Absent', 'Absent'),
    ('Leave', 'Leave'),
)

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    remarks = models.TextField(blank=True, null=True)


# ================= LEAVE REQUEST =================
LEAVE_STATUS = (
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
)

class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=LEAVE_STATUS, default='Pending')
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.user.username} - {self.status}"
