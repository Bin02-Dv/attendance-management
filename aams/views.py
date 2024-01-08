from multiprocessing import context
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AddCourse, StudentCourse, Student, Attendance, Lecturer
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def index(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

# Student Section Start

def student_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('student-page')
        else:
            messages.info(request, 'Incorrect Regisration Number')
            return redirect('student-login')
    else:
        return render(request, 'student-login.html')

@login_required(login_url='student-login')
def student_page(request):
    student = Student.objects.get(user=request.user)
    return render(request, 'student-page.html', {'student':student})


@login_required(login_url='student-login')
def student_attendance_view(request):
    current_student = User.objects.get(username=request.user)
    students = Attendance.objects.filter(student_regis=current_student)

    context = {
        'students':students
    }

    return render(request, 'student-attendance-view.html', context)


@login_required(login_url='student-login')
def student_course_registration(request):
    course_list = AddCourse.objects.all()
    student_course = StudentCourse.objects.get(user=request.user)
    if request.method == 'POST':

        if request.POST.get('course_1') == None:
            course_1 = request.POST['course_1']
            course_2 = request.POST['course_2']
            course_3 = request.POST['course_3']
            course_4 = request.POST['course_4']

            student_course.course_1 = course_1
            student_course.course_2 = course_2
            student_course.course_3 = course_3
            student_course.course_4 = course_4
            student_course.save()
        
        if request.POST.get('course_1') != None:
            course_1 = request.POST['course_1']
            course_2 = request.POST['course_2']
            course_3 = request.POST['course_3']
            course_4 = request.POST['course_4']

            student_course.course_1 = course_1
            student_course.course_2 = course_2
            student_course.course_3 = course_3
            student_course.course_4 = course_4
            student_course.save()

            messages.info(request, 'Course added successfully..')
            return redirect('student-page')

    context = {
        'course_list':course_list,
        'student_course':student_course
    }
    return render(request, 'student-course-registration.html', context)


@login_required(login_url='student-login')
def student_course_view(request):
    courses = StudentCourse.objects.filter(user=request.user)
    course_1 = AddCourse.objects.all()
    
    context = {
        'courses':courses,
        'course_1':course_1
    }

    return render(request, 'student-course-view.html', context)

# Student Section ends


# Lecturer Section Start

def lecturer_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_staff == True:
                auth.login(request, user)
                return redirect('lecturer-page')
            else:
                messages.info(request, 'Sorry You are not allowed to access this page!!!')
                return redirect('lecturer-login')
        else:
            messages.info(request, 'Incorrect Username/Password')
            return redirect('lecturer-login')
    else:
        return render(request, 'lecturer-login.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_superuser == True:
                auth.login(request, user)
                return redirect('admin-page')
            else:
                messages.info(request, 'Sorry You are not allowed to access this page!!!')
                return redirect('admin-login')
        else:
            messages.info(request, 'Incorrect Username/Password')
            return redirect('admin-login')
    else:
        return render(request, 'admin-login.html')


@login_required(login_url='lecturer-login')
def lecturer_page(request):
    current_lecturer = User.objects.get(username=request.user)
    return render(request, 'lecturer-page.html', {'current_lecturer':current_lecturer})


@login_required(login_url='lecturer-login')
def take_student_attendance(request):
    student = Student.objects.all()
    course_list = AddCourse.objects.all()
    current_lecturer = User.objects.get(username=request.user)
    student_regis = User.objects.get(username=request.user)

    if request.method == 'POST':
        lecturer = current_lecturer.username
        course_title = request.POST['course']
        # course_code = AddCourse.objects.filter(course_title=course_title)
        student_regis = request.POST['student']
        # student_name = Student.objects.filter(student_regis=student_regis)
        ca1 = request.POST['ca1']
        ca2 = request.POST['ca2']
        exam = request.POST['exam']

        # if current_lecturer  and Attendance.objects.filter(student=student).exists():
        #     messages.info(request, 'Student already exist..')
        #     return redirect('take-student-attendance')
        # else:
        new_attendance = Attendance.objects.create(
            lecturer=lecturer, student_regis=student_regis, course_title=course_title, 
            first_CA=ca1, second_CA=ca2, exams=exam
        )
        new_attendance.save()
        messages.info(request, 'Attendance added successfully...')
        return redirect('view-student-attendance')

    context = {
        'student':student,
        'course_list':course_list,
        'current_lecturer':current_lecturer
    }
    return render(request, 'take-student-attendance.html', context)


@login_required(login_url='lecturer-login')
def view_student_attendance(request):
    # student = User.objects.get(username=request.user)
    current_lecturer = User.objects.get(username=request.user)
    lecturer = Attendance.objects.filter(lecturer=current_lecturer)
    # student_name = Student.objects.all()

    context = {
        'lecturer':lecturer,
        # 'student_name':student_name
    }
    return render(request, 'view-student-attendance.html', context)

# Lecturer Section ends

def student_logout(request):
    auth.logout(request)
    return redirect('student-login')

def lecturer_logout(request):
    auth.logout(request)
    return redirect('lecturer-login')

def admin_logout(request):
    auth.logout(request)
    return redirect('admin-login')


def update(request, id):
  student_atten = Attendance.objects.get(id=id)
  template = loader.get_template('edit.html')
  context = {
    'student_atten': student_atten,
  }
  return HttpResponse(template.render(context, request))


def updaterecord(request, id):
    student_regis = request.POST['student']
    course_title = request.POST['course']
    ca1 = request.POST['ca1']
    ca2 = request.POST['ca2']
    exam = request.POST['exam']

    student_atten = Attendance.objects.get(id=id)
    student_atten.student_regis = student_regis
    student_atten.course_title = course_title
    student_atten.first_CA = ca1
    student_atten.second_CA = ca2
    student_atten.exams = exam
    student_atten.save()
    messages.info(request, 'Attendance Updated successfully...')
    return HttpResponseRedirect(reverse('view-student-attendance'))

def request_for_delete(request, id):
    student_atten = Attendance.objects.get(id=id)
    context = {
    'student_atten': student_atten,
  }
    return render(request, 'request-for-delete.html', context)

def course_request_for_delete(request, id):
    course = AddCourse.objects.get(id=id)
    current_user = User.objects.get(username=request.user.username)
    context = {
    'course': course,
    'current_user': current_user
  }
    return render(request, 'course-request-for-delete.html', context)

def lec_request_for_delete(request, id):
    lec = User.objects.get(id=id)
    current_user = User.objects.get(username=request.user.username)
    context = {
    'lec': lec,
    'current_user': current_user
  }
    return render(request, 'request-for-delete-lec.html', context)

def stu_request_for_delete(request, id):
    stu = User.objects.get(id=id)
    current_user = User.objects.get(username=request.user.username)
    context = {
    'stu': stu,
    'current_user': current_user
  }
    return render(request, 'request-for-delete-stu.html', context)

def lec_delete(request, id):
    lec = User.objects.get(id=id)
    lec.delete()
    messages.info(request, 'Lecturer Deleted successfully...')
    return HttpResponseRedirect(reverse('view-user'))

def stu_delete(request, id):
    stu = User.objects.get(id=id)
    stu.delete()
    messages.info(request, 'Student Deleted successfully...')
    return HttpResponseRedirect(reverse('view-student'))

def delete(request, id):
    studen_atten = Attendance.objects.get(id=id)
    studen_atten.delete()
    messages.info(request, 'Attendance Deleted successfully...')
    return HttpResponseRedirect(reverse('view-student-attendance'))


def course_delete(request, id):
    course = AddCourse.objects.get(id=id)
    course.delete()
    messages.info(request, 'Course Deleted successfully...')
    return HttpResponseRedirect(reverse('view-courses'))

def level(request):
    return render(request, 'level.html')

def take_attendance_for_level1(request):
    course = AddCourse.objects.all()
    students = Student.objects.all()
    context = {
        'course':course,
        'students':students
    }
    return render(request, 'take-attendance-for-level1.html', context)

def take_attendance_for_level2(request):
    course = AddCourse.objects.all()
    students = Student.objects.all()
    context = {
        'course':course,
        'students':students
    }
    return render(request, 'take-attendance-for-level2.html', context)

@login_required(login_url='lecturer-login')
def admin_2(request):
    current_admin = User.objects.get(username=request.user)
    return render(request, 'admin-page.html', {'current_admin':current_admin})
    
def add_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Staff already exist.')
        elif cpassword != password:
            messages.info(request, 'password and comfirm password missed match.')
        else:
            new_staff = User.objects.create_user(
                username=username, email=email, password=password, is_staff=True
            )
            new_staff.save()

            # creating the staffs table.
            get_staff1 = User.objects.get(username=username)
            create_staff = Lecturer.objects.create(user=get_staff1, id_user=get_staff1.id)
            create_staff.save()
            messages.info(request, 'Staff create successfully...')
            return redirect('view-user')
    return render(request, 'add-users.html')

def view_user(request):
    staffs = Lecturer.objects.all()
    return render(request, 'view-users.html', {'staffs': staffs})

def add_course(request):
    if request.method == 'POST':
        course_code = request.POST['course-code']
        course_title = request.POST['course-title']
        course_unit = request.POST['course-unit']

        if AddCourse.objects.filter(course_code=course_code).exists():
            messages.info(request, 'course code already exist..')
            return redirect('add-courses')
        elif AddCourse.objects.filter(course_title=course_title).exists():
            messages.info(request, 'course title already exist..')
            return redirect('add-courses')
        else:
            new_course = AddCourse.objects.create(
                course_code=course_code, course_title=course_title, unit=course_unit
            )
            new_course.save()
            messages.info(request, 'Course registered successfully...')
            return redirect('view-courses')
    return render(request, 'add-courses.html')

def view_course(request):
    courses = AddCourse.objects.all()
    return render(request, 'view-courses.html', {'courses':courses})

def view_student(request):
    students = Student.objects.all()
    return render(request, 'view-student.html', {'students':students})

def add_student(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Student already exist.')
        elif cpassword != password:
            messages.info(request, 'password and comfirm password missed match.')
        else:
            new_student = User.objects.create_user(
                username=username, email=email, password=password
            )
            new_student.save()

            # creating the student table.
            get_student1 = User.objects.get(username=username)
            create_student = Student.objects.create(user=get_student1, id_user=get_student1.id)
            create_student.save()

            # creating the student courses.
            get_student2 = User.objects.get(username=username)
            create_course = StudentCourse.objects.create(user=get_student2, id_user=get_student2.id)
            create_course.save()
            messages.info(request, 'Student create successfully...')
            return redirect('view-student')
    return render(request, 'add-student.html')

def update_student(request, id):
    users = Student.objects.get(id=id)

    if request.method == 'POST':

        if request.FILES.get('img') == None:
            image = users.profileImg
            f_name = request.POST['f-name']
            level = request.POST['level']

            users.profileImg = image
            users.student_name = f_name
            users.student_level = level
            users.save()
            messages.info(request, 'Student Record Updated successfully..')
            return redirect('view-student')
        
        if request.FILES.get('img') != None:
            image = request.FILES.get('img')
            f_name = request.POST['f-name']
            level = request.POST['level']

            users.profileImg = image
            users.student_name = f_name
            users.student_level = level
            users.save()
            messages.info(request, 'Student Record Updated successfully..')
            return redirect('view-student')
    return render(request, 'update-student.html', {'users':users})


def update_staff(request, id):
    users = Lecturer.objects.get(id=id)
    courses = AddCourse.objects.all()

    if request.method == 'POST':

        if request.POST.get('f-name') == None:
            f_name = request.POST['f-name']
            course = request.POST['course']

            users.lecturer_name = f_name
            users.course_taking = course
            users.save()
            messages.info(request, 'Staff Record Updated successfully..')
            return redirect('view-staff')
        
        if request.POST.get('f-name') != None:
            f_name = request.POST['f-name']
            course = request.POST['course']

            users.lecturer_name = f_name
            users.course_taking = course
            users.save()
            messages.info(request, 'Staff Record Updated successfully..')
            return redirect('view-user')
    return render(request, 'update-staff.html', {'users':users, 'courses':courses})