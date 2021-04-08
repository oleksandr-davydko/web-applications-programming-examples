from django.db import models

"""
Опис моделі контакту. Автоматично буде створено у БД після міграції.
"""
class ContactModel(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=30)
	surname = models.CharField(max_length=30)
	patronymic = models.CharField(max_length=30)
	email = models.CharField(max_length=30)
	telephone = models.CharField(max_length=30)
