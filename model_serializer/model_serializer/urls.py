from django.contrib import admin
from django.urls import path
from api.views import single_student_view, all_student_view,create_student
from api.views import update_student, delete_student, hello_world, bye_world,Employee, StudentApi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/hello', hello_world),
    path('api/bye', bye_world),
    path('api/employee', Employee),
    path('api/student/<int:pk>', single_student_view),
    path('api/student/', all_student_view),
    path('api/student-create/', create_student),
    path('api/student-update/', update_student),
    path('api/student-delete/', delete_student),
    path('api/studentapi/', StudentApi.as_view()),
    path('api/studentapi/<int:pk>', StudentApi.as_view()),
]
