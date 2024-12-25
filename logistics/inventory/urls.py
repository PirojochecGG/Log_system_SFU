from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('prihod/', views.prihod, name='prihod'),
    path('rashod/', views.rashod, name='rashod'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('products/', views.products_view, name='products'),
    path('products/search/', views.search_products, name='search_products'),
    path('get_products_by_operation/<int:operation_id>/', views.get_products_by_operation, name='get_products_by_operation'),
    path('add_product/', views.add_product, name='add_product'),
    path('generate_reports/generate_pdf_report/', views.generate_pdf_report, name='generate_pdf_report'),
    path('generate_reports/generate_excel_report/', views.generate_excel_report, name='generate_excel_report'),
    path('generate_reports/', views.generate_reports_view, name='generate_reports'),
]

