from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_worker = models.BooleanField(default = False)
    is_approved = models.BooleanField(default = False)
    is_declined = models.BooleanField(default = False)
    email = models.EmailField(max_length = 1000, null = False, unique=True)
    profile_pic = models.ImageField(upload_to="images/")
    is_profile_set = models.BooleanField(default = False)
    cnic = models.CharField(max_length = 20, null = True, blank = True)
    phone = models.CharField(max_length = 20, null = True, blank = True)
    address = models.CharField(max_length = 1000, null = True, blank = True)
    
    @property
    def get_profile_pic(self):
        
        if self.profile_pic:
            print(self.profile_pic.url)
            return self.profile_pic.url
        else:
            return ""
    
class WorkerProfileModel(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="worker_profile")
    cnic_front = models.ImageField(upload_to="images/", null = True)
    cnic_back = models.ImageField(upload_to="images/", null = True)
    experience = models.CharField(max_length = 200, null = True, blank = True)
    profession = models.CharField(max_length = 200, null = True, blank = True)
    about = models.CharField(max_length = 200, null = True, blank = True)
    
    @property
    def get_cnic_front(self):
        
        if self.cnic_front:
            return self.cnic_front.url
        else:
            return ""
    @property
    def get_cnic_back(self):
        
        if self.cnic_back:
            return self.cnic_back.url
        else:
            return ""
    
    
    
    
    