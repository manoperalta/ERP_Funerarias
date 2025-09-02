"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from accounts import views as accounts_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", accounts_views.home_redirect, name="home"),
    path("accounts/", include("accounts.urls")),
    
    # URLs dos dashboards (sem namespace para facilitar redirecionamento)
    path('dashboard/admin/', accounts_views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/vendedor/', accounts_views.dashboard_vendedor, name='dashboard_vendedor'),
    path('dashboard/funcionario/', accounts_views.dashboard_funcionario, name='dashboard_funcionario'),
    
    path('funcionarios/', include('funcionario.urls')),
    path('familias/', include('familia.urls')),
    path('pessoas-falecidas/', include('pessoa_falecida.urls')),
    path('itens-servico/', include('item_servico.urls')),
    path('servicos-contratados/', include('servico_contratado.urls')),
    path('agendamentos/', include('agendamento.urls')),
    path('planejamentos/', include('planejamento.urls')),
    path('financeiro/', include('financeiro.urls')),
    path("configuracoes/", include("configuracoes.urls")),
    path("documentos/", include("documentos.urls")),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
