"""pumps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from main import views, restviews
from rest_framework.routers import DefaultRouter

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'manufacturer', restviews.ManufacturerViewSet)
router.register(r'type', restviews.TypeViewSet)
router.register(r'model', restviews.ModelViewSet)
router.register(r'mark', restviews.MarkViewSet)

urlpatterns = [

    path('', include(router.urls)),
    path('init/select', restviews.init_select),

    path('admin/', admin.site.urls),
    path('main/', views.pumps),
    path('choice/', views.choice),
    path('select/', views.select),
]
