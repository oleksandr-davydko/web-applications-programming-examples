"""
Класи, що описують схеми для запиту і відповіді
"""
class CalculateRequest:
    def __init__(self, input_value: int):
        self.input_value = input_value

class CalculateResponse:
    def __init__(self, result: int):
        self.output_value = result