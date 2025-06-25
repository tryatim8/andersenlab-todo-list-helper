from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request


@api_view(['GET'])
def hello_apiview(request: Request) -> Response:
    """Функция приветствия с описанием приложения."""

    return Response({'message': 'Hello ToDo API users app customer!'})
