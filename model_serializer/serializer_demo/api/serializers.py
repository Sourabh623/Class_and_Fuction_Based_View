from rest_framework import serializers
from api.models import Student

# create serializer class for read model
class StudentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    roll_no = serializers.IntegerField()
    city = serializers.CharField(max_length=100)

#validator validation
def start_with_s(value) :
    if value[0].lower() != "s":
        raise serializers.ValidationError("name start with only S")

# create serializer class for create model
class StudentSerializerCreate(serializers.Serializer):
    name = serializers.CharField(max_length=100, validators=[start_with_s])
    roll_no = serializers.IntegerField()
    city = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Student.objects.create(**validated_data)
    
    #field level validation
    def validate_roll_no(self, value):
        if value >= 200:
            raise serializers.ValidationError("Seat Full")
        return value
    
    #object level validation
    def validate(self, data):
        print(type(data))
        name = data.get("name")
        city = data.get("city")
        if name.lower() == "sourabh" and city.lower() == "khandwa":
            raise serializers.ValidationError("city must be unique")
        return data

# create serializer class for update model
class StudentSerializerUpdate(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    roll_no = serializers.IntegerField()
    city = serializers.CharField(max_length=100)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.roll_no = validated_data.get('roll_no',instance.roll_no)
        instance.city = validated_data.get('city',instance.city)
        instance.save()
        return instance
