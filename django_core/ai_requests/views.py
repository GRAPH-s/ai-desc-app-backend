from rest_framework import generics, status
import ai_requests.models as models
import ai_requests.serializers as serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
AI_SERVICE_URL = os.getenv("AI_SERVICE_URL")


class RequestHistoryAPIList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = models.RequestHistory
    serializer_class = serializers.RequestHistorySerializer

    @staticmethod
    def get_ai_service_response(data):
        try:
            endpoint = "without_input"
            if data.get("description"):
                endpoint = "with_input"
            url = f"{AI_SERVICE_URL}/api/{endpoint}"
            print(f"Sending request to {url}...", data)
            response = requests.post(url, json=data)
            response.raise_for_status()
            response_data = response.json()

            if response_data.get("description") is None:
                raise Exception(f"Request to AI service failed: {str(response_data)}")

            return response_data
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request to AI service failed: {str(e)}")

    def create(self, request, *args, **kwargs):
        try:
            image = request.data.get("image")
            user_description = request.data.get("user_description", "")
            user = request.user

            if not image:
                return Response(
                    {"error": "Missing 'image' in the request data"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            rh_object = models.RequestHistory.objects.create(
                image=image, user=user, user_description=user_description
            )

            serialized_rh_object = (
                serializers.RequestHistorySerializer(rh_object)
            ).data

            data = {
                "image_url": serialized_rh_object.get("image"),
                "accuracy_threshold": "0.7",
                "number_objects": 20,
                "description": serialized_rh_object.get("user_description"),
            }

            response = self.get_ai_service_response(data=data)

            rh_object.ai_description = response.get("description")
            rh_object.save()

            return Response(
                serializers.RequestHistorySerializer(rh_object).data,
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_queryset(self):
        return models.RequestHistory.objects.all().filter(user=self.request.user)
