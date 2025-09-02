from django.urls import path
from . import views

app_name = 'funcionario'

urlpatterns = [
    path('', views.FuncionarioListView.as_view(), name='list'),
    path('<int:pk>/', views.FuncionarioDetailView.as_view(), name='detail'),
    path('novo/', views.FuncionarioCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', views.FuncionarioUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', views.FuncionarioDeleteView.as_view(), name='delete'),
    
    # URLs para gerenciamento de contas
    path('<int:pk>/criar-conta/', views.criar_conta_view, name='criar_conta'),
    path('<int:pk>/resetar-senha/', views.resetar_senha_view, name='resetar_senha'),
    path('<int:pk>/toggle-ativo/', views.toggle_ativo_view, name='toggle_ativo'),
]

