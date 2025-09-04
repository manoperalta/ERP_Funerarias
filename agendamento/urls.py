from django.urls import path
from . import views

app_name = 'agendamento'

urlpatterns = [
    path('', views.AgendamentoListView.as_view(), name='list'),
    path('<int:pk>/', views.AgendamentoDetailView.as_view(), name='detail'),
    path('novo/', views.AgendamentoCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', views.AgendamentoUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', views.AgendamentoDeleteView.as_view(), name='delete'),
    path("public/<int:pk>/", views.AgendamentoPublicDetailView.as_view(), name="public_detail"),
]


