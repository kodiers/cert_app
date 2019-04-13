from rest_framework.response import Response
from rest_framework import status


class CreateMixin:
    def create(self, request, *args, **kwargs):
        context = {'request': request}
        serializer = self.serializer_class(data=request.data, context=context, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)