from django.urls import path
from . import views

app_name = 'item_servico'

urlpatterns = [
    path('', views.ItemServicoListView.as_view(), name='list'),
    path('<int:pk>/', views.ItemServicoDetailView.as_view(), name='detail'),
    path('novo/', views.ItemServicoCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', views.ItemServicoUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', views.ItemServicoDeleteView.as_view(), name='delete'),
]

