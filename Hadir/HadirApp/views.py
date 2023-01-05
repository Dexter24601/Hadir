import re  # regex
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegisterForm
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Class, Image, Attendance

from datetime import date

import sys
sys.setrecursionlimit(10000)


def temp(request):
    return redirect('/Hadir/')


def index(request):
    # username = User.username
    # template = loader.get_template('HadirApp/index.html')
    # context = RequestContext(request, {
    #     'username': username,
    # })
    # # Because Context() is deprecated in django 1.11  .
    # context_dict = context.flatten()
    # return HttpResponse(template.render(context_dict))
    # latest_users = User.objects.order_by('-reg_date')[:5]
    # output = ", ".join(q.username for q in latest_users)
    # return HttpResponse(output)
    return render(request, 'HadirApp/index.html')


@login_required(login_url='./login')
def detail(request):
    users = User.objects.all()
    students = Student.objects.all()
    # images = Image.objects.all()
    classes = Class.objects.all()
    context = {'users': users, 'students': students, 'classes': classes}
    return render(request, 'HadirApp/detail.html', context)


def registerPage(request):

    if request.user.is_authenticated:
        return redirect('/Hadir/main')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.save()
                login(request, user)
                # print(f" 11111111111111111{form.username}")
                # print(user.username)
                return redirect('/Hadir/main')
                # return render(request, 'HadirApp/MainPage.html', {'user': user})

        else:
            print(request.method)
            form = RegisterForm()
            user = None
        return render(request, 'HadirApp/register.html', {'form': form})

    '''
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']  # Regex later !!!!!!
        password2 = request.POST['password2']
        # user_id = request.POST['user_id']

        try:
            if User.objects.filter(email=email).exists():
                err = (f'A user with this Email already exist!')
                return render(request, 'HadirApp/register.html', {'err': err, })

            elif password != password2:
                err = (f'Passwords Doesnt Match!')
                return render(request, 'HadirApp/register.html', {'err2': err, })

            user = User.objects.create(
                email=email, username=username, password=password,)
            user.save()
            print(f' User "{user}" created')
            # return redirect(f'/{username}/welcomeBack')
            return redirect(f'/Hadir/main')
        except:
            print("ERROR")
            return redirect('/404')

    context = {
        'err':err,
    }
    return render(request, 'HadirApp/sign-up.html', {'form': form})
    '''


def loginPage(request):  # redirect to the page user was on

    if request.user.is_authenticated:
        return redirect('/Hadir/main')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            logPassword = request.POST.get('password')
            # rawPass = logPassword.clear

            user = authenticate(request, username=username,
                                password=logPassword)
            if user is not None:
                login(request, user)
                print(f'User {user} has logged in succesfuly')
                # return render(request, 'HadirApp/MainPage.html', {'user': user})
                return redirect('/Hadir/main')
            else:
                Err = ('Email/Password is Invalid')
                return render(request, './HadirApp/login.html', {'Err': Err})

            # old way
            '''
        if User.objects.filter(password=logPassword, email=logEmail).exists():
            user = User.objects.get(password=logPassword, email=logEmail)
            user.save()
            print(f'welcome back {user}')
            if user is not None:
                login(request, user)
            # login(request, user)
            # return redirect(f'/{user.username}/welcomeBack')
            return render(request, 'HadirApp/MainPage.html', {'user': user})
        elif User.objects.filter(email=logEmail).exists():
            passErr = ('Password is Invalid')
            return render(request, 'HadirApp/login.html', {'passErr': passErr, })

        else:
            emailErr = ('Email is Invalid')
            return render(request, 'HadirApp/login.html', {'emailErr': emailErr, })
        '''
            '''
            if Instructor.objects.get(email=logEmail):
                if Instructor.objects.get(password=logPassword):

                    print(f'welcome back {user}')
                    redirect(f'/{user.username}/welcomeBack')
                else:
                    redirect('/404')
                    print('Wrong Password')
            else:
                redirect('/404')
                print("Email Doesnt Exsist")
            except:
            '''
        else:
            return render(request, './HadirApp/login.html',)


@login_required(login_url='./login')
def LogoutUser(request):
    logout(request)
    # return render(request, 'HadirApp/login.html')
    return redirect('/Hadir/login')


