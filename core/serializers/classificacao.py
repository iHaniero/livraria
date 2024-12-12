from rest_framework.serializers import ModelSerializer

from core.models import Classificacao


class ClassificacaoSerializer(ModelSerializer):
    class Meta:
        model = Classificacao
        fields = "__all__"
