from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as auth_logout
from meet.forms import UserRegisterForm, UserLoginForm, OTPVerificationForm  , CreateClassroomForm , ClassroomSearchForm
from meet.models import UserRegister , Create_classroom , join_classroom
import random
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import JsonResponse

# Initialize Gemini with API key at the top of the file




def home(request):
    if 'user_id' not in request.session:
        return redirect('userLogin')
    
    user_id = request.session['user_id']
    user = UserRegister.objects.get(id=user_id)
    
    # Fetch classrooms created by the user
    created_classrooms = Create_classroom.objects.filter(user=user)


    profile = request.session.get('profile')
    username = request.session.get('username')
    full_name = request.session.get('full_name')
    data ={
        'profile': profile,
        'username': username,
        'full_name': full_name,
        'class_code': user.class_code,
    }
    return render(request, 'meet/navbar.html' , {'data': data})

def userRegister(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            gender = form.cleaned_data['gender']
            profile = form.cleaned_data['profile']
            
            # Store form data in session for later use after OTP verification
            request.session['user_registration'] = {
                'full_name': full_name,
                'username': username,
                'email': email,
                'phone': phone,
                'password': password,
                'gender': gender,
                'profile_path': profile.name if profile else None,
            }
            
            # Generate OTP and send email
            return send_otp_mail(request, full_name, username, email, phone, profile)
    else:
        form = UserRegisterForm()
    
    return render(request, 'meet/userRegister.html', {'form': form})


def userLogin(request):
    # Check if user is already logged in
    if 'user_id' in request.session:
        return redirect('home')  # Redirect to home if already logged in
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        
        # For login forms, we don't need to validate against the model
        # Just extract the data from the form
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me') == 'on'
        
        if username and password:
            try:
                # Authenticate user
                user = UserRegister.objects.get(username=username, password=password)
                
                # Store user info in session
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                request.session['full_name'] = user.full_name
                request.session['email'] = user.email
                request.session['profile'] = user.profile.url if user.profile else None
                
                # Set session expiry based on remember_me checkbox
                if not remember_me:
                    # Session expires when browser closes
                    request.session.set_expiry(0)
                
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')  # Redirect to home page after login
            except UserRegister.DoesNotExist:
                messages.error(request, 'Invalid username or password. Please try again.')
                # Return the form with entered username to make it easier for the user
                return render(request, 'meet/userLogin.html', {'form': form})
    else:
        form = UserLoginForm()
    
    return render(request, 'meet/userLogin.html', {'form': form})

def send_otp_mail(request, full_name, username, email, phone, profile):
    try:
        # Generate a 6-digit OTP
        otp = random.randint(100000, 999999)
        
        # Store OTP in session for verification
        request.session['otp'] = otp
        
        email_data = {
            'name': full_name,
            'username': username,
            'email': email,
            'phone': phone,
            'profile': profile,
            'otp': otp,
        }
        
        # Send OTP email to the user
        subject = 'OTP for Meet on Cloude Registration'
        html_message = render_to_string('meet/sendmail.html', {'email_data': email_data})
        from_email = settings.EMAIL_HOST_USER
        to_email = email
        
        # Send mail to user
        msg = EmailMessage(subject, html_message, from_email, [to_email])
        msg.content_subtype = 'html'
        msg.send()
        
        messages.success(request, f'OTP has been sent to {email}')
        
    except Exception as e:
        messages.error(request, f'Email sending failed: {e}')
        return redirect('userRegister')
    
    # Render the OTP verification page
    return redirect('otp_verify')

def otp_verify(request):
    if 'user_registration' not in request.session:
        messages.error(request, 'Please complete registration form first')
        return redirect('userRegister')
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            stored_otp = request.session.get('otp')
            
            if entered_otp == stored_otp:
                # Get user data from session
                user_data = request.session.get('user_registration')
                
                # Create and save user
                user = UserRegister(
                    full_name=user_data['full_name'],
                    username=user_data['username'],
                    email=user_data['email'],
                    phone=user_data['phone'],
                    password=user_data['password'],
                    gender=user_data['gender'],
                    profile=user_data['profile_path']
                )
                user.save()
                
                # Clean up session data
                if 'otp' in request.session:
                    del request.session['otp']
                if 'user_registration' in request.session:
                    del request.session['user_registration']
                
                messages.success(request, f'Account created for {user_data["username"]}! You can now log in.')
                return redirect('userLogin')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
    else:
        form = OTPVerificationForm()
    
    return render(request, 'meet/otp_verify.html', {'form': form})

def resend_otp(request):
    if 'user_registration' not in request.session:
        messages.error(request, 'Registration session expired')
        return redirect('userRegister')
    
    user_data = request.session.get('user_registration')
    
    # Generate new OTP
    otp = random.randint(100000, 999999)
    request.session['otp'] = otp
    
    # Prepare email data
    email_data = {
        'name': user_data['full_name'],
        'username': user_data['username'],
        'email': user_data['email'],
        'otp': otp,
    }
    
    # Send new OTP email
    subject = 'New OTP for Meet on Cloude Registration'
    html_message = render_to_string('meet/sendmail.html', {'email_data': email_data})
    from_email = settings.EMAIL_HOST_USER
    to_email = user_data['email']
    
    try:
        msg = EmailMessage(subject, html_message, from_email, [to_email])
        msg.content_subtype = 'html'
        msg.send()
        messages.success(request, f'New OTP has been sent to {user_data["email"]}')
    except Exception as e:
        messages.error(request, f'Email sending failed: {e}')
    
    return redirect('otp_verify')

def logout(request):
    # Clear all session data
    request.session.flush()
    
    messages.success(request, 'You have been logged out successfully.')
    return redirect('userLogin')

def dashboard(request):
    # Check if user is logged in
    if 'user_id' not in request.session:
        return redirect('userLogin')  # Redirect to login page if not logged in
    
    # Get user data from session
    user_id = request.session['user_id']
    user = UserRegister.objects.get(id=user_id)
    
    data = {
        'email': user.email,
        'phone': user.phone,
        'profile': user.profile.url if user.profile else None,
        'username': user.username,
        'full_name': user.full_name,
    }
    
    return render(request, 'meet/dashboard.html', {'data': data})

def create_classroom(request):
    if 'user_id' not in request.session:
        return redirect('userLogin')

    if request.method == 'POST':
        form = CreateClassroomForm(request.POST, request.FILES)
        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.user = UserRegister.objects.get(id=request.session['user_id'])
            classroom.save()  # You missed this!
            messages.success(request, 'Classroom created successfully!')
            return redirect('dashboard')
    else:
        form = CreateClassroomForm()

    return render(request, 'meet/createclassroom.html', {'form': form})

def search_class(request):
    form = ClassroomSearchForm(request.GET)
    results = []
    
    if form.is_valid() and 'search_query' in request.GET:
        query = form.cleaned_data['search_query']
        if query:
            # Search for teachers
            teacher_results = Create_classroom.objects.filter(
                techer_name__icontains=query
            )
            
            # Search for class codes
            code_results = []
            if len(query) == 6 and query.isdigit():  # Class codes are 6-digit numbers
                try:
                    user = UserRegister.objects.get(class_code=query)
                    code_results = Create_classroom.objects.filter(user=user)
                except UserRegister.DoesNotExist:
                    pass
            
            # Combine results
            results = list(teacher_results) + list(code_results)
    
    context = {
        'form': form,
        'results': results,
        'search_performed': 'search_query' in request.GET
    }
    
    return render(request, 'meet/search-class.html', context)



def my_resources(request):
    if 'user_id' not in request.session:
        return redirect('userLogin')
    
    user_id = request.session['user_id']
    user = UserRegister.objects.get(id=user_id)
    
    # Fetch classrooms created by the user
    created_classrooms = Create_classroom.objects.filter(user=user)
    
    # For future expansion: if you track which classrooms a user has joined
    # joined_classrooms = Create_classroom.objects.filter(members=user)
    
    context = {
        'created_classrooms': created_classrooms,
        # 'joined_classrooms': joined_classrooms,
        'profile': user.profile.url if user.profile else None,
        'username': user.username,
        'full_name': user.full_name,
    }
    
    return render(request, 'meet/myresources.html', context)


def  class_code(request):
    if 'user_id' not in request.session:
        return redirect('userLogin')
    
    user_id = request.session['user_id']
    user = UserRegister.objects.get(id=user_id)
    
    # Fetch classrooms created by the user
    created_classrooms = Create_classroom.objects.filter(user=user)
    
    # For future expansion: if you track which classrooms a user has joined
    # joined_classrooms = Create_classroom.objects.filter(members=user)
    
    context = {
        'created_classrooms': created_classrooms,
        # 'joined_classrooms': joined_classrooms,
        'profile': user.profile.url if user.profile else None,
        'username': user.username,
        'full_name': user.full_name,
        'class_code':user.class_code
     }

    return render(request , 'meet/classroomcode.html' , context)

def my_material(request):
    if 'user_id' not in request.session:
        return redirect('userLogin')
    
    user_id = request.session['user_id']
    user = UserRegister.objects.get(id=user_id)

    # Get all classrooms associated with the user's class code
    try:
        # Fetch all classrooms where the user is either the creator or has the matching class_code
        created_classrooms = Create_classroom.objects.filter(user__class_code=user.class_code)
        
        context = {
            'created_classrooms': created_classrooms,
            'profile': user.profile.url if user.profile else None,
            'username': user.username,
            'full_name': user.full_name,
            'class_code': user.class_code,
            'success': True,
            'message': 'Data fetched successfully'
        }
    except Exception as e:
        context = {
            'success': False,
            'message': f'Error fetching data: {str(e)}',
            'class_code': user.class_code
        }

    return render(request, 'meet/mymaterial.html', context)

def our_team(request):
    return render(request, 'meet/ourteam.html')




    
    
        
        