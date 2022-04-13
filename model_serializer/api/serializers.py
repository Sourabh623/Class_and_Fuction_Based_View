from rest_framework import serializers
from .models import Student

#validator validation
def start_with_s(value) :
    if value[0].lower() != "s":
        raise serializers.ValidationError("name start with only S")
        
# create serializer class for read model
class StudentSerializer(serializers.ModelSerializer):
    #validator level validation
    name = serializers.CharField(max_length=100, validators=[start_with_s])
    
    #field level validation
    def validate_roll(self, value):
        if value >= 200:
            raise serializers.ValidationError("Seat Full")
        return value
    
    #meta about model
    class Meta:
        model = Student
        fields = ("id","name", "roll", "city")


