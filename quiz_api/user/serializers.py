from rest_framework import serializers
from user.models import User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["UID", "name", "email", "grade", "thumbnail", "country"]
        # read_only_field = []