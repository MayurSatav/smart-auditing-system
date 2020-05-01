from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import imaplib
import email
import os

class Invoicelist(models.Model):
    issuer = models.CharField(max_length=50)
    invoice_number = models.CharField(max_length=50)
    date = models.CharField(max_length=50)
    amount = models.IntegerField()
    currency = models.CharField(max_length=10)
    other = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return (self.issuer)

    def get_absolute_url(self):
        return reverse('invoice-detail', kwargs={'pk': self.pk})


def handle_uploaded_file(f):
    with open('invoicedata/static/upload/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def connectionToMail(user,password):

    host = 'imap.gmail.com'
    path = 'invoicedata/static/upload/'
    #print('Connecting to ' + host)
    mailBox = imaplib.IMAP4_SSL(host)
    mailBox.login(user, password)
    boxList = mailBox.list()
    mailBox.select("INBOX")
    searchQuery = '(SUBJECT "Invoice")'
    result, data = mailBox.uid('search', None, "UNSEEN", searchQuery)
    ids = data[0]
    id_list = ids.split()

    i = len(id_list)
    for x in range(i):
        latest_email_uid = id_list[x]
        result, email_data = mailBox.uid('fetch', latest_email_uid, '(RFC822)')

        raw_email = email_data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)
        for part in email_message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            fileName = part.get_filename()

            if bool(fileName):
                filePath = os.path.join(path, fileName)
                if not os.path.isfile(filePath):
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()

    mailBox.close()
    mailBox.logout()
    return "Successful"