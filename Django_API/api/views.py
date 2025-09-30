from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

@api_view(['GET'])
def hello_world(request):
    """
    Simple Hello World API endpoint
    """
    data = {
        'message': 'Hello World from Django API! 🚀',
        'timestamp': datetime.now().isoformat(),
        'method': request.method,
        'endpoint': '/api/test/',
        'status': 'success'
    }
    
    return Response(data, status=status.HTTP_200_OK)