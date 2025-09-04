from django.urls import path
from . import views

app_name = 'financeiro'

urlpatterns = [
    path('', views.FinanceiroListView.as_view(), name='list'),
    path('<int:pk>/', views.FinanceiroDetailView.as_view(), name='detail'),
    path('novo/', views.FinanceiroCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', views.FinanceiroUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', views.FinanceiroDeleteView.as_view(), name='delete'),
    path('<int:pk>/marcar-pago/', views.marcar_como_pago, name='marcar_pago'),
    path('<int:pk>/nota-fiscal/', views.visualizar_nota_fiscal, name='nota_fiscal'),
]

