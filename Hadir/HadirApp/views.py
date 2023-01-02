from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import User, Student, Class, Image
import re  # regex

# Create your views here.


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


def detail(request):
    users = User.objects.all()
    students = Student.objects.all()
    # images = Image.objects.all()
    classes = Class.objects.all()
    context = {'users': users, 'students': students, 'classes': classes}
    return render(request, 'HadirApp/detail.html', context)


def register(request):

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

    # context = {
    #     'err':err,
    # }
    return render(request, 'HadirApp/register.html')


def login(request):

    if request.method == 'POST':
        logEmail = request.POST['email']
        logPassword = request.POST['password']
        if User.objects.filter(password=logPassword, email=logEmail).exists():
            user = User.objects.get(password=logPassword, email=logEmail)
            user.save()
            print(f'welcome back {user}')
            # return redirect(f'/{user.username}/welcomeBack')
            return redirect('/Hadir/main')
        elif User.objects.filter(email=logEmail).exists():
            passErr = ('Password is Invalid')
            return render(request, 'HadirApp/login.html', {'passErr': passErr, })

        else:
            emailErr = ('Email is Invalid')
            return render(request, 'HadirApp/login.html', {'emailErr': emailErr, })

        #     if User.objects.get(email=logEmail):
        #         if User.objects.get(password=logPassword):

        #             print(f'welcome back {user}')
        #             redirect(f'/{user.username}/welcomeBack')
        #         else:
        #             redirect('/404')
        #             print('Wrong Password')
        #     else:
        #         redirect('/404')
        #         print("Email Doesnt Exsist")
        # except:

    return render(request, './HadirApp/login.html')


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

                if st.classes == classes:
                    idErr = 'A Student with this ID already exsist in this class'
                    print(idErr)
                    return render(request, 'HadirApp/student_enrollment.html', {'idErr': idErr})
                pass
            elif not match:
                wrongID = 'Invalid Student ID!'
                print(wrongID)
                return render(request, 'HadirApp/student_enrollment.html', {'wrongID': wrongID})
                # see the vid https://www.youtube.com/watch?v=f3iytAmzuNQ&t=298s
            student = Student.objects.create(
                name=name, student_id=student_id)  # classes=classes

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


def mainPage(request):

    return render(request, 'HadirApp/MainPage.html')


def images(request):
    image = Image.objects.all()
    for img in image:  # muted!!
        print(img)
    return render(request, 'HadirApp/images.html', {'image': image})


def create_class(request):

    if request.method == 'POST':
        classID = request.POST['classID']
        className = request.POST['className']
        # numOfStudents = request.POST['numOfStudents']

        try:
            # num_of_students=numOfStudents
            if Class.objects.filter(class_id=classID).exists():
                idErr = 'A Class with this ID already exsists'
                print(idErr)
                return render(request, 'HadirApp/class_form.html', {'idErr': idErr})

            newClass = Class.objects.create(
                class_id=classID, class_name=className,)
            newClass.save()
            succes = (f"Class {className}-{classID} Created Succesfuly")
            print(succes)
            return redirect(f'/Hadir/student_enrollment/{className}-{classID}')
        except:
            print('404 Not Found')
            return redirect('/Hadir/404')
    # qrimg = qrcode.make('secID')
    return render(request, 'HadirApp/class_form.html')


def Classes(request):
    classes = Class.objects.all()
    return render(request, 'HadirApp/classes.html', {'classes': classes})



def clas(request, class_id, class_name):

    try:
        if Class.objects.filter(class_id=class_id).exists():
            currentClass = Class.objects.get(class_id=class_id)
            students = Student.objects.all()
            classStd = []
            for student in students:
                print(
                    f'student === {student},,,, classes === {student.classes.all()}')
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

def welcomeBack(request, username):
    return HttpResponse(f"welcome {username}")
# old way

    # template = loader.get_template('HadirApp/welcome.html')
    # context = RequestContext(request, {

    #     'latest_users': latest_users,
    # })
    # context_dict = context.flatten()
    # return HttpResponse(template.render(context_dict))


def absent(request, student_id):
    student = get_object_or_404(Student, pk=student_id)


def PageNotFound(request):
    return render(request, 'HadirApp/404.html')
