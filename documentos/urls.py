from django.urls import path
from . import views

app_name = 'documentos'

urlpatterns = [
    path("post_lembranca/<int:pk>/", views.post_lembranca_view, name="post_lembranca"),
]


