from django.urls import include, path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('posts', PostViewsets, basename='posts')


urlpatterns =[
    # path('', include(router.urls)),
    path('posts/', PostListCreatedView.as_view()),
    path('posts/<slug:pk>/', PostRetriveView.as_view()),
    path('categories/', CategoryListCreateView.as_view()),
    path('tags/', TagListCreateView.as_view()),
    path('posts/', PostViewsets.as_view({'get': 'list'})),
    # path('posts/<slug:pk>/',PostViewsets.as_view({'get': 'retrieve', 'put': 'update', 'pach': 'partial_update', 'delete': 'desrtoy'})),

]