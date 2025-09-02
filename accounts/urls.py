from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path("logout/", views.custom_logout_view, name="logout"),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
]

# URLs dos dashboards (sem namespace para compatibilidade com as views)
from django.urls import path as url_path
from django.urls import include

dashboard_patterns = [
    url_path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    url_path('dashboard/vendedor/', views.dashboard_vendedor, name='dashboard_vendedor'),
    url_path('dashboard/funcionario/', views.dashboard_funcionario, name='dashboard_funcionario'),
]

urlpatterns += dashboard_patterns

