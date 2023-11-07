from rest_framework.views import APIView
from rest_framework.response import Response
from dotenv import load_dotenv
import os

load_dotenv()
AI_SERVICE_URL = os.getenv("AI_SERVICE_URL")

# Create your views here.
class AiServiceWithDescription(APIView):
    def get(self, request, *args, **kwargs):
        return Response(f"Привет, {AI_SERVICE_URL}")
