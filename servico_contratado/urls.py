from django.urls import path
from . import views

app_name = 'servico_contratado'

urlpatterns = [
    path('', views.ServicoContratadoListView.as_view(), name='list'),
    path('<int:pk>/', views.ServicoContratadoDetailView.as_view(), name='detail'),
    path('novo/', views.servico_contratado_create, name='create'),
    path('<int:pk>/editar/', views.servico_contratado_update, name='update'),
    path('<int:pk>/excluir/', views.ServicoContratadoDeleteView.as_view(), name='delete'),
    path('<int:pk>/nota-fiscal/', views.gerar_nota_fiscal_pdf, name='nota_fiscal'),
    path('<int:pk>/visualizar-pdf/', views.visualizar_nota_fiscal_pdf, name='visualizar_pdf'),
    path('api/item-preco/<int:item_id>/', views.get_item_preco, name='item_preco'),
]

