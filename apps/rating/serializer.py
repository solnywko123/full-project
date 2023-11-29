from rest_framework import serializers

from apps.rating.models import Rating


class RatingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    product = serializers.ReadOnlyField(source='product.title')

    class Meta:
        model = Rating
        fields = '__all__'

