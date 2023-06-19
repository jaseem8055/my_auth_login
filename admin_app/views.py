from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control, never_cache

from django.contrib.auth.models import User

from django.contrib import messages

from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('dashboard')
    return render(request, 'admin_login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_access(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('dashboard')
    
    if request.method == 'POST':
        admin_name = request.POST.get('uname')
        admin_password = request.POST.get('pass')

        user_obj = authenticate(request, username=admin_name, password=admin_password)
        if user_obj is not None:
            if user_obj.is_superuser:
                login(request, user_obj)
                return redirect('dashboard')
        else:            
            # return HttpResponse('Error, user does not exist')
            # Error = "Username or Password is Invalid!"
            # return render(request, 'admin_login.html', {'Error': Error})
            messages.error(request, "Username or Password is Invalid! Try again with Superuser credentials!")
            return render(request, 'admin_login.html')
            # return HttpResponseRedirect('/')
    return render(request, 'admin_login.html', {})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            login_user = request.user.username
            # context = {'login_user' : login_user}
            users_data=User.objects.all()
            return render(request,'admin_dashboard.html', {'users':users_data, 'login_user' : login_user})

            # return render(request, 'admin_dashboard.html', context)
    return render(request,'admin_login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logoutadmin(request):
    logout(request)

    # Clear session data
    request.session.flush()

    # Delete session cookie
    response = redirect('admin-login')
    response.delete_cookie('sessionid')
    return response

    # return redirect('admin-login')

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def userform(request):
#     return render(request, 'createuser.html')

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def create(request):    
    if not request.user.is_authenticated:
        return render(request,'admin_login.html')
    
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == 'POST':
                uname=request.POST['uname']
                email=request.POST['email']
                password1=request.POST['pass']
                password2=request.POST['pass2']

                try:
                    is_super = request.POST['is_superuser']
                except:
                    is_super = False
                
                if not uname or not email or not password1 or not password2:
                    return render(request, 'createuser.html', {'error': 'Please fill in all fields.'})
                
                if User.objects.filter(username=uname).exists():
                    return render(request, 'createuser.html', {'error': 'Username already exists. Please choose a different username.'})
                
                if User.objects.filter(email=email).exists():
                    return render(request, 'createuser.html', {'error': 'Email already exists. Please choose a different Email.'})

                try:
                    validate_email(email)
                except ValidationError:
                    return render(request, 'createuser.html', {'error': 'Invalid Email address'})

                try:
                    validate_password(password1)
                except ValidationError as e:
                    return render(request, 'createuser.html', {'error': ','.join(e.messages)})

                # if username.strip() == '' or password1.strip() == '' or password2.strip() == '':
                #     messages.error(request,"fields cannot be empty")
                #     return redirect('create')
                if password1 != password2 :
                    return render(request, 'createuser.html', {'error': 'Password does not match!'})
                    # messages.error(request,'password doesnt match' )
                    # return redirect('create')
                
                user=User.objects.create_user(username=uname,email=email,password=password1)

                if is_super:
                    user.is_superuser=True

                user.save()
                # messages.success(request,'User has been created succesfully')
                return redirect('dashboard')
            return render(request,'createuser.html')
        else: return render(request,'admin_login.html')
# def updateform(request):
#     return render(request, 'update.html')


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def update(request, user_id):    
    if not request.user.is_authenticated:
        return render(request,'admin_login.html')
    
    if request.user.is_authenticated:
        if request.user.is_superuser:
            user=User.objects.get(id=user_id)

            if request.method == 'POST':

                uname=request.POST['uname']
                email=request.POST['email']
                password1=request.POST['pass']
                password2=request.POST['pass2']
                # password=request.POST['password']

                try:
                    is_super = request.POST['is_superuser']
                except:
                    is_super = False
                
                if not uname or not email or not password1 or not password2:
                    return render(request, 'createuser.html', {'error': 'Please fill in all fields.'})
                        
                try:
                    validate_email(email)
                except ValidationError:
                    return render(request, 'createuser.html', {'error': 'Invalid Email address'})

                try:
                    validate_password(password1)
                except ValidationError as e:
                    return render(request, 'createuser.html', {'error': ','.join(e.messages)})

                if password1 != password2 :
                    return render(request, 'createuser.html', {'error': 'Password does not match!'})        
                
                user.username=uname
                user.email=email
                user.set_password(password1)

                if is_super:
                    user.is_superuser=True

                user.save()
                # messages.success(request,'updated successfully')
                return redirect('dashboard')
            return render(request,'update.html',{'user':user})
    
        else: return render(request,'admin_login.html')


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def delete(request,user_id):    
    if not request.user.is_authenticated:
        return render(request,'admin_login.html')
    
    if request.user.is_authenticated:
        if request.user.is_superuser:
            user=User.objects.get(id=user_id)

            user.delete()

            return redirect('dashboard')
        else: return render(request,'admin_login.html')

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def search(request):
    if not request.user.is_authenticated:
        return render(request,'admin_login.html')

    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == 'GET':
                query = request.GET.get('search_query')
                
                if query:
                    detail=User.objects.filter(username__startswith=query)
                    # detail=User.objects.filter(username=query)
                    return render(request,'search.html',{'details':detail})
                else:
                    return render(request, 'search.html',{})

        else: return render(request,'admin_login.html')


# @login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def HomePage(request):
    if request.user.is_authenticated:
        login_user = request.user.username
        context = {'login_user' : login_user}
        return render(request, 'index.html', context)    
    return render(request, 'login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Register(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('sname')
        name = request.POST.get('uname')
        email = request.POST.get('email')
        password = request.POST.get('pass')

        if not fname or not lname or not name or not email or not password:
            return render(request, 'register.html', {'error': 'Please fill in all fields.'})
        
        if User.objects.filter(username=name).exists():
            return render(request, 'register.html', {'error': 'Username already exists. Please choose a different username.'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already exists. Please choose a different Email.'})

        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'register.html', {'error': 'Invalid Email address'})

        try:
            validate_password(password)
        except ValidationError as e:
            return render(request, 'register.html', {'error': ','.join(e.messages)})

        new_user = User.objects.create_user(name, email, password)
        new_user.first_name = fname
        new_user.last_name = lname

        new_user.save()
        Success = "Account has been successfully created! Signin with your credential!"
        return render(request, 'login.html', {'Success': Success})
        # messages.success(request,'Account has been successfully created')
        # return redirect('login-page', {'Success' : 'Account has been successfully created'})
  
    return render(request, 'register.html', {})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def perform_Login(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    
    if request.method == 'POST':
        name = request.POST.get('uname')
        password = request.POST.get('pass')

        user_obj = authenticate(request, username=name, password=password)
        if user_obj is not None:
            login(request, user_obj)
            return redirect('home-page')
        else:            
            # return HttpResponse('Error, user does not exist')
            Error = "Username or Password is Invalid!"
            return render(request, 'login.html', {'Error': Error})
            # messages.error(request, "Error : Username or Password is Invalid!")
            # return redirect(request, 'login.html')
            # return HttpResponseRedirect('/')


    return render(request, 'login.html', {})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logoutuser(request):
    logout(request)
    return redirect('login-page')


def test(request):
    return render(request, 'test.html', {})


