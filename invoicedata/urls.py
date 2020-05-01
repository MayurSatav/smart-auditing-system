from django.urls import path
from .views import (
    InvoiceListView,
    InvoiceDetailView,
    InvoiceCreateView,
    InvoiceUpdateView,
    InvoiceDeleteView,
    CompleteView,
    extractinvoice,
    graphView,
    graph,
    graphViewMonthly,
    graphMonthly
)
from . import views



urlpatterns = [
    path('', InvoiceListView.as_view(), name='invoicedata-home'),
    path('invoice/<int:pk>/', InvoiceDetailView.as_view(), name='invoice-detail'),
    path('invoice/new/', InvoiceCreateView.as_view(), name='invoice-create'),
    path('invoice/<int:pk>/update/', InvoiceUpdateView.as_view(), name='invoice-update'),
    path('invoice/<int:pk>/delete/', InvoiceDeleteView.as_view(), name='invoice-delete'),
    
    path('completeview/', CompleteView.as_view(), name='invoicedata-complete'),
    path('filter/', views.filter, name='invoicedata-filter'),
    path('filter1/', views.filter1, name='invoicedata-filter1'),
    path('filter2/', views.filter2, name='invoicedata-filter2'),
    path('search/', views.search, name='invoicedata-search'),
    path('extractinvoice/', views.extractinvoice, name='invoicedata-extractinvoice'),
    path('about/', views.about, name='invoicedata-about'),

    #mail
    path('checkMail/', views.checkMail, name='invoicedata-checkMail'),
    path('checkme/', views.checkme, name='invoicedata-checkme'),
    path('showdownloadedFile/', views.showdownloadedFile, name='invoicedata-showdownloadedFile'),
    path('savef/', views.savef, name='invoicedata-savef'),
    path('mailExtract/', views.mailExtract, name='invoicedata-mailExtract'),
    path('export_users_xls/', views.export_users_xls, name='invoicedata-export_users_xls'),

    path('invoice/graphView/', graphView.as_view(), name='invoice-graphView'),
    path('invoice/graph/', graph.as_view(), name='invoice-graph'),
    path('invoice/graphViewMonthly/', graphViewMonthly.as_view(), name='invoice-graphViewMonthly'),
    path('invoice/graphMonthly/', graphMonthly.as_view(), name='invoice-graphMonthly'),

]