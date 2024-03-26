from django.shortcuts import render, redirect
from .models import *

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate

# Create your views here.

def Homepage(request):
  return  render(request, 'Website/homepage.html')

def SearchPros(request):
  return  render(request, 'Website/Search_pros.html')
def SearchProject(request):
  return  render(request, 'Website/Search_project.html')


def LoginPage(request):
  error = ""
  email = None
  if request.method == "POST":
    email = request.POST.get("email")
    password = request.POST.get("password")
    
    
    if User.objects.filter(username = email).exists():
      user = User.objects.get(username = email)
      user_data = authenticate(username= email, password = password)
      if user_data is not None:
        auth_login(request, user_data)  
        if user.is_superuser:
          return redirect("admindashboard")
        elif user.is_worker:
          return redirect("workerdashboard")
        else:
          return redirect("clientdashboard")
        
      else:
        error = "Invalid password"
    else:
        error = "Invalid Username or password"
      
      
  return  render(request, 'Website/Login.html', {'error':error, 'email':email})


def logout(request):
  auth_logout(request)
  
  return redirect('homepage')
  
def SignUpPage(request):
  form = request.POST
  error = {}
  if request.method == "POST":
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    email = request.POST.get("email")
    password = request.POST.get("password")
    confirm_password = request.POST.get("password2")
    account_type = request.POST.get('account_type')
    
    if len(password) < 8:
      error['password'] = "Password must be 8 or more characters long"
    elif password != confirm_password:
      error['password2'] = "Password do not match"
    elif User.objects.filter(email = email).exists():
      error["email"] = "Email already exists"
    
    else:
      user_instance = User.objects.create(
        email = email,
        username = email,
        first_name = first_name,
        last_name = last_name,
        is_worker = account_type == "worker"
        )
      user_instance.set_password(password)
      user_instance.save()
      
      if account_type == "worker":
        WorkerProfileModel.objects.create(user = user_instance)
      
      return redirect('login')
      
  return  render(request, 'Website/Signup.html', {"form":form, 'error':error})

def ResetPassword(request):
  return  render(request, 'Website/ResetPassword.html')
# Admin

def AdminDashboard(request):
  if not request.user.is_authenticated:
    return redirect('login')
  if request.user.is_superuser:
    
    workers = User.objects.filter(is_worker = True, is_approved = False, is_profile_set=True)
    clients = User.objects.filter(is_worker = False, is_approved = False, is_superuser = False)
    
    return  render(request, 'Admin/AdminDashboard.html',{"worker_requests":workers, "clients":clients})
  elif request.user.is_worker:
    return redirect("workerdashboard")
  else:
    return redirect("clientdashboard")
  

def acceptRejectUser(request):
  if request.method == "POST":
    
    id = request.POST.get('worker_id')
    if User.objects.filter(id = id).exists():
      user = User.objects.get(id = id)
      status = request.POST.get("status")
      print(status)
      if status == "Accept":
        user.is_approved = True
      else:
        user.is_declined = True
      
      user.save()
      print(user)
      print(status, id)

  return redirect('admindashboard')

def RecentMembers(request):
  members = User.objects.filter(is_worker = False, is_superuser = False).order_by('-id')
  return  render(request, 'Admin/RecentMembers.html', {"members":members})
def RecentWorkers(request):
  
  members = User.objects.filter(is_worker = True).order_by('-id')
  return  render(request, 'Admin/RecentWorkers.html',{"workers":members})
def RecentWorkersDetail(request):
  return  render(request, 'Admin/RecentWorkerDetail.html')
# def RecentMembersDetail(request):
#   return  render(request, 'Admin/RecentMemberDetail.html')

# Worker

def WorkerDashboard(request):
  if not request.user.is_profile_set:
    return redirect("editworkerprofile")
  
  
  return  render(request, 'Worker/WorkerDashboard.html')
def WorkerSample(request):
  samples = WorkerSampleProject.objects.filter(user = request.user)

  return  render(request, 'Worker/Workersamples.html', {'samples':samples})
def AddWorkerSample(request):
  if request.method == "POST":
    title = request.POST.get('project-title')
    budget = request.POST.get('project-budget')
    desc = request.POST.get('project-desc')
    days = request.POST.get('project-days')
    thumbnail = request.FILES.get('thumbnail')
    images = request.FILES.getlist('sample_images')

    work_sample = WorkerSampleProject.objects.create(
                      budget = budget,
                      title = title,
                      description = desc,
                      completed_days = days,
                      thumbnail = thumbnail,
                      user = User.objects.get(id = request.user.id)
                    )
    work_sample.save()
    for img in images:
      SampleProjectImages.objects.create(image = img, project = work_sample)




  return  render(request, 'Worker/AddWorkSamples.html')
def WorkerProfile(request):
  
  user = User.objects.get(id = request.user.id)
  return  render(request, 'Worker/Profile.html', {'user':user})


def EditWorkerProfile(request):
  if request.method == "POST":
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    phone = request.POST.get("phone")
    address = request.POST.get("address")
    profession = request.POST.get("profession")
    experience = request.POST.get("experience")
    cnic = request.POST.get("cnic")
    
    profile_pic = request.FILES.get("profile_pic")
    cnic_front = request.FILES.get("cnic_front")
    cnic_back = request.FILES.get("cnic_back")
    
    
    print(request.FILES)  
    
    user = User.objects.get(id = request.user.id)
    worker_instance = WorkerProfileModel.objects.get(user = user)
    
    user.first_name = first_name
    user.last_name = last_name
    user.phone = phone
    user.address = address
    user.cnic = cnic
    
    worker_instance.experience = experience
    worker_instance.profession = profession
    
    if profile_pic:
      user.profile_pic = profile_pic
      
    if cnic_front:
      worker_instance.cnic_front = cnic_front
    if cnic_back:
      worker_instance.cnic_back = cnic_back
    
    user.is_profile_set = True
    
    user.save()
    worker_instance.save()
    
    
  
  user = User.objects.get(id = request.user.id)
    
  return  render(request, 'Worker/EditProfile.html', {"user":user})

# Client
def ClientDashboard(request):
  return  render(request, 'Client/Dashboard.html')
def ShowJobs(request):
  return  render(request, 'Client/PostJob.html')
def AddJob(request):
  return  render(request, 'Client/AddJob.html')
def ClientProfile(request):
  return  render(request, 'Client/Profile.html')
def EditClientProfile(request):
  return  render(request, 'Client/EditProfile.html')
