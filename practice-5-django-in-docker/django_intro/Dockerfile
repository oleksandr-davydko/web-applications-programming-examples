# Вибрати базовий образ
FROM python:3.8
EXPOSE 80
# встановити робочу директорію, щоб не працювати у корені ОС
WORKDIR /app
# спочатку встановлюємо залежності, адже вони будуть мінятися досить рідко
COPY requirements.txt requirements.txt
RUN ["pip", "install", "-r", "requirements.txt"]
# тепер копіюємо у контейнер усі файли
COPY . .
# старт django
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
