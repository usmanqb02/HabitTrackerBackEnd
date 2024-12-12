from django.urls import path, include
from rest_framework.routers import DefaultRouter
from habitTracker import views

router = DefaultRouter()
from habitTracker.views import HabitListCreate

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', views.LoginView.as_view(), name='login'),
    path('api/register/', views.RegisterView.as_view(), name='register'),
    path('api/habits/', HabitListCreate.as_view(), name='habit-list-create'),
    path('api/habits/<int:pk>/', views.HabitDetailUpdateDelete.as_view(), name='habit-detail-update-delete'),
    path('api/habits/<int:pk>/toggle/', views.HabitToggleCheck.as_view(), name='habit-toggle-check'),
]
