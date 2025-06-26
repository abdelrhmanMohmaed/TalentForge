from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
import uuid

# Create your models here.
# Manager for our Custom User Model
class CustomUserManager(BaseUserManager):
    def create_user(self, email, EED, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not EED:
            raise ValueError('The EED field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, EED=EED, **extra_fields)
        
        # If password is not provided, generate a random one (for admin creation scenario)
        if password:
            user.set_password(password)
        else:
            # Generate a random password here. This will be sent via email later.
            # For simplicity, let's just set a placeholder for now.
            # In a real app, you'd use a strong random string generator.
            temp_password = BaseUserManager().make_random_password()
            user.set_password(temp_password)
            user.temp_generated_password = temp_password # Store for email sending later if needed
            print(f"DEBUG: Generated password for {email}: {temp_password}") # For debugging only, remove in production!

        user.save(using=self._db)
        return user

    def create_superuser(self, email, EED, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True) # Superuser should be active by default

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, EED, password, **extra_fields)

# Role Model
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    EED = models.CharField(max_length=255, unique=True) # Assuming string for flexibility

    # Optional fields (can be null/blank initially)
    name = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    # Status and timestamps
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # Required for Django Admin access
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Field used for authentication (login)
    REQUIRED_FIELDS = ['EED'] # Fields required when creating a user via createsuperuser command

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'   
        verbose_name_plural = 'Users'

# UserRoleProject (Pivot table for User-Role-Project)
class Project(models.Model):
    # This is a placeholder for the Project model.
    # In a real scenario, you'd define its actual fields.
    # For now, just a name will suffice for the foreign key.
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class UserRoleProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True) # Nullable until assigned

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures a user has a specific role for a specific project only once
        unique_together = ('user', 'role', 'project')
        verbose_name = 'User Project Role'
        verbose_name_plural = 'User Project Roles'

    def __str__(self):
        project_name = self.project.name if self.project else "No Project"
        return f"{self.user.email} - {self.role.name} - {project_name}"