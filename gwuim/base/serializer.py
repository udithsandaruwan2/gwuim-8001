from rest_framework import serializers
from django.contrib.auth.models import User
from vacations.models import Vacation

class VacationSerializer(serializers.ModelSerializer):
    """Serializer for Vacation model."""
    class Meta:
        model = Vacation
        fields = '__all__'

class LeaveCountSerializer(serializers.Serializer):
    attendance_count = serializers.IntegerField()
    leave_count = serializers.IntegerField()