from django.db import models
from django.core.mail import EmailMultiAlternatives
from mySite import settings
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.

class Job(models.Model):
	STATUS_CHOICES = (("Pending","Pending"),("Approved","Approved"),("Cancle","Cancle"))
	Name=models.CharField(max_length=100)
	Email=models.EmailField()
	JobTitile=models.CharField(max_length=100)
	Location=models.CharField(max_length=1000)
	Salary = models.FloatField()
	Description=RichTextField()
	ApplicationLink=models.CharField(max_length=100)
	CompanyName=models.CharField(max_length=100)
	CompanyWebsite=models.CharField(max_length=100)
	Type=models.CharField(max_length=100,null=True)
	Status=models.CharField(max_length=100, default="Pending", choices=STATUS_CHOICES)
	Is_Featured = models.BooleanField(default=False)
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

	def save(self):
		if self.Status == 'Approved':
			try:
				chkUser = User.objects.get(username=self.Name)
			except:
				password = User.objects.make_random_password()
				subject = f"Job status approved"
				body = "Your job is approved by admin. Your username = "+self.Name+" and password = "+password
				from_email = settings.EMAIL_HOST_USER
				to_email = [self.Email]
				msg = EmailMultiAlternatives(subject, body, from_email, to_email)
				msg.send()
				userObj = User.objects.create_user(username=self.Name, password=password,email=self.Email)
				self.user = userObj
		super().save()

	def __str__(self):
		return self.Name + " | " + self.JobTitile + " | " + self.CompanyName

class Blog(models.Model):
	Titile=models.CharField(max_length=100)
	Description=models.TextField()
	image = models.ImageField(null=True, blank=True, default="default.jpg")

	def __str__(self):
		return self.Titile