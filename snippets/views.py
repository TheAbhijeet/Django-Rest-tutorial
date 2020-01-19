from django.contrib.auth.models import User  # new
# from rest_framework import generics

from .models import Snippet
from .serializers import SnippetSerializer, UserSerializer  # new
from rest_framework import generics, permissions, renderers  # new
from .permissions import IsOwnerOrReadOnly
# from rest_framework.decorators import api_view  # new
# from rest_framework.response import Response  # new
# from rest_framework.reverse import reverse  # new


# @api_view(['GET'])  # new
# def api_root(request, format=None):
#     return Response({
#         'users': reverse('user-list', request=request, format=format),
#         'snippets': reverse('snippet-list', request=request, format=format)
#     })


# class SnippetHighlight(generics.GenericAPIView):  # new
#     queryset = Snippet.objects.all()
#     renderer_classes = (renderers.StaticHTMLRenderer,)

#     def get(self, request, *args, **kwargs):
#         snippet = self.get_object()
#         return Response(snippet.highlighted)


# class SnippetList(generics.ListCreateAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

#     def perform_create(self, serializer):  # new
#         serializer.save(owner=self.request.user)


# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = (
#         permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


# class UserList(generics.ListAPIView):  # new
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserDetail(generics.RetrieveAPIView):  # new
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
