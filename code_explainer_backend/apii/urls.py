from django.urls import path
from .views import analyze_code

urlpatterns = [
    path('analyze-code/', analyze_code),
]
