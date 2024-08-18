from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignUpForm,AddRecordForm
from .models import Record

def home(request):

    records = Record.objects.all()

    #check to see if logging in
    if request.method == 'POST':
        username = request.POST['username'] #getting the username from the form filled by the user
        password = request.POST['password'] #getting the password from the form filled by the user

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            messages.success(request,'You have been logged in!')
            return redirect('home')
        else:
            messages.success(request, 'There was an error while logging in!')
            return redirect('home')
        
    else:
        return render (request,'home.html',{'records':records})

def logout_user(request):
    logout(request)
    messages.success(request,'You have been logged out!')
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})

def customer_record(request,pk):
    if request.user.is_authenticated:

        record = Record.objects.get(id = pk)
        return render(request, 'record.html', {'record': record})
    
    else:
        messages.success(request, "You Need to be logged into access customer Record!")
        return redirect('home')
    
def delete_record(request,pk):

    if request.user.is_authenticated:
        record = Record.objects.get(id = pk)
        record.delete()
        messages.success(request, "Record deleted Successfully! ")
        return redirect('home')
    
    else:
        messages.success(request, "You Need to be logged into access customer Record!")
        return redirect('home')
    

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request,'Added Record Successfully')
                return redirect('home')
            
        return render(request, 'add_record.html', {'form':form})
    
    else:
        messages.success(request, "You Need to be logged into add records!")
        return redirect('home')
    
def update_record(request,pk):

    if request.user.is_authenticated:
        record = Record.objects.get(id = pk)
        form = AddRecordForm(request.POST or None, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request,'Updated Record Successfully')
            return redirect('home')
        
        return render(request, 'update_record.html', {'form':form})
    
    else:
            messages.success(request, "You Need to be logged into update records!")
            return redirect('home')
                



  



    
    

    





