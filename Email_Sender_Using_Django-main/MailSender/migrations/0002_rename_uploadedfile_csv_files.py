# Generated by Django 4.0.4 on 2023-07-01 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MailSender', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UploadedFile',
            new_name='CSV_files',
        ),
    ]
