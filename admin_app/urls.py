from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.HomePage, name="home-page"),
    path('register/', views.Register, name="register-page"),
    path('login/', views.perform_Login, name="login-page"),
    path('logout/', views.logoutuser, name='logout'),
    path('', views.perform_Login, name="login-page"),
    path('test/', views.test, name='test'),
    path('admin_login/', views.admin_login, name='admin-login'),
    path('admin_access/', views.admin_access, name='admin-access'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin_logout/', views.logoutadmin, name='admin-logout'),
    # path('userform/', views.userform, name='user-form'),
    path('create_user/', views.create, name='create'),
    # path('updateform/', views.updateform, name='update-form'),
    path('update/<int:user_id>', views.update, name='update'),
    path('delete/<int:user_id>', views.delete, name='delete-user'),
    path('search/', views.search, name='search')
]
