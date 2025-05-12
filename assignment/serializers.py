from rest_framework import serializers

class EventSerializer(serializers.Serializer):
    type = serializers.CharField()
    created_time = serializers.DateTimeField()
    unit = serializers.IntegerField()

class StudentDataSerializer(serializers.Serializer):
    namespace = serializers.CharField()
    student_id = serializers.CharField()
    events = EventSerializer(many=True)
