
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Post
from . import serializers


class PageSizeAndNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 1000


@swagger_auto_schema(method='post', request_body=serializers.RegisterSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = serializers.RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user, token = serializer.save()

    data = {"user": user, "access_token": token.key}
    return Response(serializers.UserTokenSerializer(data).data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='post', request_body=serializers.LoginSerializer)
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    wrong_credentials = {"detail": "Wrong credentials."}
    serializer = serializers.LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    if data.get('email'):
        user = authenticate(request, email=data['email'], password=data['password'])
    elif data.get('phone_number'):
        user = authenticate(request, phone_number=data['phone_number'], password=data['password'])
    else:
        return Response({'detail': 'Please provide email or phone number.'}, status=status.HTTP_401_UNAUTHORIZED)

    if not user:
        return Response(wrong_credentials, status=status.HTTP_401_UNAUTHORIZED)

    token, created = Token.objects.get_or_create(user=user)

    data = {"user": user, "access_token": token.key}

    return Response(serializers.UserTokenSerializer(data).data, status=status.HTTP_200_OK)


class PostListView(ListCreateAPIView):
    """
       get:
       Return a list of post objects

       post:
       creates a new post object
   """

    permission_classes = [AllowAny]
    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        return Post.objects.all()


class PostDetailView(RetrieveUpdateDestroyAPIView):
    """
    get:
    Return the details of a single post

    put:
    Updates a given post, non-partial update

    patch:
    Updates a given post, partial update



    delete:
    Deletes a single post
    """

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        return Post.objects.all()

    def get_object(self):
        id_ = self.kwargs.get('id')
        post = Post.objects.get(id=id_)
        return post


@api_view()
@permission_classes([IsAuthenticated])
def unlike_post(request, post_id):

    post = Post.objects.get(id=post_id)
    # if post.owner == request.user:
    #     return Response({'detail': 'You are not allowed to like  your own post'}, status=status.HTTP_400_BAD_REQUEST)

    post.likes.remove(request.user)
    post.refresh_from_db()
    return Response(serializers.PostSerializer(post).data, status=status.HTTP_200_OK)


@api_view()
@permission_classes([IsAuthenticated])
def like_post(request, post_id):

    post = Post.objects.get(id=post_id)
    if post.owner == request.user:
        return Response({'detail': 'You are not allowed to like your own post'}, status=status.HTTP_400_BAD_REQUEST)

    post.likes.add(request.user)
    post.refresh_from_db()
    return Response(serializers.PostSerializer(post).data, status=status.HTTP_200_OK)
