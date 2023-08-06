from rest_framework import generics, mixins, permissions, viewsets
from rest_framework.response import Response

from huscy.attributes import models, serializer, services
from huscy.subjects.models import Subject


class AttributeSchemaView(generics.ListCreateAPIView):
    permission_classes = (permissions.DjangoModelPermissions, )
    queryset = models.AttributeSchema.objects.all()
    serializer_class = serializer.AttributeSchemaSerializer

    def list(self, request):
        attribute_schema = services.get_attribute_schema()
        serializer = self.get_serializer(attribute_schema)
        return Response(serializer.data)


class AttributeSetViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Subject.objects.all()
    serializer_class = serializer.AttributeSetSerializer

    def get_object(self):
        subject = super().get_object()
        return services.get_or_create_attribute_set(subject)
