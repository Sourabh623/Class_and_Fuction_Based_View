import io
import json

from django.http import HttpResponse, JsonResponse
from .serializers import StudentSerializer, StudentSerializerCreate, StudentSerializerUpdate
from .models import Student
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view


#Instantiate the form
#Instantiate the form, check whether request is post or not. It validate the data by using is_valid() method.

@api_view(["GET"]) 
def single_student_view(request,pk):
    try:
        
        if pk is not None:
            #create instance of the student model class
            single_student = Student.objects.get(id=pk)
            print("single student model instance : ",single_student)

            #convert complex data into python data
            py_obj_student = StudentSerializer(single_student)
            print("python data : ",py_obj_student.data)
            
            #py data convert into json and send of the client
            return JsonResponse(py_obj_student.data,safe=False)
      
    except Exception as ex:
        print("my exception name is -> {}".format(ex))
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])       
def all_student_view(request):
    try:
        #create instance of the student model class
        all_student = Student.objects.all()
        
        #convert complex data into python data
        py_obj_students = StudentSerializer(all_student, many=True)
      
        #py data convert into json  #send the client end or front end
        #json_data = json.dumps(py_obj_students.data)

       
        #return HttpResponse(json_data, content_type="application/json")
        return JsonResponse(py_obj_students.data,safe=False)
    
    except Exception as ex:
        print("my exception name is {}".format(ex))
        return HttpResponse(str(ex))

@api_view(["POST"]) 
def create_student(request):
   try:
        #get the student in the req body
        student_data_json = request.body
        print("request body data",student_data_json)
        
        #change student data into bytes data
        stream = io.BytesIO(student_data_json)
        print("stream data",stream)
        
        #change stream data into python native data
        py_data = JSONParser().parse(stream)
        print("python data ",py_data)

        #change python native data into complex data
        serializer = StudentSerializerCreate(data=py_data)
        print(serializer)

        if serializer.is_valid():
            serializer.save()
            res_msg = {"response_message":"given data is created", "status":status.HTTP_201_CREATED}
            return JsonResponse(data=[serializer.validated_data,res_msg], safe=False)
        else :
            print("serializer error ->",serializer.errors)
            return JsonResponse(serializer.errors, safe=False)

   except Exception as ex:
       print("my exception name is {}".format(ex))
       return HttpResponse(str(ex))

@api_view(["PUT"]) 
def update_student(request):
   try:
        #get the student in the req body
        student_data_json = request.body
        print("request body data",student_data_json)
        
        #change student data into bytes data
        stream = io.BytesIO(student_data_json)
        print("stream data",stream)
        
        #change stream data into python native data
        py_data = JSONParser().parse(stream)
        print("python data ",py_data)

        #get id of student
        id = py_data.get("id")
        if id is not None:
            student = Student.objects.get(id=id)
        serializer = StudentSerializerUpdate(student, data=py_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            res_msg = {"response_message":"given data is updated", "status":200}
            return JsonResponse(data=[serializer.validated_data,res_msg], safe=False)
        else:
            return HttpResponse(str(serializer.error_messages))

   except Exception as ex:
       print("my exception name is {}".format(ex))
       return HttpResponse(str(ex))     

@api_view(["DELETE"])
def delete_student(request):
   
    json_data = request.body
    print("json data -> {}".format(json_data))
    
    py_data = json.loads(json_data)
    print("python data -> {}".format(py_data))
    
    student_id = py_data.get("id")
    print("student id -> {}".format(student_id))

    student = Student.objects.get(id=student_id)
    print("student object -> {}".format(student))

    Student.delete(student)
    return JsonResponse({"message":"student is deleted"})

