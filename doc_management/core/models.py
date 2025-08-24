from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must need an email..!")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Super user must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Super user must have is_superuser=True")
        
        return self.create_user(email, password, **extra_fields)
    

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Doctor'),
        ('HOSPITAL_ADMIN', 'Hospital Admin'),
        ('ADMIN', 'Platform Admin'),
        ('BLOOD_DONOR', 'Blood Donor')
    ]
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES, default='PATIENT')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [

    ]

    def __str__(self):
        return f"USER : {self.email}"
    

class PatientProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=5)
    address = models.CharField(max_length=255)
    medical_history = models.TextField(blank=True)
    history_img = models.ImageField(blank=True, null=True, upload_to="Patient_medical_history")

    def __str__(self):
        return f"{self.user.email}"
    

class DoctorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=255) 
    experience = models.PositiveIntegerField(help_text="Years of experience")
    degree = models.CharField(max_length=255)
    availability = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.email}"
    

class HospitalProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.TextField()

    def __str__(self):
        return f"Hospital Name : {self.name}"
    
class Department(models.Model):
    hospital = models.ForeignKey(HospitalProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=155)

    def __str__(self):
        return f"Department Name : {self.name}"
class DonorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    last_donate = models.DateField(null=True, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"Donor Name : {self.user.name}"


    
