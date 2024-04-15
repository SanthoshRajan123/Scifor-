from django.db import IntegrityError
from django.http import HttpResponse
from .models import Uploaded_File
from django.shortcuts import render
import csv
import io
from django.core.mail import send_mail
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from EmailApp.settings import EMAIL_HOST_USER


def index(request):
    return render(request, 'UploadPage.html')

def process_upload(request):
    if request.method == 'POST' and request.FILES.get('csvFile'):
        uploaded_file = request.FILES['csvFile']
        file_name = uploaded_file.name
        try:
            uploaded_file = Uploaded_File(
                file_name=file_name,
                file_content=uploaded_file.read(),
            )
            uploaded_file.save()  # Save the uploaded file to the database
        except IntegrityError:
            return HttpResponse("Error: Failed to save file.")

        valid_emails, invalid_emails = handler(uploaded_file.file_content)

        return render(request, 'email_results.html', {'valid_emails': valid_emails,'invalid_emails': invalid_emails})
    else:
        return HttpResponse("No file uploaded.")


def send_email(request):
    if request.method == 'POST':
        valid_emails = request.POST.get('valid_emails')
        emails_list = valid_emails.split(',')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        send_mail(subject, message, EMAIL_HOST_USER, emails_list, fail_silently=False)

        return HttpResponse("Emails sent successfully!")
    else:
        return HttpResponse("Failed to Send Mail")


def handler(file_content):
    # Parse the CSV file content
    email_addresses = []
    csv_reader = csv.reader(io.StringIO(file_content.decode()))
    for row in csv_reader:
        # Assuming the email addresses are in the first column of the CSV
        email = row[0]
        email_addresses.append(email)

    # Validate email addresses
    valid_emails = []
    invalid_emails = []
    email_validator = EmailValidator()

    for email in email_addresses:
        try:
            email_validator(email)
            valid_emails.append(email)
        except ValidationError:
            invalid_emails.append(email)

    return valid_emails, invalid_emails