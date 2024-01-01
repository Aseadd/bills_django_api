from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

class UserManager(BaseUserManager):
    groups = models.ManyToManyField(Group, blank=True)

    def _create_user(self, email, password=None, user_type=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set.")
        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, user_type=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, user_type, **extra_fields)

    def create_superuser(self, email, password=None, user_type=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, user_type, **extra_fields)

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('B', 'Biller'),
        ('A', 'Admin'),
        ('C', 'Customer'),
    )

    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250, unique=True)
    password = models.CharField(max_length=250)
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, default='C')

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'user_type']


    objects = UserManager()

class Biller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Bill(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]
    id = models.AutoField(primary_key=True)
    bill_name = models.CharField(max_length=250)
    bill_amount = models.IntegerField()
    bill_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    biller_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.bill_name} - {self.biller_name} - {self.bill_amount} - {self.bill_date} - {self.status}"

class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=50) 

class Reminder(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reminder_title = models.CharField(max_length=250)
    reminder_date = models.DateField()

    def __str__(self):
        return str(self.reminder_title) + " - " + str(self.reminder_date)
class Report(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_title = models.CharField(max_length=250)
    report_date = models.DateField()

    def __str__(self):
        return str(self.report_title) + " - " + str(self.report_date)


# Create Customer Model
class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    def __str__(self):
        return self.name 

# Create a new group
class CustomPermissions(models.Model):
    class Meta:
        permissions = [
            ("admin_permissions", "Can manage users, system configurations, and overall system settings"),
            ("biller_permissions", "Can create bills, monitor payments, and manage biller-specific settings"),
            ("customer_permissions", "Can view and pay bills, receive reminders, and access payment history"),
        ]

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class SwiftConnection(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    id = models.AutoField(primary_key=True)
    companyName = models.CharField(max_length=255)
    companyAddress: models.CharField(max_length=255)
    contactPhone = models.CharField(max_length=255)
    contactEmail = models.CharField(max_length=255)
    status: models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.companyName


