from rest_framework import serializers, viewsets, status, response
from rest_framework.decorators import list_route, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

from visualiser import models, data


class ImageSerializer(serializers.ModelSerializer):
    labels = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()

    class Meta:
        model = models.Image
        fields = ('id', 'url', 'last_modified', 'labels', 'text')

    def get_labels(self, obj):
        labels = obj.get_labels()
        labels = [{'description': label.description, 'score': label.score,
                   'mid': label.mid, 'topicality': label.topicality} for
                  label in labels]
        return sorted(labels, key=lambda x: x.get('score', 0), reverse=True)

    def get_text(self, obj):
        texts = obj.get_text()
        texts = [ind_text for text in texts for ind_text in
                 text.text.split('\n') if ind_text]
        return texts


class ImageView(viewsets.ViewSet):

    def queryset(self):
        return models.Image.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ImageSerializer

    @list_route(methods=['post'])
    @parser_classes((FormParser, MultiPartParser,))
    def upload(self, request):
        upload = request.FILES.get('file')
        image_url = request.data.get('image_url')
        if upload:
            image_data = data.create_update_image(upload)
        elif image_url:
            image_data = data.create_update_image(image_url=image_url)
        else:
            image_data = []
        return response.Response(image_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        instance = models.Image.objects.get(pk=pk)
        serializer = ImageSerializer(instance)
        return response.Response(serializer.data)

    def list(self, request):
        queryset = models.Image.objects.order_by('-last_modified')
        serializer = ImageSerializer(queryset, many=True)
        return response.Response(serializer.data)
