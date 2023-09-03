# from django.shortcuts import render
from rest_framework import generics, viewsets, filters
from .models import Post, Category, Tag
from .serializers import PostDetailSerializer, PostListSerializer, CategorySerializer, TagSerializer
import django_filters
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework.permissions import AllowAny
from .permission import IsAuthorPermission,  IsAdminOrIsAuthenticatedPermission
from rest_framework.decorators import action
from review.serializers import RatingSerializer
from review.models import Like, Rating
from rest_framework.response import Response


class PostListCreatedView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    
    def get_serializer_class(self):
       if self.request.method == 'GET':
           return PostListSerializer
       return PostDetailSerializer
    
class PostRetriveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
        

class PostViewsets(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['tags_slug', 'category', 'author']
    search_fields = ['title', 'body']
    ordering_fields =['created_at', 'title']

    @action(methods=['POST', 'PATCH'], detail=True)
    def set_rating(self, request, pk=None):
        # data = request.data
        data = request.data.copy()
        data['post'] = pk
        serializer = RatingSerializer(data=data, context = {'request': request})
        rating = Rating.objects.filter(author=request.user, post=pk).first()
        if serializer.is_valid(raise_exception=True):
            if rating and request.method == 'POST':
                return Response('Rating object exixsts', status=200)
            elif rating and request.method == 'PATCH':
                serializer.update(rating, serializer.validated_data)
                return Response(serializer.data, status=200)
            elif request.method == 'POST':
                serializer.create(serializer.validated_data)
                return Response(serializer.data, status=200)
            
    @action(['Post'], detail=True)
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(post=post, author=user)
            print('===========')
            print(like)
            print('===========')
            like.delete()
            message = 'Disliked'
            status = 204
        except Like.DoesNotExist:
            Like.objects.create(post=post, author=user)
            message = 'liked'
            status = 201
        return Response(message, ststus=201)



    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostListSerializer

    def get_permission(self):
        if self.action == 'create':
            self.permission_classes = [IsAdminOrIsAuthenticatedPermission]

        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission]

        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()
    