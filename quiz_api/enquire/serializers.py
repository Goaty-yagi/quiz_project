from rest_framework import serializers
from .models import Enquire


class EnquireSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Enquire
		fields = "__all__"