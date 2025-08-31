from django.urls import path
from . import views

app_name = 'configuracoes'

urlpatterns = [
    path('', views.configuracoes_view, name='detail'),
    path('editar/', views.ConfiguracaoFunerariaUpdateView.as_view(), name='update'),
    path('preview/', views.configuracoes_preview, name='preview'),
]

