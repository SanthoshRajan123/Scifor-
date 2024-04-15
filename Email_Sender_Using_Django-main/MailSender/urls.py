from django.urls import path
from . import views
from django.urls import include, path
from MailSender.views import index, process_upload,send_email
urlpatterns = [
    path('',views.index,name='index'),
    path('process_upload',views.process_upload, name='process_upload'),
    path('send_email/', views.send_email, name='send_email'),
]
