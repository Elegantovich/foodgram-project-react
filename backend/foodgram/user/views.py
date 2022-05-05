from api.permissions import AdminUserOrReadOnly
from api.serializers import (PasswordSerializer, ShowFollowsSerializer,
                             TokenSerializer, UserRetrieveSerializer,
                             UserRoleSerializer, UserSerializer)
from recipe.models import Follow, User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    queryset = User.objects.all()
    lookup_field = 'pk'

    def get_permissions(self):
        if self.action not in ['create', 'list', 'retrieve']:
            permission_classes = [AdminUserOrReadOnly]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

         
    @permission_classes([AllowAny])
    def list(self, request):
        queryset = User.objects.all()
        user = request.user
        if str(user) == 'AnonymousUser':
            serializer = UserRetrieveSerializer(queryset, many=True)
            return Response(serializer.data)
        serializer = UserRetrieveSerializer(queryset, many=True)
        for acc in serializer.data:
            author = get_object_or_404(queryset, pk=acc['id'])
            if user.id == author.id:
                is_subscribed = False
            elif Follow.objects.filter(user=user, author=author).exists():
                is_subscribed = True
            acc['is_subscribed'] = is_subscribed
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        is_subscribed = False
        user = request.user
        queryset = User.objects.all()
        author = get_object_or_404(queryset, pk=pk)
        if str(user) == 'AnonymousUser':
            serializer = UserRetrieveSerializer(author)
            return Response(serializer.data)
        serializer = UserRetrieveSerializer(author)
        if Follow.objects.filter(user=user, author=author).exists():
            is_subscribed = True
        serializar_dict = serializer.data
        serializar_dict['is_subscribed'] = is_subscribed
        return Response(serializar_dict)

    @action(detail=True, methods=('post',),
            permission_classes=(IsAuthenticated, AdminUserOrReadOnly))
    def set_password(self, request, pk=None):
        old_password = request.data['current_password']
        new_password = request.data['new_password']
        user = self.get_object()
        if user.password != old_password:
            return Response(
                {"message": "Password not correct!"},
                status=status.HTTP_400_BAD_REQUEST
                )
        data = {'id': user.id, 'password': user.password}
        serializer = PasswordSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user.password = new_password
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=('get',), url_path='me',
            permission_classes=(IsAuthenticated,),
            serializer_class=UserRoleSerializer)
    def get_patch_me_url(self, request):
        if request.method != 'GET':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer = self.get_serializer(request.user)
        serializar_dict = serializer.data
        serializar_dict['is_subscribed'] = False
        return Response(serializar_dict)


def get_tokens_for_user(user):
    "Создание токена."
    access = AccessToken.for_user(user)
    return {'access': str(access)}


class RecieveToken(APIView):

    @permission_classes(AdminUserOrReadOnly)
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        serializer = TokenSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        user = get_object_or_404(User, email=email, password=password)
        response = {'auth_token': get_tokens_for_user(user)}
        return Response(response, status=status.HTTP_200_OK)


class FollowViewSet(APIView):

    @permission_classes(AdminUserOrReadOnly)
    def get(self, request):
        user = User.objects.filter(following__user=request.user)

        serializer = ShowFollowsSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @permission_classes(AdminUserOrReadOnly)
    def post(self, request, user_id):
        is_subscribed = False
        user = request.user
        author = get_object_or_404(User, id=user_id)
        print(user.id, author.id)
        if user.id == author.id:
            return Response(
                {'response': 'You not can subscribe to yourself!'},
                status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(user=user, author=author).exists():
            return Response(
                {'response': 'Follow also exist!'},
                status=status.HTTP_400_BAD_REQUEST)
        Follow.objects.create(user=user, author=author)
        serializer = ShowFollowsSerializer(author)
        if Follow.objects.filter(user=user, author=author).exists():
            is_subscribed = True
        serializar_dict = serializer.data
        serializar_dict['is_subscribed'] = is_subscribed
        print(serializar_dict)
        return Response(serializar_dict, status=status.HTTP_201_CREATED)

    @permission_classes(AdminUserOrReadOnly)
    def delete(self, request, user_id):
        user = request.user
        author = get_object_or_404(User, id=user_id)
        follow = get_object_or_404(Follow, user=user, author=author)
        follow.delete()
        return Response({'response': 'Removed!'},
                        status=status.HTTP_204_NO_CONTENT)
