# users/views.py
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework import generics
from .models import Role, Project

# Import Serializers from the main serializers.py file
from .serializers import RoleSerializer, ProjectSerializer


# Home API View
@api_view(["GET"])
@permission_classes([AllowAny])

def home_view(request):
    return JsonResponse({"message": "Welcome to the TalentForge API!"})

# Role List and Create API View
class RoleListCreateView(generics.ListCreateAPIView):

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    # permission_classes = [IsAdminUser] # Only admin users can create/list roles

# Project List and Create API View
class ProjectListCreateView(generics.ListCreateAPIView):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # permission_classes = [IsAdminUser] # Only admin users can create/list projects

