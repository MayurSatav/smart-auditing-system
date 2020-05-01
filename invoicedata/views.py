from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Invoicelist, handle_uploaded_file
from .forms import browse
from invoice2data import extract_data
import os
from .models import connectionToMail as tf
import imaplib
import xlwt

from django.core.paginator import Paginator

from django.views import View
from rest_framework.views import APIView
from rest_framework.response import  Response
from django.db.models import Sum, Count

'''def home(request):
    context = {'invoices': Invoicelist.objects.all()}
    return render(request, 'invoicedata/home.html', context)'''

class InvoiceListView(LoginRequiredMixin,ListView):
    model = Invoicelist
    template_name = 'invoicedata/home.html'
    context_object_name = 'invoices'
    
    def get_queryset(self):
        return self.model.objects.all().filter(author=self.request.user).order_by('-date_posted')[:4]

class InvoiceDetailView(DetailView):
    model = Invoicelist
    

class InvoiceCreateView(LoginRequiredMixin, CreateView):

    model = Invoicelist
    fields = ['issuer','invoice_number','date','amount','currency','other']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class InvoiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Invoicelist
    fields = ['issuer','invoice_number','date','amount','currency','other']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        invoice = self.get_object()
        if self.request.user == invoice.author:
            return True
        return False

class InvoiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Invoicelist
    success_url = '/'

    def test_func(self):
        invoice = self.get_object()
        if self.request.user == invoice.author:
            return True
        return False

def Invoicecompleteview(request):
    a = Invoicelist.objects.values('issuer').distinct().aggregate(Count('issuer'))
    b = Invoicelist.objects.all().aggregate(Sum('amount'))
    total_author = a["issuer__count"]
    total_amount = b["amount__sum"]
    c = Invoicelist.objects.values('amount').distinct().aggregate(Count('amount'))
    amount_count = c['amount__count']
    
    contact_list=Invoicelist.objects.filter(author=request.user)
    paginator = Paginator(contact_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'invoices': page_obj,'total_amount':total_amount,'total_author':total_author,'total_count':amount_count}
    
    return render(request, 'invoicedata/completeview.html', context)

    


'''class CompleteView(LoginRequiredMixin,ListView):
    model = Invoicelist
    template_name = 'invoicedata/completeview.html'
    context_object_name = 'invoices'
    
    def get_queryset(self):
        return self.model.objects.all().filter(author=self.request.user).order_by('-date_posted')'''

def filter(request):
    if request.method == "GET":
        company=request.GET['company']
        fi=company[0].upper()+company[1:]
        a=Invoicelist.objects.filter(author=request.user)
        newl = []
        for i in a:
            if i.issuer == company or i.issuer == fi:
                newl.append(i)

    return render(request, 'invoicedata/completeview.html', {'invoices': newl})

def filter1(request):
    if request.method == "GET":
        amount=request.GET['amount']
        a = Invoicelist.objects.filter(author=request.user)
        newl = []
        for i in a:
            if int(i.amount) >= int(amount):
                newl.append(i)

    return render(request, 'invoicedata/completeview.html', {'invoices': newl})

def filter2(request):
    if request.method == "GET":
        currency=request.GET['currency']
        a=Invoicelist.objects.filter(author=request.user)
        newl = []
        for i in a:
            if i.currency == currency:
                newl.append(i)

    return render(request, 'invoicedata/completeview.html', {'invoices': newl})


def search(request):
    if request.method == "GET":
        company=request.GET['company']
        fi=company[0].upper()+company[1:]
        a=Invoicelist.objects.all()
        newl = []
        for i in a:
            if (company in i.issuer) or (fi in i.issuer) :
                newl.append(i)

    return render(request, 'invoicedata/completeview.html', {'invoices': newl})

#Data-extraction-------------------------------------------------------------------------------------------------
def Reverse(lst): 
    return [ele for ele in reversed(lst)] 

