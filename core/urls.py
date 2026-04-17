from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Auth
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Modules
    path('documents/', views.document_list, name='document_list'),
    path('documents/delete/<int:pk>/', views.delete_document, name='delete_document'),
    
    path('expenses/', views.expense_list, name='expense_list'),
    
    path('reminders/', views.reminder_list, name='reminder_list'),
    
    path('subscriptions/', views.subscription_list, name='subscription_list'),
    
    path('emergency/', views.emergency_mode, name='emergency_mode'),
]
