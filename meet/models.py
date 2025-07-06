import random
from django.db import models

class UserRegister(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    class_code = models.CharField(max_length=6, unique=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    profile = models.ImageField(upload_to='media/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.class_code:
            self.class_code = self.generate_unique_class_code()
        super().save(*args, **kwargs)

    def generate_unique_class_code(self):
        while True:
            code = str(random.randint(100000, 999999))
            if not UserRegister.objects.filter(class_code=code).exists():
                return code

    def __str__(self):
        return self.username

class Create_classroom(models.Model):
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE, related_name='classrooms')
    title = models.CharField(max_length=100) 
    techer_name = models.CharField(max_length=100)   
    file = models.FileField(upload_to='classroom_files/')
    
    def __str__(self):
        return self.title
class join_classroom(models.Model):
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE, related_name='joined_classrooms')
    classroom = models.ForeignKey(Create_classroom, on_delete=models.CASCADE, related_name='joined_users')
    joined_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    
    

    
    def __str__(self):
        return f"{self.user.username} joined {self.classroom.title}"