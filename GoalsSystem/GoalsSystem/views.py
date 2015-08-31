from django.shortcuts import render
from django.db import connection
from django.template import RequestContext
from django.http import HttpResponseRedirect
from datetime import datetime,date,timedelta
import json
from django.db.models import Q

from GoalsSystem.models import Goal
# Create your views here.


# HttpResponses of views.
def Login(request):
	if(request.method == "POST"):
		userName = request.POST['username']
		password = request.POST['password']
		validating = ValidateUser(userName,password)
		if(validating == True):
			templateName = "/Goals/"
			return HttpResponseRedirect(templateName)
		else:
			templateName = "GoalsSystem/Login.html"
	else:
		templateName = "GoalsSystem/Login.html"
	return render(request,templateName,context_instance=RequestContext(request))

def Home(request):
	goals = Goal.objects.all()
	return render(request,"GoalsSystem/Home.html",{'goals':goals})

def Goals(request):
	todayDate = str(datetime.now().date())
	yesterdayDate=str(date.today()-timedelta(days=1))
	goals = Goal.objects.filter(created__contains=todayDate)
	#goals = Goal.objects.all()
	yesterDayGoals=Goal.objects.filter(created__contains=yesterdayDate).filter(~Q(status=2))
	return render(request,"GoalsSystem/Goals.html",{'goals' : goals,'pendingGoals':yesterDayGoals})

def UpdateGoal(request):
	goals = []	
	if(request.POST):
		goalId = request.POST["id"]
		description = request.POST["description"]
		remarks = request.POST["remarks"]
		status = request.POST["status"]
		goals = Goal.objects.filter(id__contains=goalId).update(description=description,remarks=remarks,status=status,lastupdated=datetime.now())		
	else:
		goals=[]
	return render(request,"GoalsSystem/AddedGoals.html")

def AddGoal(request):
	if(request.POST):
		description = request.POST["description"]
		remarks = request.POST["remarks"]
		status = request.POST["status"]
		newGoal = Goal(description=description,remarks=remarks,isactive=0)
		newGoal.created = datetime.now()
		newGoal.lastupdated = datetime.now()
		newGoal.status = status
		newGoal.save()
		id = newGoal.id
	return render(request,"GoalsSystem/AddedGoals.html",{'id':id})


def  LoadGoalsAccordingToDate(request):
	goals = []
	if(request.GET):
		dateTime = str(request.GET['dateTime'])
		goals = Goal.objects.filter(created__contains=dateTime).filter(status=2)
		#goals = json.dumps(goals)
	return render(request,"GoalsSystem/LoadGoalsAccordingToDate.html",{'goals' : goals,'goalStatus' : "goals"})

def LoadPedingGoalsAccordingToDate(request):
	goals = []
	if(request.GET):
		duration = int(request.GET['range'])
		if(duration==0):
			allPendingGoals = []
			allPendingGoals = Goal.objects.filter(~Q(status=2))
			goals = allPendingGoals
		elif(duration==1):
			yesterdayDate = str(date.today() - timedelta(days=1))
			yesterdayPendingGoals = Goal.objects.filter(created__contains=yesterdayDate).filter(~Q(status=2)).order_by("-created")
			goals = yesterdayPendingGoals
		elif(duration==2):
			currentDate = str(date.today())
			lastweekDate = str(date.today() - timedelta(days=7))
			lastWeekPendingGoals = Goal.objects.filter(created__gte=lastweekDate).filter(created__lt=currentDate).filter(~Q(status=2)).order_by("-created")
			goals = lastWeekPendingGoals
		elif(duration==3):
			lastMonthPendingGoals = []
			currentDate = str(date.today())
			lastMonthDate = str(GetPastMonthDates(date.today(),1))
			lastMonthPendingGoals = Goal.objects.filter(created__gte=lastMonthDate).filter(created__lt=currentDate).filter(~Q(status=2)).order_by("-created")
			goals = lastMonthPendingGoals
		elif(duration==4):
			lastThreeMonthsPendingGoals = []
			requiredDate = str(GetPastMonthDates(date.today(),3))
			currentDate = str(date.today())
			lastThreeMonthsPendingGoals = Goal.objects.filter(created__gte=requiredDate).filter(created__lt=currentDate).filter(~Q(status=2)).order_by("-created")
			goals = lastThreeMonthsPendingGoals
		elif(duration==5):
			lastSixMonthsPendingGoals = []
			currentDate = str(date.today())
			requiredDate = str(GetPastMonthDates(date.today(),6))
			lastSixMonthsPendingGoals = Goal.objects.filter(created__gte=requiredDate).filter(created__lt=currentDate).filter(~Q(status=2)).order_by("-created")
			goals = lastSixMonthsPendingGoals
	return render(request,"GoalsSystem/LoadGoalsAccordingToDate.html",{ 'goalStatus' : "pendingGoals",'goals':goals})


# User Defined Functions.
def ValidateUser(userName ,password):
	validUser = False
	if(len(userName) <=0 or len(password) <= 0):
		return validUser
	cursor = connection.cursor()
	cursor.execute("select * from login where username = %s and password = %s", (userName,password))
	userList = cursor.fetchall()
	if(userList):
		validUser = True
	return validUser

def GetPastMonthDates(currentDate,months):
	currentDay = currentDate.day
	currentMonth = currentDate.month
	currentYear = currentDate.year
	resultingMonth = currentMonth - months
	if(resultingMonth <= 0):
		currentYear -= 1
		currentMonth = resultingMonth + 12
	else:
		currentMonth = resultingMonth
	import calendar
	resultingDays = calendar.monthrange(currentYear,currentMonth)[1]
	if(resultingDays < currentDay):
		currentDay = resultingDays
	return date(currentYear,currentMonth,1)

"""
class StaticClassExample():	
	#@static_var(counter=0)
	counter=0
	#@staticmethod
	#def InitializeCount():
		#global counter
		#StaticClassExample.counter = 1
		
	@staticmethod
	def CheckStaticMethod():
		StaticClassExample.counter = StaticClassExample.counter + 1
		print(StaticClassExample.counter)
"""