"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views
import os
from django.views.generic import RedirectView

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'teams', views.TeamViewSet, basename='team')
router.register(r'activities', views.ActivityViewSet, basename='activity')
router.register(r'leaderboard', views.LeaderboardViewSet, basename='leaderboard')
router.register(r'workouts', views.WorkoutViewSet, basename='workout')

def api_root_with_codespace(request):
    codespace_name = os.environ.get('CODESPACE_NAME', 'localhost')
    # Przekazujemy zmienną do oryginalnego api_root, jeśli obsługuje request
    response = views.api_root(request)
    # Dodajemy do odpowiedzi URL-e z dynamicznym hostem
    if codespace_name == 'localhost':
        base_url = f"http://localhost:8000/api/"
    else:
        base_url = f"https://{codespace_name}-8000.app.github.dev/api/"
    if hasattr(response, 'data'):
        # Przykład: dodajemy pole 'api_base_url' do odpowiedzi
        response.data['api_base_url'] = base_url
    return response

urlpatterns = [
    path('', RedirectView.as_view(url='/api/', permanent=False)),
    path('api/', api_root_with_codespace, name='api-root'),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
