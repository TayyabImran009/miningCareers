from multiprocessing import context
from django.shortcuts import render, redirect
from .forms import JobForm, AddJobForm
from .models import Job, Blog
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.

def home(request):
	if request.method == 'POST':
		jobName = request.POST.get('jobName')
		jobLocation = request.POST.get('jobLocation')
		if jobName != "":
			try:
				jobObj = Job.objects.filter(JobTitile=jobName, Is_Featured=True)
			except:
				jobObj = ""
			context = {
				'jobObj':jobObj,
				'jobName':jobName,
				'jobLocation':jobLocation
			}
			return render(request,'miningCareers/index.html',context)
		elif jobLocation != "":
			try:
				jobObj = Job.objects.filter(Location=jobLocation, Is_Featured=True)
			except:
				jobObj = ""
			context = {
					'jobObj':jobObj,
					'jobName':jobName,
					'jobLocation':jobLocation
				}
			return render(request,'miningCareers/index.html',context)
			
	jobObj = Job.objects.filter(Is_Featured=True)
	
	page = request.GET.get('page')
	results = 10
	paginator = Paginator(jobObj, results)

	try:
		jobObj = paginator.page(page)
	except PageNotAnInteger:
		page = 1
		jobObj = paginator.page(page)
	except EmptyPage:
		page = paginator.num_pages
	context = {
		'jobObj':jobObj,
		'paginator':paginator
	}
	return render(request,'miningCareers/index.html',context)

def postJob(request):
	form = JobForm()
	if request.method == 'POST':
		form = JobForm(request.POST)
		if form.is_valid():
			jobs = form.save(commit=False)
			try:
				user = User.objects.get(username=jobs.Name)
				context = {
					'msg':'username already exists'
				}
				return render(request,'miningCareers/postJob.html',context)
			except User.DoesNotExist:
				try:
					user = User.objects.get(email=jobs.Email)
					context = {
					'msg':'email already exists'
					}
					return render(request,'miningCareers/postJob.html',context)
				except User.DoesNotExist:
					form.save()
					context = {
					'msg':'Job post successfully'
					}
					return render(request,'miningCareers/postJob.html',context)
		else:
			print(form.errors)
	return render(request,'miningCareers/postJob.html')

def jobs(request):

	if request.method == 'POST':
		jobName = request.POST.get('jobName')
		jobLocation = request.POST.get('jobLocation')
		if jobName != "":
			try:
				jobObj = Job.objects.filter(JobTitile=jobName)
			except:
				jobObj = ""
			context = {
				'jobObj':jobObj,
				'jobName':jobName,
				'jobLocation':jobLocation
			}
			return render(request,'miningCareers/index.html',context)
		elif jobLocation != "":
			try:
				jobObj = Job.objects.filter(Location=jobLocation)
			except:
				jobObj = ""
			context = {
					'jobObj':jobObj,
					'jobName':jobName,
					'jobLocation':jobLocation
				}
			return render(request,'miningCareers/index.html',context)

	jobObj = Job.objects.all()
	page = request.GET.get('page')
	results = 10
	paginator = Paginator(jobObj, results)

	try:
		jobObj = paginator.page(page)
	except PageNotAnInteger:
		page = 1
		jobObj = paginator.page(page)
	except EmptyPage:
		page = paginator.num_pages
	context = {
		'jobObj':jobObj,
		'paginator':paginator
	}
	return render(request,'miningCareers/jobs.html',context)

def jobDetails(request,pk):
	jobObj = Job.objects.get(id=pk)
	context = {
		'jobObj':jobObj
	}
	return render(request,'miningCareers/jobDetails.html',context)

def blogs(request):
	blogObj = Blog.objects.all()
	if len(blogObj) != 0:
		lastObj = blogObj[len(blogObj) -1]
	else:
		lastObj=""
	page = request.GET.get('page')
	results = 10
	paginator = Paginator(blogObj, results)

	try:
		blogObj = paginator.page(page)
	except PageNotAnInteger:
		page = 1
		blogObj = paginator.page(page)
	except EmptyPage:
		page = paginator.num_pages
	context = {
		'blogObj':blogObj,
		'paginator':paginator,
		'lastObj':lastObj
	}
	return render(request,'miningCareers/blogs.html',context)

def blogDetail(request,pk):

	blogObj = Blog.objects.get(id=pk)
	context = {
		'blogObj':blogObj
	}
	
	return render(request,'miningCareers/detailBlog.html',context)

def signIn(request):
	if request.user.is_authenticated:
		return redirect('home')
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		try:
			user = User.objects.get(username=username)
		except:
			msg="Username is incorrect"
			constext = {
				'msg':msg
			}
			return render(request,'miningCareers/login.html',constext)

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('profile')
		else:
			msg="Password is incorrect"
			constext = {
				'msg':msg
			}
			return render(request,'miningCareers/login.html',constext)
	return render(request,'miningCareers/login.html')

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url="login")
def editJob(request,pk):
	jobObj = Job.objects.get(id=pk)
	form = JobForm(instance=jobObj)
	if request.method == 'POST':
		form = JobForm(request.POST,instance=jobObj)
		if form.is_valid():
			form.save()
			return redirect('profile')
		else:
			print(form.errors)
	context = {'jobObj': jobObj}
	return render(request,'miningCareers/editJob.html',context)

@login_required(login_url="login")
def profile(request):
	jobObj = Job.objects.filter(user=request.user)
	page = request.GET.get('page')
	results = 10
	paginator = Paginator(jobObj, results)

	try:
		jobObj = paginator.page(page)
	except PageNotAnInteger:
		page = 1
		jobObj = paginator.page(page)
	except EmptyPage:
		page = paginator.num_pages
	context = {
		'jobObj':jobObj,
		'paginator':paginator
	}
	context = {'jobObj': jobObj}
	return render(request,'miningCareers/profile.html',context)

@login_required(login_url="login")
def addJob(request):
	form = AddJobForm()
	if request.method == 'POST':
		form = AddJobForm(request.POST)
		if form.is_valid():
			jobs = form.save(commit=False)
			jobs.Name = request.user.username
			jobs.Email = request.user.email
			jobs.user = request.user
			jobs.save()
			return redirect('profile')
		else:
			print(form.errors)
	return render(request,'miningCareers/addJob.html')