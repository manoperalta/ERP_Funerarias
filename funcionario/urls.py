from django.urls import path
from . import views

app_name = 'funcionario'

urlpatterns = [
    path('', views.FuncionarioListView.as_view(), name='list'),
    path('<int:pk>/', views.FuncionarioDetailView.as_view(), name='detail'),
    path('novo/', views.FuncionarioCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', views.FuncionarioUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', views.FuncionarioDeleteView.as_view(), name='delete'),
]

