from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from recipe.models import User
from ..api.permissions import (AdminOrReadonly, AuthorOrModeratorOrAdminOrReadonly,
                          SelfOrAdmin)
from ..api.serializers import (AuthSerializer, UserSerializer,
                               UserRoleSerializer)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (SelfOrAdmin,)
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    queryset = User.objects.all()
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'], url_path='me',
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
        return Response(serializer.data)