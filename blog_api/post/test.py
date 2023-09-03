from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from .models import Category, Post
from django.contrib.auth import get_user_model
from .views import PostViewsets
from collections import OrderedDict

User = get_user_model()


class PostTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.category = Category.objects.create(title='cat1')
        user = User.objects.create_user(email='qwerty@qwerty.qwerty', password='qwerty', name='qwerty', is_active=True)
        self.token = '12345'

        posts = [
            Post(author=user, body='test posts', title='first_post', category=self.category, slug='1'),
            Post(author=user, body='test posts', title='second_post', category=self.category, slug='2'),
            Post(author=user, body='test posts', title='third_post', category=self.category, slug='3'),
                ]
        Post.objects.bulk_create(posts)

    def test_post_list(self):
        request = self.factory.get('api/v1/posts/')
        view = PostViewsets.as_view({'get': 'list'})
        response = view(request)
        # print(response.data)
        assert response.status_code == 201
        assert type(response.data) == OrderedDict

    def test_post_retrieve(self):
        slug =Post.objects.all()[0].slug
        request = self.factory.get(f'/posts/{slug}/')
        view = PostViewsets.as_view({'get': 'retrieve'})
        response = view(request, pk=slug)
        # print(response.data)

        assert response.status_code == 200

    def test_post_create(self):
        user = User.objects.all()[0]
        data = {'body': 'new post',
                'title': 'post4',
                'category': 'cat1',
                'slug': 4 }
        request = self.factory.post('/posts/', data, format='json')
        force_authenticate(request, user)
        view = PostViewsets.as_view({'post': 'create'})
        response = view(request)
        print(response.status_code)

        # assert response.data['body'] == data['body']
        # assert response.data['author'] == user.name
        assert Post.objects.filter(author=user, body=data['body']).exists()

    def test_post_update(self):
        user = User.objects.all()[0]
        data = {'body': 'updated body'}
        post = Post.objects.all()[2]
        request = self.factory.patch(f'/posts/{post.slug}', data, format='json')
        force_authenticate(request, user)
        view = PostViewsets.as_view({'path': 'partial_update'})
        response = view(request, pk=post.slug)

        assert Post.objects.filter(slug=post.slug).body == data['body']

    def test_post_delete(self):
        user = User.objects.all()[0]
        post = Post.objects.all()[2]
        request = self.factory.delete(f'/posts/{post.slug}/')
        force_authenticate(request, user)
        view = PostViewsets.as_view({'delete': 'destroy'})
        response = view(request, pk=post.slug)

        assert not Post.objects.filter(slug=post.slug).exists()



            