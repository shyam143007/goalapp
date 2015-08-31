from django.db import models
from datetime import date

# Create your models here.
class Employee(models.Model):
	ID = models.AutoField(db_column = 'ID', primary_key = True)
	EmployeeID = models.CharField(db_column = 'EmployeeID', max_length = 20,null = False)
	FirstName = models.CharField(db_column = 'FirstName',max_length = 50,null = False)
	MiddleName = models.CharField(db_column = 'MiddleName' ,max_length = 50) 
	LastName = models.CharField(db_column = 'LastName' ,max_length = 50 ,null = False)
	Gender = models.IntegerField(db_column = 'Gender' ,null = False)
	Nationality = models.CharField(db_column = 'Nationality' ,max_length = 15,null = False)
	MaritalStatus = models.IntegerField(db_column = 'MaritalStatus' ,null = False ,default = '0')
	DateOfBirth = models.DateTimeField(db_column = 'DateOfBirth' ,null = False)
	PAN = models.CharField(db_column = 'PAN' ,max_length = 20, null = True,default = "")
	AadhaarCard = models.CharField(db_column = 'AadhaarCard' ,max_length = 50)
	PassportNo = models.CharField(db_column = 'PassportNo' ,max_length = 20)
	DataRowVersion = models.IntegerField(db_column = 'DataRowVersion'  ,null = False ,default ='0')
	IsActive = models.IntegerField(db_column = 'IsActive' ,null = False ,default = '0')
	Created = models.DateTimeField(db_column = 'Created')
	LastUpdated = models.DateTimeField(db_column = 'LastUpdated')
	
	class META:		
		db_table = "employees"



class Goal(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', max_length=255, blank=True, null=True)  # Field name made lowercase.
    created = models.DateTimeField(db_column='Created', blank=True, null=True)  # Field name made lowercase.
    closed = models.DateTimeField(db_column='Closed', blank=True, null=True)  # Field name made lowercase.
    lastupdated = models.DateTimeField(db_column='LastUpdated', blank=True, null=True)  # Field name made lowercase.
    isactive = models.IntegerField(db_column='IsActive')  # Field name made lowercase.
    createdby = models.IntegerField(db_column='CreatedBy', blank=True, null=True)  # Field name made lowercase.
    assignedto = models.IntegerField(db_column='AssignedTo', blank=True, null=True)  # Field name made lowercase.
    islongterm = models.IntegerField(db_column='IsLongTerm', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'goals'


class Login(models.Model):
	Id = models.IntegerField(db_column = 'Id')
	Username = models.CharField(db_column ='Username', max_length = 20, default = "")
	Password = models.CharField(db_column ='Password', max_length= 20, default = "")
	class META:		
		db_table = "login"
		