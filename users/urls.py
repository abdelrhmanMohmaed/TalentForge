from django.urls import path
from .views import RoleListCreateView, ProjectListCreateView

urlpatterns = [
    path('roles/', RoleListCreateView.as_view(), name='role-list-create'),
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
]