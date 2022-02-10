from django.contrib import admin
from django.urls import path

from .import views

urlpatterns = [
    path('',views.home,name="home"),
    path('postJob/',views.postJob,name="postJob"),
    path('jobs/',views.jobs,name="jobs"),
    path('jobDetails/<int:pk>/',views.jobDetails,name="jobDetails"),

    path('blogs/',views.blogs,name="blogs"),
    path('blogDetail/<int:pk>/',views.blogDetail,name="blogDetail"),

    path('login/',views.signIn,name="login"),
    path('logout/',views.logoutUser,name="logout"),

    path('profile/',views.profile,name="profile"),

    path('editJob/<int:pk>/',views.editJob,name="editJob"),

    path('addJob/',views.addJob,name="addJob"),
]