@login_required(login_url='./login')
def mainPage(request):

    # if request.method == "POST":
    # if user is not None:
    #     currentUser = user
    # {'currentUser': currentUser}
    return render(request, 'HadirApp/MainPage.html')
    # else:
    #     print(request.method)
    #     return redirect('/Hadir/login')


def student_enrollment(request, class_name, class_id):

    if request.method == 'POST':
        name = request.POST['name']
        student_id = request.POST['student_id']
        images = request.FILES.getlist('images')
        if Class.objects.filter(class_id=class_id).exists:
            classes = Class.objects.get(class_id=class_id)
            print(classes)
        else:
            print('404 Class Not Found')
            return redirect('/Hadir/404')

        match = re.match(r'^(4)(\d{2}0\d{4})$', student_id)

        try:
            if Student.objects.filter(student_id=student_id).exists():
                st = Student.objects.get(student_id=student_id)
                print(st.classes.all())

                for clas in st.classes.all():
                    if clas == classes:
                        idErr = 'A Student with this ID already exsist in this class'
                        print(idErr)
                        return render(request, 'HadirApp/student_enrollment.html', {'idErr': idErr})

                st.classes.add(classes)
                st.save()

                # succMsg = (f'Student {st.name} has been added to {classes.class_name} class succesfuly')
                # print(succMsg)

                messages.success(
                    request, f'Student {st.name} has been added to {classes.class_name} class succesfuly')
                # 'succMsg':succMsg
                return render(request, 'HadirApp/student_enrollment.html', {'class_name': classes.class_name})

            elif not match:
                wrongID = 'Invalid Student ID!'
                print(wrongID)
                return render(request, 'HadirApp/student_enrollment.html', {'wrongID': wrongID})
                # see the vid https://www.youtube.com/watch?v=f3iytAmzuNQ&t=298s

            student = Student.objects.create(
                name=name, student_id=student_id)  # classes=classes

            print('alive!')
            student.classes.add(classes)  # solution for many to many
            student.save()
            print(f'student {student} is registered')

            for image in images:
                # print(image)
                # print(student.student_id)
                Image.objects.create(images=image, student=student)
            images = Image.objects.all()
        except:
            print('404 Not Found')
            return redirect('/Hadir/404')

    return render(request, 'HadirApp/student_enrollment.html', {'class_name': class_name})


def upload(request):
    if request.method == "POST":
        images = request.FILES.getlist('images')
        for image in images:
            User.objects.create(images=image)
    images = User.objects.all()
    return render(request, 'index.html', {'images': images})


@login_required(login_url='./login')
def images(request):
    image = Image.objects.all()
    for img in image:
        print(img)
    return render(request, 'HadirApp/images.html', {'image': image})


@login_required(login_url='./login')
def create_class(request):

    if request.method == 'POST':
        classID = request.POST['classID']
        className = request.POST['className']
        # numOfStudents = request.POST['numOfStudents']

        matchName = re.match(r'\D{3,50}', className)
        matchID = re.match(r'\d{3}', classID)

        if not matchName:
            nameErr = 'Invalid Class Name'
            return render(request, 'HadirApp/class_form.html', {'nameErr': nameErr})
        elif not matchID:
            IDErr = 'Invalid Class ID'
            return render(request, 'HadirApp/class_form.html', {'IDErr': IDErr})

        try:
            # num_of_students=numOfStudents
            if Class.objects.filter(class_id=classID).exists():
                idErr = 'A Class with this ID already exsists'
                print(idErr)
                return render(request, 'HadirApp/class_form.html', {'idErr': idErr})

            newClass = Class.objects.create(
                class_id=classID, class_name=className, instructor=request.user)
            newClass.save()
            succes = (f"Class {className}-{classID} Created Succesfuly")
            print(succes)
            return redirect(f'/Hadir/student_enrollment/{className}-{classID}')
        except:
            print('404 Not Found')
            return redirect('/Hadir/404')
    # qrimg = qrcode.make('secID')
    return render(request, 'HadirApp/class_form.html')


