from rest_framework import serializers


class CalculationRequestSerializer(serializers.Serializer):
    input_value = serializers.IntegerField()

class CalculationResponseSerializer(serializers.Serializer):
    output_value = serializers.IntegerField()