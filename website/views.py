from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

#import registration form
from .forms import SignUpForm

#import for record showing
from .models import Record

#import for record creation
from .forms import AddRecordForm

# Create your views here.

def home(request):

    #Take all records
    records = Record.objects.all()



    # Check to see if logging in

    if request.method == 'POST':
        username = request.POST['username'] #name property of respective field
        password = request.POST['password']

        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been Logged In")
            return redirect('home')
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again ...")
            return redirect('home')

    else:
        return render(request, 'home.html', {'records': records}) #reply to user's request


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')


def register_user(request):

    if request.method == 'POST':
        
        form = SignUpForm(request.POST)
        if (form.is_valid()):
            form.save()

            #auth and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)

            login(request, user)
            messages.success(request, "You Have Successfully Registered and Logged In")
            return redirect('home')

    else:
        form = SignUpForm()

        return render(request, 'register.html', {'form': form}) #reply to user's request
    
    return render(request, 'register.html', {'form': form})

def customer_record(request, pk):

    if request.user.is_authenticated :
         #Lookup the record

        customer_record = Record.objects.get(id=pk)

        return render(request, 'record.html', { 'customer_record': customer_record } )

    else:
        #Unauthorized access
        messages.success(request, "You Must Be Logged In To View That Page")
        return redirect('home')


def delete_record(request, pk):

    if request.user.is_authenticated:

        delete_it = Record.objects.get(id = pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully")
        return redirect('home')
    else:
        messages.success(request, "You Must Be Logged In To Do That Action")
        return redirect('home')


def add_record(request):
        
    form = AddRecordForm(request.POST or None)

    if request.user.is_authenticated:

        if request.method == "POST":

            if form.is_valid():

                add_record = form.save()
                messages.success(request, "Record Added Successfully")
                return redirect('home')

        return render(request, 'add_record.html', {'form': form} )
    

    else:
        messages.success(request, "You Must Be Logged In To Do That Action")
        return redirect('home')

def update_record(request, pk):

    if request.user.is_authenticated:

        current_record = Record.objects.get(id = pk)
        form = AddRecordForm(request.POST or None, instance=current_record)

        if request.method == "POST":

            if form.is_valid():

                form.save()
                messages.success(request, "Record Updated Successfully")
                return redirect('home')
            

        return render(request, 'update_record.html', {'form': form} )

       
       
    else:
        messages.success(request, "You Must Be Logged In To Do That Action")
        return redirect('home')