file_list = os.listdir("invoicedata/static/upload/")
def extractinvoice(request):
    result = None
    form = None
    if request.method == 'POST':  
        form = browse(request.POST, request.FILES)  
        if form.is_valid():  
            handle_uploaded_file(request.FILES['file']) # store file in upload folder
            path = "invoicedata/static/upload/"+ str(request.FILES['file'])#path of selected file
            result = extract_data(path) # extract data from file
            print(result)
            fields=['issuer','invoice_number','date','amount','currency']
            alist = []
            other = []
            for i in result:
                if i in fields:
                    print(i)
                    if  i == 'issuer':
                        alist.insert(0,result[i])
                    elif i == 'invoice_number':
                        alist.insert(1,result[i])
                    elif i == 'date':
                        alist.insert(2,result[i])
                    elif i == 'amount':
                        alist.insert(3,result[i])
                    elif i == 'currency':
                        alist.insert(4,result[i])
                    else:
                        pass
                else:
                    temp = str(str(i) + "-" + str(result[i]))
                    other.append(temp)
                

            nalist = alist
            
            nother = Reverse(other)
            print(nalist)
            print(nother)

            p = Invoicelist(issuer = nalist[0],invoice_number = nalist[1], amount = nalist[2], date = nalist[3] , currency = nalist[4], other = nother,author = request.user)
            p.save()
    else:
        form = browse()
    context = {"form": form, "result": result}
    return render(request,'invoicedata/extractdata.html', context)    

#---------------------------------------------------------------------------------------
#Mail------------------------------------------------------------------------------------
def checkMail(request):
    return render(request, 'invoicedata/mailEntry.html')

def checkme(request):

    if request.method == "GET":
        user=request.GET['mailid']
        password=request.GET['password']
        a = tf(user, password)
        flist = []
        path = 'invoicedata/static/upload/'

        for file in os.listdir(path):
            flist.append(file)

        return render(request, 'invoicedata/showdownloadedFile1.html', {"flist": flist})


def showdownloadedFile(request):
    import os
    import sys
    path = 'invoicedata/static/upload/'
    i=0
    for file in os.listdir(path):
        current = os.path.join(path, file)
        if os.path.isfile(current):
            data = open(current, "rb")
            len1 = len(data.read())
            data.close()
            os.remove(current)
        i+=1
        break
    if i == 0:
        len1 = "No invoice present to extract"

    return render(request, 'invoicedata/showdownloadedFile1.html', {"len": len1})

def savef(request):
    if request.method == "POST":
        issuer=request.POST['issuer']
        invoice_number = request.POST['invoice_number']
        amount = request.POST['amount']
        date = request.POST['date']
        currency = request.POST['currency']
        other = request.POST['other']
        p = Invoicelist(issuer=issuer, invoice_number=invoice_number, date=date, amount=amount,currency=currency, other=other, author=request.user)
        p.save()

    return render(request, 'invoicedata/home.html')

#-----------------------------------------------------------------------------------------


def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Issuer', 'Invoice Number', 'Date', 'Amount', 'Currency', 'Other' ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Invoicelist.objects.filter(author=request.user).values_list('issuer', 'invoice_number', 'date', 'amount', 'currency', 'other')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


#graph--------------------------------------------------------


class graphView(View):
    def get(self, request):
        return render(request, 'invoicedata/completeview.html')

