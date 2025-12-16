from django.shortcuts import render
from .models import Product
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .models import Product, Company,Supplier,Category, Employee,Sale,Attendance,LeaveRequest
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
from django.db import models
from django.db.models import Sum

@login_required
def dashboard(request):
    company = Company.objects.first()

    # Employee data
    employees = Employee.objects.all()
    total_employees = employees.count()
    active_employees = employees.filter(is_active=True).count()
    inactive_employees = total_employees - active_employees
    male_count = employees.filter(gender='Male').count()
    female_count = employees.filter(gender='Female').count()
    
    # Attendance today
    today = timezone.now().date()
    attendance_today = Attendance.objects.filter(date=today)
    employees_on_leave = attendance_today.filter(status='Leave').count()

    # Inventory data
    products = Product.objects.all()
    total_products = products.count()
    total_quantity = sum([p.quantity for p in products])
    total_value = sum([p.quantity * p.price for p in products])
    low_stock = products.filter(quantity__lt=10)

    # Sales data
    sales = Sale.objects.all()
    today_sales = sum([s.total_price for s in sales if s.date.date() == today])
    weekly_sales = []
    labels = []
    for i in range(7):
        day = today - timezone.timedelta(days=i)
        labels.append(day.strftime('%a'))
        day_sales = sum([s.total_price for s in sales if s.date.date() == day])
        weekly_sales.append(day_sales)
    labels.reverse()
    weekly_sales.reverse()

    context = {
        'company': company,
        'total_employees': total_employees,
        'active_employees': active_employees,
        'inactive_employees': inactive_employees,
        'male_count': male_count,
        'female_count': female_count,
        'employees_on_leave': employees_on_leave,
        'total_products': total_products,
        'total_quantity': total_quantity,
        'total_value': total_value,
        'low_stock': low_stock,
        'today_sales': today_sales,
        'weekly_sales': weekly_sales,
        'weekly_labels': labels,
    }
    return render(request, 'dashboard.html', context)



@login_required
def dashboard(request):
    products = Product.objects.all()
    company = Company.objects.first()   # 👈 company data

    context = {
        'products': products,
        'company': company
    }

    return render(request, 'dashboard.html', context)


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def company_profile(request):
    company = Company.objects.first()
    return render(request, 'company.html', {'company': company})


@login_required
def inventory(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    suppliers = Supplier.objects.all()

    # Optional: low stock alert
    low_stock = products.filter(quantity__lt=5)

    context = {
        'products': products,
        'categories': categories,
        'suppliers': suppliers,
        'low_stock': low_stock
    }
    return render(request, 'inventory.html', context)


@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})


@login_required
def sales_list(request):
    sales = Sale.objects.select_related(
        'product',
        'employee',
        'employee__user'
    ).order_by('-date')

    # Total Sales (FAST & CORRECT)
    total_sales = sales.aggregate(
        total=Sum('total_price')
    )['total'] or 0

    # Today's Sales
    today = timezone.now().date()
    today_sales = sales.filter(
        date__date=today
    ).aggregate(
        total=Sum('total_price')
    )['total'] or 0

    context = {
        'sales': sales,
        'total_sales': total_sales,
        'today_sales': today_sales
    }

    return render(request, 'sales_list.html', context)



# Employee applies for leave
def apply_leave(request):
    if request.method == 'POST':
        start = request.POST['start_date']
        end = request.POST['end_date']
        reason = request.POST['reason']
        employee = Employee.objects.get(user=request.user)
        LeaveRequest.objects.create(employee=employee, start_date=start, end_date=end, reason=reason)
        messages.success(request, "Leave request submitted successfully!")
        return redirect('dashboard')

    return render(request, 'apply_leave.html')


# Admin dashboard for leave requests
def leave_requests(request):
    leaves = LeaveRequest.objects.all().order_by('-applied_on')
    context = {'leaves': leaves}
    return render(request, 'leave_requests.html', context)


