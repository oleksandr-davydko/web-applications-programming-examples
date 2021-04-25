from rest_framework import serializers
from introapp.models import ContactModel


class ContactSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(required=False)
	class Meta:
		model = ContactModel
		fields = '__all__'

