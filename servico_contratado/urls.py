from django.urls import path
from . import views

app_name = 'servico_contratado'

urlpatterns = [
    path('', views.ServicoContratadoListView.as_view(), name='list'),
    path('<int:pk>/', views.ServicoContratadoDetailView.as_view(), name='detail'),
    path('novo/', views.ServicoContratadoCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', views.ServicoContratadoUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', views.ServicoContratadoDeleteView.as_view(), name='delete'),
]

