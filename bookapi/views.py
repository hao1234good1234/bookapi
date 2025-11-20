from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView #导入APIView类视图

@api_view(['GET'])
def hello_api(request):
    return Response({"message": "hello, this is your first drf api"})

class HelloAPIView(APIView):
    def get(self, request):
        return Response({"message": "hello from class-based APIView"})