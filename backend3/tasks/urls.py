from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

router = DefaultRouter() # ask here what its working
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)) #which url it is representing
]