class graph(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        #usernames = [user.username for user in User.objects.all()]
        a = Invoicelist.objects.filter(date__range=["2020-01-01", "2020-01-30"]).aggregate(Sum('amount'))["amount__sum"]
        b = Invoicelist.objects.filter(date__range=["2020-02-01", "2020-02-30"]).aggregate(Sum('amount'))["amount__sum"]
        c = Invoicelist.objects.filter(date__range=["2020-03-01", "2020-03-30"]).aggregate(Sum('amount'))["amount__sum"]
        d = Invoicelist.objects.filter(date__range=["2020-04-01", "2020-04-30"]).aggregate(Sum('amount'))["amount__sum"]
        e = Invoicelist.objects.filter(date__range=["2020-05-01", "2020-05-30"]).aggregate(Sum('amount'))["amount__sum"]
        f = Invoicelist.objects.filter(date__range=["2020-06-01", "2020-06-30"]).aggregate(Sum('amount'))["amount__sum"]
        g = Invoicelist.objects.filter(date__range=["2020-07-01", "2020-07-30"]).aggregate(Sum('amount'))["amount__sum"]
        h = Invoicelist.objects.filter(date__range=["2020-08-01", "2020-08-30"]).aggregate(Sum('amount'))["amount__sum"]
        i = Invoicelist.objects.filter(date__range=["2020-09-01", "2020-09-30"]).aggregate(Sum('amount'))["amount__sum"]
        j = Invoicelist.objects.filter(date__range=["2020-10-01", "2020-10-30"]).aggregate(Sum('amount'))["amount__sum"]
        k = Invoicelist.objects.filter(date__range=["2020-11-01", "2020-11-30"]).aggregate(Sum('amount'))["amount__sum"]
        l = Invoicelist.objects.filter(date__range=["2020-12-01", "2020-12-30"]).aggregate(Sum('amount'))["amount__sum"]

        default_item=[a,b,c,d,e,f,g,h,i,j,k,l]
        month=["January","February","March","April","May","June","July","August","September","October","November","December"]

        pie_chart=Invoicelist.objects.values('issuer').annotate(Sum('amount'))
        pie_label=[]
        pie_data=[]
        for i in pie_chart:
            pie_label.append(i["issuer"])
            pie_data.append(i["amount__sum"])


        noi=Invoicelist.objects.values('issuer').annotate(num=Count('issuer'))
        noi_label = []
        noi_data = []
        for i in noi:
            noi_label.append(i["issuer"])
            noi_data.append(i["num"])




        data={"labels":month,
              "default":default_item,
              "pie_label": pie_label,
              "pie_data": pie_data,
              "noi_label": noi_label,
              "noi_data": noi_data,
        }
        return Response(data)


##################################################################
class graphViewMonthly(View):
    def get(self, request):
        if request.method == "GET":
            month = request.GET['submit']
            return render(request, 'invoicedata/graphMonthly.html',{"a":month})

class graphMonthly(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        query1 = Invoicelist.objects.values('date').annotate(Sum('amount'))
        label = []
        data1 = []

        for i in query1:
            label.append(i["date"])
            data1.append(i["amount__sum"])


        pie_chart = Invoicelist.objects.filter(date__range=["2020-01-01", "2020-01-31"]).values('issuer').annotate(Sum('amount'))
        jan_label = []
        jan_data = []
        for i in pie_chart:
            jan_label.append(i["issuer"])
            jan_data.append(i["amount__sum"])

        pie_chart1 = Invoicelist.objects.filter(date__range=["2020-02-01", "2020-02-29"]).values('issuer').annotate(Sum('amount'))
        feb_label = []
        feb_data = []
        for i in pie_chart1:
            jan_label.append(i["issuer"])
            jan_data.append(i["amount__sum"])

        pie_chart2 = Invoicelist.objects.filter(date__range=["2020-03-01", "2020-03-31"]).values('issuer').annotate(Sum('amount'))
        mar_label = []
        mar_data = []
        for i in pie_chart2:
            mar_label.append(i["issuer"])
            mar_data.append(i["amount__sum"])

        pie_chart3 = Invoicelist.objects.filter(date__range=["2020-04-01", "2020-04-31"]).values('issuer').annotate(Sum('amount'))
        apr_label = []
        apr_data = []
        for i in pie_chart3:
            apr_label.append(i["issuer"])
            apr_data.append(i["amount__sum"])

        pie_chart4 = Invoicelist.objects.filter(date__range=["2020-05-01", "2020-05-31"]).values('issuer').annotate(Sum('amount'))
        may_label = []
        may_data = []

        for i in pie_chart4:
            may_label.append(i["issuer"])
            may_data.append(i["amount__sum"])

        pie_chart5 = Invoicelist.objects.filter(date__range=["2020-06-01", "2020-06-31"]).values('issuer').annotate(Sum('amount'))
        jun_label = []
        jun_data = []

        for i in pie_chart5:
            jun_label.append(i["issuer"])
            jun_data.append(i["amount__sum"])

        pie_chart6 = Invoicelist.objects.filter(date__range=["2020-07-01", "2020-07-31"]).values('issuer').annotate(
            Sum('amount'))
        jul_label = []
        jul_data = []

        for i in pie_chart6:
            jul_label.append(i["issuer"])
            jul_data.append(i["amount__sum"])

        pie_chart7 = Invoicelist.objects.filter(date__range=["2020-08-01", "2020-08-31"]).values('issuer').annotate(
            Sum('amount'))
        aug_label = []
        aug_data = []

        for i in pie_chart7:
            aug_label.append(i["issuer"])
            aug_data.append(i["amount__sum"])

        pie_chart8 = Invoicelist.objects.filter(date__range=["2020-09-01", "2020-09-31"]).values('issuer').annotate(
            Sum('amount'))
        sep_label = []
        sep_data = []

        for i in pie_chart8:
            sep_label.append(i["issuer"])
            sep_data.append(i["amount__sum"])

        pie_chart9 = Invoicelist.objects.filter(date__range=["2020-10-01", "2020-10-31"]).values('issuer').annotate(
            Sum('amount'))
        oct_label = []
        oct_data = []

        for i in pie_chart9:
            oct_label.append(i["issuer"])
            oct_data.append(i["amount__sum"])

        pie_chart10 = Invoicelist.objects.filter(date__range=["2020-11-01", "2020-11-31"]).values('issuer').annotate(
            Sum('amount'))
        nov_label = []
        nov_data = []

        for i in pie_chart10:
            nov_label.append(i["issuer"])
            nov_data.append(i["amount__sum"])

        pie_chart11 = Invoicelist.objects.filter(date__range=["2020-12-01", "2020-12-31"]).values('issuer').annotate(
            Sum('amount'))
        dec_label = []
        dec_data = []

        for i in pie_chart11:
            dec_label.append(i["issuer"])
            dec_data.append(i["amount__sum"])

        data={"labels":label,
              "data1":data1,
              "jan_data":jan_data,
              "jab_label":jan_label,
              "feb_data": feb_data,
              "feb_label": feb_label,
              "mar_data": mar_data,
              "mar_label": mar_label,
              "apr_data": apr_data,
              "apr_label": apr_label,
              "may_data": may_data,
              "may_label": may_label,
              "jun_data": jun_data,
              "jun_label": jun_label,
              "jul_data": jul_data,
              "jul_label": jun_label,
              "aug_data": aug_data,
              "aug_label": aug_label,
              "sep_data": sep_data,
              "sep_label": sep_label,
              "oct_data": oct_data,
              "oct_label": oct_label,
              "nov_data": nov_data,
              "nov_label": nov_label,
              "dec_data": dec_data,
              "dec_label": dec_label

        }
       
        return Response(data)


#------------------------------------------------------------
file_list = os.listdir("invoicedata/static/upload/")
def mailExtract(request):
    result = None
    form = None
    if request.method == 'POST':  
        form = browse(request.POST, request.FILES)  
        if form.is_valid():  
            handle_uploaded_file(request.FILES['file']) # store file in upload folder
            path = "invoicedata/static/upload/"+ str(request.FILES['file'])#path of selected file
            result = extract_data(path) # extract data from file
            print(result)
            fields=['issuer','invoice_number','date','amount','currency']
            alist = []
            other = []
            for i in result:
                if i in fields:
                    print(i)
                    if  i == 'issuer':
                        alist.insert(0,result[i])
                    elif i == 'invoice_number':
                        alist.insert(1,result[i])
                    elif i == 'date':
                        alist.insert(2,result[i])
                    elif i == 'amount':
                        alist.insert(3,result[i])
                    elif i == 'currency':
                        alist.insert(4,result[i])
                    else:
                        pass
                else:
                    temp = str(str(i) + "-" + str(result[i]))
                    other.append(temp)
                

            nalist = alist
            
            nother = Reverse(other)
            print(nalist)
            print(nother)

            p = Invoicelist(issuer = nalist[0],invoice_number = nalist[1], amount = nalist[2], date = nalist[3] , currency = nalist[4], other = nother,author = request.user)
            p.save()
    else:
        form = browse()
    context = {"form": form, "result": result}
    return render(request,'invoicedata/showdownloadedFile1.html', context)



def about(request):
    return render(request, 'invoicedata/about.html', {'title': 'About'})