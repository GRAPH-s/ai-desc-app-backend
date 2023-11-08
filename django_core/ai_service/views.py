import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from dotenv import load_dotenv
import os
from rest_framework import status

load_dotenv()
AI_SERVICE_URL = os.getenv("AI_SERVICE_URL")
HOST_URL = os.getenv("HOST_URL")


# Create your views here.
class AiServiceWithDescription(APIView):
    @staticmethod
    def send_request(data):
        try:
            endpoint = "without_input"
            if data.get("description"):
                endpoint = "with_input"
            url = f"{AI_SERVICE_URL}/api/{endpoint}"
            print(f"Sending request to {url}...", data)
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request to AI service failed: {str(e)}")

    def post(self, request, *args, **kwargs):
        try:
            image_url = request.data.get("image")
            user_description = request.data.get("user_description", "")

            if not image_url:
                return Response(
                    {"error": "Missing 'image' in the request data"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            data = {
                "image_url": HOST_URL + image_url,
                "accuracy_threshold": "0.7",
                "number_objects": 20,
                "description": user_description,
            }

            response = self.send_request(data=data)

            return Response(response.json(), status=response.status_code)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
