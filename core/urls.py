from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views as auth_views

from anemometers import views

router = routers.DefaultRouter()
router.register('anemometers', views.AnemometerViewSet)
router.register('tags', views.TagViewSet)
router.register('wind-reading', views.WindReadingCreateListRetrieveView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/anemometer/<int:pk>/wind-reading',
         views.WindReadingForAAnemometerListView.as_view()),
    path('api/wind-statistics/', views.WindStatisticView.as_view()),
    path('api/', include(router.urls)),
    path('auth-token/', auth_views.obtain_auth_token)
]
