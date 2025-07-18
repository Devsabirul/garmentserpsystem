from datetime import datetime
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.http import JsonResponse
from django.contrib import messages
from django.utils.crypto import get_random_string
from datetime import date

def dashboard(request):
    if request.user.is_authenticated:
        employeeLenth = Employees.objects.all()
        companyLength = Companies.objects.all()
        productLength = Products.objects.all()
        return render(request,'core/index.html',locals())
    else:
        return redirect('signin')


def addAttandents(request):
    if not request.user.is_authenticated:
        return redirect('signin')

    employeeList = Employees.objects.all()
    error = None
    success = None

    if request.method == "POST":
        employee_id = request.POST.get('employee_id')
        date = request.POST.get('date')
        entry = request.POST.get('entry')
        out = request.POST.get('out')
        total_hour = request.POST.get('total_hour')

        try:
            employee = Employees.objects.get(id=employee_id)
        except Employees.DoesNotExist:
            return render(request, 'core/add_attandents.html', {
                'employeeList': employeeList,
                'error': 'Invalid employee selected.'
            })

        # Optional: Use employee.name if you still need name in a separate field
        name = employee.name

        if Atandents.objects.filter(employee=employee, date=date).exists():
            error = "Attendance for this employee and date already exists."
        else:
            attandent = Atandents(
                name=name,
                employee=employee,
                date=date,
                entry=entry,
                out=out,
                total_hour=total_hour,
                author=request.user,
            )
            attandent.save()
            success = "Attendance saved successfully."

    return render(request, 'core/add_attandents.html', {
        'employeeList': employeeList,
        'error': error,
        'success': success
    })

    
def attandentsReport(request):
     if request.user.is_authenticated:
        attandentsReport = Atandents.objects.order_by("-id")
        return render(request,'core/attandents_report.html',locals())
     else:
        return redirect('signin')

def viewattandentsreport(request):
    if not request.user.is_authenticated:
        return redirect('signin')

    attandent_id = request.GET.get('id')
    date_str = request.GET.get('date')

    if not attandent_id or not date_str:
        return render(request, 'core/error.html', {'message': 'Missing id or date parameter'})

    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return render(request, 'core/error.html', {'message': 'Invalid date format'})

    year = date_obj.year

    # Filter attendance records by employee ID and year (using startswith on CharField)
    records = Atandents.objects.filter(
        employee__id=attandent_id,
        date__startswith=f"{year}-"
    ).order_by('date')

    # Sum total hours
    total_hours = sum(rec.total_hour for rec in records if rec.total_hour)

    # Optional: sanitize empty fields
    for rec in records:
        rec.entry = rec.entry or ''
        rec.out = rec.out or ''
        rec.total_hour = rec.total_hour or 0

    context = {
        'attandentsReport': records,
        'total_hours': total_hours
    }

    return render(request, 'core/view_report.html', context)

    
def addProducts(request):
    if not request.user.is_authenticated:
        return redirect('signin')

    companyList = Companies.objects.all()
    error = None
    success = None

    if request.method == "POST":
        date = request.POST.get('date')
        art = request.POST.get('art')
        piz = request.POST.get('piz')
        price = request.POST.get('price')
        delivery_date = request.POST.get('delivery_date')
        company_name_str = request.POST.get('company_name')

        try:
            company_instance = Companies.objects.get(name=company_name_str)
        except Companies.DoesNotExist:
            error = f"Company '{company_name_str}' does not exist."
            return render(request, 'core/add_products.html', {
                'companyList': companyList,
                'error': error,
                'success': success
            })

        product = Products.objects.create(
            date=date,
            art=art,
            piz=piz,
            price=price,
            delivery_date=delivery_date,
            company_name=company_instance
        )
        product.save()
        success = "Product added successfully."

    return render(request, 'core/add_products.html', {
        'companyList': companyList,
        'error': error,
        'success': success
    })

