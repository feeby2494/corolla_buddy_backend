from django.urls import path, include

from repair_service import views

urlpatterns = [
    path('repairs/', views.repair.as_view()),
]