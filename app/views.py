from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Todoapp
from .forms import taskform
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q


# Create your views here.
@login_required(login_url="/login-register/")
def index(request):
    if request.GET.get("search") is None:
        search=""
    else:
        search=request.GET.get("search")

    todoapp=Todoapp.objects.filter(user__id=request.user.id).filter(Q(title__icontains=search) | Q(description__icontains=search))
    number=Todoapp.objects.filter(user__id=request.user.id).filter(complete=False).count()
    context={
        "todoapp":todoapp,
        "number":number,
    }

    return render(request,"app/index.html",context)

@login_required
def task(request,pk):
    try:

        todoapps=Todoapp.objects.get(id=pk)

        if todoapps is None:
            return HttpResponse("Doesnot exist")
        if request.user.id != todoapps.user.id:
            return HttpResponse("Your are not allowed")
    
        taskforms=taskform(instance=todoapps)



        if request.method=="POST":
            taskforms=taskform(request.POST, instance=todoapps)
            if taskforms.is_valid():
                taskforms.save()
                return redirect("index")
    
        context={
        "todoapp":taskforms
        }

        return render(request,"app/task.html",context)
    except:
        return HttpResponse("Doesnot exist")

@login_required
def delete_task(request,pk):
        todoapps=Todoapp.objects.get(id=pk)


        if request.method=="POST":
             todoapps.delete()

             return redirect("index")
        

        
        
        return render(request,"app/delete.html")


def loginPage(request):
     message=""
 
     if request.method=="POST":
          username=request.POST.get("username")
          password=request.POST.get("password")
          try:
              user=User.objects.get(username=username)
              if user is not None :
                  user=authenticate(request, username=username, password=password)
 
                  if user is not None:
                    print("its also working")      
                    login(request, user)
                    return redirect("index")
              else:
                message= "password is wrong"

          except:
               message="username or password is incorrect"

     context={
          "message":message,
          "page":"login",
     }
     return render(request, "app/login_register.html",context)

@login_required
def logoutPage(request):
    logout(request)
    return redirect("index")
                   
def registerPage(request):
    userform=UserCreationForm()

    if request.method=="POST":
        userform=UserCreationForm(request.POST)
        if userform.is_valid:
            user=userform.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request, user)
            return redirect("index")
    context={
        "userform":userform
    }
    return render(request, "app/login_register.html", context)
     





@login_required
def create_task(request):
      taskforms=taskform()
      
      
      if request.method=="POST":
        taskforms=taskform(request.POST)
        if taskforms.is_valid():
            form=taskforms.save(commit=False)
            form.user=request.user
            form.save()
            return redirect("index")
    
      context={
        "todoapp":taskforms
       }

      return render(request,"app/create.html",context)



