from django.urls import path
from .views import *
urlpatterns = [
    path('',dashboard,name="dashboard"),
    path('add-attandents',addAttandents,name="add_attandents"),
    path('attandents-report',attandentsReport,name="attandents_Report"),
    path('view-attandents-report/',viewattandentsreport,name="view_attandents_Report"),
    path('add-products',addProducts,name="add_products"),
    path('product-report',productsReport,name="product_report"),
    path('add-employee',addEmployee,name="add_employee"),
    path('add-company',addCompany,name="add_company"),
    path('employee-list',employeeList,name="employee_list"),
    path('company-list',companyList,name="company_list"),
    path('add-delivery',addDelivery,name="add_delivery"),
    path('get-piz/', get_piz_by_art, name='get_piz'),
    path('delivery-report',deliveryReport,name="delivery_report"),
    path('add-invoice/', add_invoice, name='add_invoice'),
    path('invoice/<int:invoice_id>/', invoice_detail, name='invoice_detail'),
    path('invoice-list/', invoice_list, name='invoice_list'),
   path('ajax/get-deliveries/<int:company_id>/', ajax_get_deliveries, name='ajax_get_deliveries'),
]
