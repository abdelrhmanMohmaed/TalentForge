# users/serializers.py
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer, UserSerializer as DjoserUserSerializer
from .models import User, Role, Project, UserRoleProject


# Custom User Creation Serializer (for Djoser registration)
class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'EED', 'password', 'name', 'department', 'job_title', 'location')
        # EED and email are required by our model, password by djoser.
        # name, department, job_title, location are optional
        read_only_fields = ('id',) # ID is generated automatically

# Custom User Serializer (for retrieving user details)
class UserSerializer(DjoserUserSerializer):
    class Meta(DjoserUserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'EED', 'name', 'department', 'job_title', 'location', 'is_active', 'is_staff', 'is_superuser', 'created_at', 'updated_at')
        read_only_fields = ('id', 'email', 'EED', 'is_active', 'is_staff', 'is_superuser', 'created_at', 'updated_at') # These fields are not editable via this serializer

# Serializer for Role
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

# Serializer for Project (simple placeholder)
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

# Serializer for UserRoleProject (pivot table)
class UserRoleProjectSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')
    role_name = serializers.ReadOnlyField(source='role.name')
    project_name = serializers.ReadOnlyField(source='project.name', allow_null=True) # Allow null if project is null

    class Meta:
        model = UserRoleProject
        fields = ('id', 'user', 'user_email', 'role', 'role_name', 'project', 'project_name', 'created_at')
        read_only_fields = ('created_at',)
        
# Custom Token Serializer to include user data
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['EED'] = user.EED
        token['name'] = user.name
        token['department'] = user.department

        # Get user roles
        # This requires a query to UserRoleProject table.
        # For simplicity, let's just get the names of roles directly from UserRoleProject
        # Note: This is an example, you might want to optimize this query
        user_roles_queryset = user.userroleproject_set.select_related('role').all()
        roles_list = [ur.role.name for ur in user_roles_queryset]
        token['roles'] = roles_list

        return token

    def validate(self, attrs):
        # The default validate method handles authentication (email + password)
        data = super().validate(attrs)

        # Add user data to the response
        user_serializer = UserSerializer(self.user)
        data['user'] = user_serializer.data

        # Remove default access/refresh keys if only 'token' is desired,
        # or keep them if you want both token and user object.
        # Assuming you want the user object as part of the token response,
        # but the actual JWT token is still 'access' token.
        # Let's adjust the response structure to match your requested format:
        # { "token": "jwt_token", "user": { ... } }

        # We'll return 'access' token as 'token' and add user details.
        # You might need to adjust the front-end to pick 'access' or 'token'
        # depending on which key you prefer.
        data['token'] = data.pop('access') # Rename 'access' to 'token'
        data.pop('refresh', None) # Remove 'refresh' if not needed in login response

        return data