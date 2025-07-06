from django.urls import path
from meet.views import *

urlpatterns = [
    path('', home, name='home'),
    path('userRegister/', userRegister, name='userRegister'),
    path('userLogin/', userLogin, name='userLogin'),
    path('logout/', logout, name='logout'),
    path('otp_verify/', otp_verify, name='otp_verify'),
    path('resend_otp/', resend_otp, name='resend_otp'),
    path('dashboard/', dashboard, name='dashboard'),
    path('CreateClassroomForm/', create_classroom, name='CreateClassroomForm'),
    path('search-class/', search_class, name='search_class'),
    path('my-resources/', my_resources, name='my_resources'),
    path('class-code/', class_code, name='class_code'),
    path('mymaterial/', my_material, name='my_material'),
    path('ourteam/', our_team, name='our_team'),
    path('join_classroom/', join_classroom, name='join_classroom'),
    
]