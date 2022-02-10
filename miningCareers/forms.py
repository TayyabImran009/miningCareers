from django import forms
from django.db.models import fields
from django.forms import ModelForm
from django import forms
from .models import*

class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ['Name', 'Email', 'JobTitile', 'Location', 'Salary', 'Description', 'ApplicationLink', 'CompanyName', 'CompanyWebsite']

class AddJobForm(ModelForm):
    class Meta:
        model = Job
        fields = ['JobTitile', 'Location', 'Salary', 'Description', 'ApplicationLink', 'CompanyName', 'CompanyWebsite']