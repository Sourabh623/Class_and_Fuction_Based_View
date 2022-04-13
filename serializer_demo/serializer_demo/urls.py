from django.contrib import admin
from django.urls import path
from api.views import single_student_view, all_student_view,create_student
from api.views import update_student, delete_student


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/student/<int:pk>', single_student_view),
    path('api/student/', all_student_view),
    path('api/student-create/', create_student),
    path('api/student-update/', update_student),
    path('api/student-delete/', delete_student),

]