@login_required(login_url='./login')
def Classes(request):
    # print(request.user)
    if Class.objects.filter(instructor=request.user).exists():
        theClasses = []
        try:
            for clas in Class.objects.filter(instructor=request.user):
                # print(clas)
                if clas.instructor == request.user:
                    theClasses.append(clas)
                    print('class found')
        except:
            if Class.objects.filter(instructor=request.user).instructor == request.user:
                theClasses.append(clas)

        return render(request, 'HadirApp/classes.html', {'theClasses': theClasses})

    else:
        err = "You dont Have Any Classes"
        return render(request, 'HadirApp/classes.html', {'err': err})


@login_required(login_url='./login')
def dashboard(request, class_name, class_id):
    students = []
    # for student in Student.objects.all():
    #     st
    return render(request, 'HadirApp/dashboard.html', {'class_name': class_name})


@login_required(login_url='./login')
def clas(request, class_id, class_name):

    try:
        if Class.objects.filter(class_id=class_id).exists():
            currentClass = Class.objects.get(class_id=class_id)
            students = Student.objects.all()
            classStd = []
            for student in students:
                # print(
                #     f'student === {student},,,, classes === {student.classes.all()}')
                for clas in student.classes.all():
                    if clas == currentClass:
                        classStd.append(student)
                        # classStd.save()

            if not classStd:
                print('no student in this class')

            print(classStd)

            return render(request, 'HadirApp/class.html', {'classStd': classStd, 'currentClass': currentClass})
        else:
            print('class 404 Not Found')
            return redirect('/Hadir/404')
            # here
    except:
        print('404 Not Found')
        return redirect('/Hadir/404')

    return render(request, 'HadirApp/class.html')  # , {'classStd': classStd}


@login_required(login_url='./login')
def attendance(request, class_name, class_id):

    today = date.today()
    print(today)
    students = Student.objects.all()

    # print(request.method)
    # print(Attendance.objects.all())
    if request.method == "POST":
        studentsNames = request.POST.getlist('student')
        prestudents = []
        for name in studentsNames:

            prestudents.append(Student.objects.get(name=name))

        clas = Class.objects.get(class_id=class_id)
        print(f'class: {clas} ')
        if Attendance.objects.filter(presence_date=today, clas=clas).exists():
            print("Exist (Attendance is Already done)")
            day = Attendance.objects.get(presence_date=today, clas=clas)
            print(day)
            for st in prestudents:

                day.student.add(st)
                day.save()
                print(f'{st} Marked As Present!')

        else:
            day = Attendance.objects.create(
                presence_date=today, clas=clas)
            day.save()
            print(f'{day} CREATED!')

            for st in prestudents:

                day.student.add(st)
                day.save()
                print(f'{st} Marked As Present!')

            #
            #     for day in presnt:
            #         day.student.add(prestudents)
            # else:
            #     presnt = Attendance.objects.filter(
            #         presence_date=today)
            #     # print(f'presnt: {presnt}')
            #     for day in presnt:
            #         day.student.add(prestudents)
            # st = Attendance.objects.get(presence_date=today)
            # st.student.add(student)
            # st.save()

        return render(request, 'HadirApp/take_attendance.html', {'prestudents': prestudents})
    # return render(request, 'HadirApp/take_attendance.html')

    # for student in Student.objects.all():
    #     if Attendance.objects.filter(student=student, presence_date=today).exists():
    #         student.precense = True
    #         student.save()

    # present = Attendance.objects.filter(st)
    # for st in Student.objects.filter(student):
    #     print(st)

    context = {'students': students,
               'class_name': class_name, 'class_id': class_id}
    return render(request, 'HadirApp/take_attendance.html', context)


@login_required(login_url='./login')
def attendanceResult(request, class_name, class_id):

    prestudents = request.POST.getlist('student')
    print(prestudents)

    # {'prestudents': prestudents}
    # return render(request, 'HadirApp/results.html')

    # else:
    #     return render('Hadir/404')
    return render(request, 'HadirApp/results.html', {'prestudents': prestudents})
    # old way

    # template = loader.get_template('HadirApp/welcome.html')
    # context = RequestContext(request, {

    #     'latest_users': latest_users,
    # })
    # context_dict = context.flatten()
    # return HttpResponse(template.render(context_dict))

    # def absent(request, student_id):
    #     student = get_object_or_404(Student, pk=student_id)


def PageNotFound(request):
    return render(request, 'HadirApp/404.html')
