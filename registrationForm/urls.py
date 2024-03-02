from django.contrib import admin
from django.urls import path
from enroll import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.sign_up, name='signup'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.user_profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('changepassword/', views.user_change_password, 
        name='changepassword'),
    path('changepassword2/', views.user_change_password2, 
        name='changepassword2'),
    path('userdetail/<int:id>', views.user_detail, 
        name='userdetail'),
]
