from rest_framework import serializers
from .models import Quizes


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quizes
        exclude = ['questions']
        