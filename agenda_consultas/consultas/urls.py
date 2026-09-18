from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("disponibilidades/nova/", views.disponibilidade_create, name="disponibilidade_create"),
    path("disponibilidades/<int:pk>/excluir/", views.disponibilidade_delete, name="disponibilidade_delete"),
    path("profissionais/", views.profissional_list, name="profissional_list"),
    path("profissionais/<int:profissional_pk>/agendar/", views.consulta_create, name="consulta_create"),
    path("consultas/<int:pk>/cancelar/", views.consulta_cancelar, name="consulta_cancelar"),
    path("consultas/<int:pk>/realizar/", views.consulta_realizar, name="consulta_realizar"),
]
