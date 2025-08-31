from django.urls import path
from . import views

app_name = 'familia'

urlpatterns = [
    path('', views.FamiliaListView.as_view(), name='list'),
    path('<int:pk>/', views.FamiliaDetailView.as_view(), name='detail'),
    path('nova/', views.FamiliaCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', views.FamiliaUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', views.FamiliaDeleteView.as_view(), name='delete'),
]

