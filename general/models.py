from email.policy import default
from random import choices
from django.db import models
from django.contrib.auth.models import User
from django.forms import DateTimeField, DateTimeInput, DurationField

# Create your models here.
class Employee(models.Model):

    # gender
    Male = 'M'
    Female = 'F'
    gender = [(Male, 'Male'),(Female, 'Female')]


# job-description
    Manager="Site Manager"
    AsstManager="Asst. Manager"
    Supervisor="Supervisor"
    QM ="Quality Marshal"
    FC="Pump Attendant"
    SHOP="Shop Attendant"
    Cleaner="Cleaner"
    Security="Security"
    Driver="Driver"
    Technician="Lube Technician"
    Specialist="Oil Specialist"

    group = [("management",'management'),('staff','staff'),('trainee','trainee')]

    job = [ 
          (Manager, 'Site Manager'),
          (AsstManager, 'Asst. Manager'),
          (Supervisor, 'Supervisor'),
          (QM, "Quality Marshal"),
          (FC, "Pump Attendant"),
          (SHOP, "Shop Attendant"),
          (Cleaner,"Cleaner"),
          (Security,"Security"),
          (Driver,"Driver"),
          (Technician,"Lube Technician"),
          (Specialist," Oil Specialist"),
          ]

    username = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    fullname = models.CharField('Full Name', max_length=30)
    gender = models.CharField('Gender', choices=gender,  max_length=7)
    contact = models.CharField('Contact', max_length=10, null=True, blank=True)
    dob = models.DateField('Date of birth', null=True, blank=True)
    loc = models.CharField('Location', max_length=20, null=True, blank=True)
    gname = models.CharField("Guarantor's Name", max_length=30, null=True,blank=True)
    gcontact = models.CharField("Guarantor's contact", max_length=10, null=True,blank=True)
    job = models.CharField('Job Description', choices=job, max_length=30, null=True,blank=True)
    date_employed = models.DateField('Year Employed', null=True, blank=True)
    ssnit = models.CharField('Ssnit Number', max_length=15, null=True, blank=True)
    bank = models.CharField('Account Number', max_length=15, null=True, blank=True)
    group = models.CharField('Group', max_length=20, choices=group)
    def get_list(self):
        return [self.gender, self.fullname]
    



class MsgSent(models.Model):
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=3000)
    sent_by = models.ForeignKey(User,related_name='by', on_delete=models.CASCADE)
    sent_to = models.ForeignKey(User,related_name='to', on_delete=models.CASCADE, null=True, blank=True)
    date_sent=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.subject
    
    def get_name(self):
        return self.sent_by.first_name
    
    



class Letters(models.Model):
    # letters
    Permission="Permission"
    Warning="Verbal Warning"
    Suspension="Suspension"
    Dismissal ="Dismissal"
    Query="Query Letter"
    
    authority = [('Manager','Manager'),('Supervisor',"Supervisor"),('QM','Quality Marshal')]

    letters = [ 
          (Permission, 'Permission'),
          (Warning, 'Verbal Warning'),
          (Suspension, 'Suspension'),
          (Dismissal, "Dismissal"),
          (Query, "Query Letter"),          
          ]

    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField('Action',max_length=30, choices=letters)
    description = models.TextField('Description',max_length=1000)
    date = models.DateField(auto_now_add=True)
    authorized = models.CharField('Given by', choices=authority, max_length=30)
    start_from = models.DateField('Start From',blank=True, null=True)
    end = models.DateField('Ending',blank=True, null=True)
    file = models.FileField(upload_to ='LtrsFiles/')
    objects = models.Manager()

    def __str__(self):
        return self.action
    
    

class Resources(models.Model):
    lst = [('Accreditation','Accreditation'),('Appraisal','Appraisal'),('Resource','Resource') ]


    filename = models.CharField('File Name',max_length=20)
    file = models.FileField(upload_to ='RscFiles/')
    filetype = models.CharField(max_length=20, choices=lst, default='Resource')
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.filename    
