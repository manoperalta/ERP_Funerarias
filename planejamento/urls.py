from django.urls import path
from . import views

app_name = 'planejamento'

urlpatterns = [
    path('', views.PlanejamentoListView.as_view(), name='list'),
    path('<int:pk>/', views.PlanejamentoDetailView.as_view(), name='detail'),
    path('novo/', views.PlanejamentoCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', views.PlanejamentoUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', views.PlanejamentoDeleteView.as_view(), name='delete'),
]

