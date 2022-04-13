import io
import json
from django.http import HttpResponse, JsonResponse
from .serializers import StudentSerializer
from .models import Student
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

#class based views
class StudentApi(APIView):
    def get(self, request, pk=None, format=None):
        try:
            id = pk        
            if id is not None:
                student = Student.objects.get(id=id)
                serializer = StudentSerializer(student)
                return Response(serializer.data)
            
            students = Student.objects.all()
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data)
        
        except Exception as ex:
            print("my exception name is {}".format(ex))
            return Response(str(ex), status=status.HTTP_404_NOT_FOUND)
        

    def post(self, request, format=None):
        print(request.data)
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Data is created."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,pk,format=None):
        if pk is not None:
            student = Student.objects.get(id=pk)
        serializer = StudentSerializer(student,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Complete Data is updated."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,pk,format=None):
        if pk is not None:
            student = Student.objects.get(id=pk)
        serializer = StudentSerializer(student,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"Partially Data is updated."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk, format=None):
        if pk is not None:
            student = Student.objects.get(id=pk)
            Student.delete(student)
            return Response({"Data is deleted."})
        return Response({"this id not present in db"}, status=status.HTTP_404_NOT_FOUND)




# function based views



# by default get methods
@api_view()
def hello_world(request):
    return Response({"message":"Hello World"})

# api view with get methods
@api_view(['GET'])
def bye_world(request):
    return Response({"message":"Bye World"})

@api_view(['GET', 'POST'])
def Employee(request):
    if request.method == 'POST':
        #change python native data into complex data
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = {"given data is created":request.data}
            return Response(res,status=status.HTTP_201_CREATED)
    return Response({"message":"Hello Employee"})

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
        return Response(status=status.HTTP_204_NO_CONTENT)
 
@api_view(["GET"])       
def all_student_view(request):
    try:
        #create instance of the student model class
        all_student = Student.objects.all()
        
        #convert complex data into python data
        py_obj_students = StudentSerializer(all_student, many=True)
       
        #return HttpResponse(json_data, content_type="application/json")
        return JsonResponse(py_obj_students.data,safe=False)
    
    except Exception as ex:
        print("my exception name is {}".format(ex))
        return Response(str(ex))

@api_view(["POST"]) 
def create_student(request):
   try:
        #change student data into bytes data
        print("req body data types ->",type(request.body))
        print("req data type ->",type(request.data))
        print("req data  ->",request.data)
        
        # stream = io.BytesIO(request.body)
        # print("stream data",stream)
        
        #change stream data into python native data
        # py_data = JSONParser().parse(stream)
        # print("python data ",type(py_data))

        #change python native data into complex data
        serializer = StudentSerializer(data=request.data)
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
        serializer = StudentSerializer(student, data=py_data, partial=True)

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