# Admin approves/rejects leave
def update_leave_status(request, leave_id, status):
    leave = LeaveRequest.objects.get(id=leave_id)
    if status in ['Approved', 'Rejected']:
        leave.status = status
        leave.save()
    return redirect('leave_requests')



# @login_required
# def leave_dashboard(request):
#     employee = Employee.objects.get(user=request.user)
    
#     # Employee submitting leave
#     if request.method == 'POST':
#         start = request.POST['start_date']
#         end = request.POST['end_date']
#         reason = request.POST['reason']

#         LeaveRequest.objects.create(
#             employee=employee,
#             start_date=start,
#             end_date=end,
#             reason=reason
#         )
#         messages.success(request, "Leave request submitted successfully!")
#         return redirect('leave_dashboard')

#     # Fetch data for template
#     leaves = LeaveRequest.objects.all().order_by('-id')  # all leaves
#     employees_on_leave = LeaveRequest.objects.filter(status='Approved').count()

#     context = {
#         'employee': employee,
#         'leaves': leaves,
#         'employees_on_leave': employees_on_leave
#     }
#     return render(request, 'leave_dashboard.html', context)



# @login_required
# def leave(request):
#     employee = Employee.objects.filter(user=request.user).first()

#     if not employee:
#         messages.error(request, "Employee profile not found")
#         return redirect('/dashboard/')

#     # FORM SUBMIT
#     if request.method == "POST":
#         start = request.POST.get('start_date')
#         end = request.POST.get('end_date')
#         reason = request.POST.get('reason')

#         LeaveRequest.objects.create(
#             employee=employee,
#             start_date=start,
#             end_date=end,
#             reason=reason,
#             status='Pending'
#         )

#         messages.success(request, "Leave request submitted successfully!")
#         return redirect('/leave/')

#     # SHOW DATA
#     leaves = LeaveRequest.objects.all().order_by('-id')

#     context = {
#         'leaves': leaves
#     }

#     return render(request, 'leave.html', context)   # 🔥 MOST IMPORTANT LINE

@login_required
def leave(request):
    employee = Employee.objects.filter(user=request.user).first()

    if not employee:
        messages.error(request, "Employee profile not found")
        return redirect('/dashboard/')

    # ================= APPLY LEAVE =================
    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')

        LeaveRequest.objects.create(
            employee=employee,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            status='Pending'
        )

        messages.success(request, "Leave applied successfully")
        return redirect('/leave/')

    # ================= BASIC DATA =================
    leaves = LeaveRequest.objects.filter(employee=employee).order_by('-id')

    total_leave = leaves.count()
    approved = leaves.filter(status='Approved').count()
    pending = leaves.filter(status='Pending').count()

    today = timezone.now().date()

    # ================= ON LEAVE EMPLOYEES =================
    on_leave_employees_list = LeaveRequest.objects.filter(
        status='Approved',
        start_date__lte=today,
        end_date__gte=today
    ).select_related('employee', 'employee__user')

    # ================= ACTIVE EMPLOYEES =================
    on_leave_ids = on_leave_employees_list.values_list('employee_id', flat=True)

    active_employees_list = Employee.objects.filter(
        is_active=True
    ).exclude(
        id__in=on_leave_ids
    ).select_related('user')

    # ================= CONTEXT =================
    context = {
        'leaves': leaves,
        'total_leave': total_leave,
        'approved_leave': approved,
        'pending_leave': pending,

        # 🔥 NEW DATA FOR UI
        'active_employees_list': active_employees_list,
        'on_leave_employees_list': on_leave_employees_list,
    }

    return render(request, 'leave.html', context)



def role_select(request):
    return render(request, 'role_select.html')



def register_view(request):
    if request.method == "POST":
        fullname = request.POST['fullname']
        email = request.POST['email']
        mobile = request.POST['mobile']
        password = request.POST['password']

        if User.objects.filter(username=email).exists():
            return render(request, 'register.html', {'error': 'Email already exists'})

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=fullname
        )

        # Profile.objects.create(
        #     user=user,
        #     mobile=mobile,
        #     role='EMPLOYEE'
        # )

        return redirect('login')

    return render(request, 'register.html')