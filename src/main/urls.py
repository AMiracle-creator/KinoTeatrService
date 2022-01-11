from django.urls import path, include
from rest_framework import routers

from .views import TaskViewSet, TaskResultViewSet, MainApiView, FileView, \
    ExtraDataViewSet

router = routers.DefaultRouter()
router.register(r'task', TaskViewSet)
router.register(r'result', TaskResultViewSet)
router.register(r'extra', ExtraDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('health/', MainApiView.as_view()),
    path('file/<int:id>/', FileView.as_view()),
    path('auth/', include('rest_framework.urls'))
]