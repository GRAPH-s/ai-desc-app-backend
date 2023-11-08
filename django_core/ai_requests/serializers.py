from rest_framework import serializers
import ai_requests.models as models


class RequestHistorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image_thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = models.RequestHistory
        fields = "__all__"