def addEmployee(request):
    if not request.user.is_authenticated:
        return redirect('signin')

    error = None
    success = None

    if request.method == "POST":
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        position = request.POST.get('position')
        hourlyrate = request.POST.get('hourlyrate')

        try:
            employee = Employees.objects.create(
                name=name,
                phone_number=phone_number,
                address=address,
                position=position,
                hourlyrate=hourlyrate,
            )
            employee.save()
            success = "Employee added successfully."
        except:
            error = "Something wrong, Please try again!"


    return render(request, 'core/add_employee.html', {
        'error': error,
        'success': success
    })

def addCompany(request):
    if not request.user.is_authenticated:
        return redirect('signin')

    error = None
    success = None

    if request.method == "POST":
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_num')
        address = request.POST.get('address')
        

        try:
            company = Companies.objects.create(
                name=name,
                phone_num=phone_number,
                address=address,   
            )
            company.save()
            success = "Company added successfully."
        except:
            error = "Something wrong, Please try again!"


    return render(request, 'core/add_company.html', {
        'error': error,
        'success': success
    })


def productsReport(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    productsList = Products.objects.all()

    return render(request, 'core/product_report.html',locals())

def employeeList(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    employees = Employees.objects.all()

    return render(request, 'core/employeeList.html',locals())


def companyList(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    companys = Companies.objects.all()

    return render(request, 'core/companyList.html',locals())


def addDelivery(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    productlist = Products.objects.all()
    error = None
    success = None

    if request.method == "POST":
        date = request.POST.get('date')
        art = request.POST.get('art')
        piz = request.POST.get('piz')
        price = request.POST.get('price')

        product = Products.objects.get(art=art)

        delivery = ProductDelivery.objects.create(
            date=date,
            product=product,
            piz=piz,
            total_price=price,
        )
        delivery.save()
        success = "Deivery product added successfully."

    return render(request, 'core/add_delivery.html', {
        'productlist': productlist,
        'success': success
    })


def get_piz_by_art(request):
    art = request.GET.get('art')
    try:
        product = Products.objects.get(art=art)
        return JsonResponse({'piz': product.piz,'price':product.price})
    except Products.DoesNotExist:
        return JsonResponse({'piz': '','price':0})
    
def deliveryReport(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    delivery = ProductDelivery.objects.all()

    return render(request, 'core/delivery_report.html',locals())


def add_invoice(request):
    companies = Companies.objects.all()
    deliveries = ProductDelivery.objects.all()

    if request.method == 'POST':
        company_id = request.POST.get('company')
        delivery_ids = request.POST.getlist('deliveries')

        if not company_id or not delivery_ids:
            messages.error(request, "Please select a company and at least one delivery product.")
            return redirect('add_invoice')

        company = Companies.objects.get(id=company_id)
        invoice_number = get_random_string(length=8).upper()
        invoice = Invoice.objects.create(
            company=company,
            date=date.today(),
            invoice_number=invoice_number
        )

        for delivery_id in delivery_ids:
            delivery = ProductDelivery.objects.get(id=delivery_id)
            InvoiceItem.objects.create(invoice=invoice, delivery=delivery)

        messages.success(request, f"Invoice {invoice_number} created successfully.")
        return redirect('invoice_detail', invoice_id=invoice.id)

    return render(request, 'core/add_invoice.html', {
        'companies': companies,
        'deliveries': deliveries
    })

def invoice_detail(request, invoice_id):
    invoice = InvoiceItem.objects.filter(invoice__id=invoice_id)

    return render(request, 'core/invoice_detail.html', {
        'invoice': invoice,
    })

def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, 'core/invoice_list.html', {'invoices': invoices})


def ajax_get_deliveries(request, company_id):
    deliveries = ProductDelivery.objects.filter(product__company_name__id=company_id)
    data = []


    for d in deliveries:
        data.append({
            'id': d.id,
            'date': d.date,
            'piz': d.piz,
            'total_price': d.total_price,
            'product_art': d.product.art,
            'company_name': d.product.company_name.name,
        })

    print(data)

    return JsonResponse({'deliveries': data})