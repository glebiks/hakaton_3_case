from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated



class GetTokenNewRoleView(APIView):
    def post(self, request):
        role_data = request.data.get("role")
        if role_data in (1, 2):
            user = User.objects.create()
            custom_user = CustomUser.objects.create(user=user, role=role_data)
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            data = {
                'token': token
            }
            return Response({"success": True, "data": data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": False, "message": "Wrong role"}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class EnterMyDataView(APIView):
    def post(self, request):
        # Извлеките пользователя на основе токена
        user = request.user
        name = request.data.get("name")
        
        # Верните айди пользователя в ответе
        data = {
            'user_id': CustomUser.objects.get(user=user).user,
            'custom_user_if': CustomUser.objects.get(user=user).id


        }
        
        return Response(data, status=status.HTTP_200_OK)
