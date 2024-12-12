from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Habit
from .serializers import RegisterSerializer, LoginSerializer, HabitSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class HabitViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class HabitListCreate(APIView):
    def get(self, request):
        habits = Habit.objects.filter(user=request.user)[:5] 
        serializer = HabitSerializer(habits, many=True)
        return Response(serializer.data)

    def post(self, request):
        print("user: ", request.user.__dict__)
        serializer = HabitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HabitDetailUpdateDelete(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Habit.objects.get(pk=pk, user=user)
        except Habit.DoesNotExist:
            return None

    def get(self, request, pk):
        habit = self.get_object(pk, request.user)
        if habit:
            serializer = HabitSerializer(habit)
            return Response(serializer.data)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        habit = self.get_object(pk, request.user)
        if habit:
            serializer = HabitSerializer(habit, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        habit = self.get_object(pk, request.user)
        if habit:
            habit.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

class HabitToggleCheck(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        habit = Habit.objects.get(pk=pk, user=request.user)
        if habit:
            current_time = timezone.now()
            if habit.last_checked and (current_time - habit.last_checked).total_seconds() < 86400:
                return Response({"detail": "Already checked within the last 24 hours."}, status=status.HTTP_400_BAD_REQUEST)

            habit.checked = not habit.checked
            habit.last_checked = current_time
            habit.streak = habit.streak + 1 if habit.checked else habit.streak
            habit.save()

            serializer = HabitSerializer(habit)
            return Response(serializer.data)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({"user": user.username, "token": token.key}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']

            if User.objects.filter(username=username).exists():
                return Response({"message": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(username=username, password=password, email=email)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"user": user.username, "token": token.key}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
