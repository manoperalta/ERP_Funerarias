from django.urls import path
from . import views

app_name = 'pessoa_falecida'

urlpatterns = [
    path('', views.PessoaFalecidaListView.as_view(), name='list'),
    path('<int:pk>/', views.PessoaFalecidaDetailView.as_view(), name='detail'),
    path('nova/', views.PessoaFalecidaCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', views.PessoaFalecidaUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', views.PessoaFalecidaDeleteView.as_view(), name='delete'),
]

