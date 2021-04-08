from json import loads

from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from introapp.models import CalculateResponse, CalculateRequest
from introapp.serializers import CalculationResponseSerializer, CalculationRequestSerializer
from introapp.utils import Calculator


"""
Клас, що описує точку доступа до API застосунку. Має наслідуватись від
APIView.
"""
class ExampleView(APIView):

    def post(self, request: HttpRequest):
        """
        Описує обробник POST запитів для даної точки доступу. Аналогічно можна визначити
        обробники і для інших HTTP методів.
        """
        # Десеріалізувати тіло запиту із JSON строки у словник. Зауважте, тут ми вже маємо
        # доступ до усього тіла запиту, тобто Django гарантує, що усе тіло буде повінстю зчитане
        # незалежно від розміру.
        parsed_request = loads(request.body)
        # Створити клас-серіалізатор, що провалідує правильність заповнення полів об'єкту
        request_data_serializer = CalculationRequestSerializer(data=parsed_request)
        if not request_data_serializer.is_valid():
            # Якщо валідацію не пройдено - сповістити клієнта про неправильний формат запиту
            return Response(status=400)
        # Створити об'єкт, що описує дані запиту, із провалідованих даних
        request_data = CalculateRequest(**request_data_serializer.validated_data)
        # Використання даних запиту у бізнес-логіці
        calculation_result = Calculator.calculate(request_data.input_value)
        # Створити об'єкт, що описує дані відповіді на запит
        response_data = CalculateResponse(calculation_result)
        # Створити клас-серіалізатор, що підготує об'єкт з даними для відповіді до серіалізації
        response_data_serializer = CalculationResponseSerializer(response_data)
        # Створити об'єкт відповіді із даними
        response = Response(response_data_serializer.data, content_type='application/json')
        # Повернути відповідь. Коректна доставка гарантована фреймворком.
        return response

@api_view(['GET', 'POST'])
def another_example(request: HttpRequest):
    """
    Приклад створення точки доступу на основі python-функції із застосуванням декоратору api_view
    """
    if request.method == 'POST':
        return Response({'message': f'[POST] Another example also works!: {request.body}]'})
    return Response({'message': f'[GET] Another example also works!: no body'})





