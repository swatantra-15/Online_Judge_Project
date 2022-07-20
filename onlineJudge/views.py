
import filecmp,subprocess
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.base import File
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from onlineJudge.models import Problems,Solutions,Test_Case

# Create your views here.
def register_request(request):
    return render(request , 'onlineJudge/register.html')

def register_verify(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            username = request.POST['username']
            password = request.POST['password1']
            email = request.POST['email']

            new_user = User.objects.create_user(username,email, password)
            new_user.save()
            messages.success(request , "Registration Successful", extra_tags='alert alert-success')
            return HttpResponseRedirect('/onlineJudge/problems/')
        else:
            messages.succes(request , "Both passsword should be same.", extra_tags='alert alert-danger')
            return HttpResponseRedirect('/onlineJudge/register/')
    else:
        return HttpResponse("Usage: Post method is not used.")

def login_request(request):
    return render(request ,'onlineJudge/login.html')

def login_check(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request , "Logged in successfully.", extra_tags='alert alert-success')
            return HttpResponseRedirect('/onlineJudge/problems/')
        else:
            messages.success(request , "Log in failed!! check username or password.", extra_tags='alert alert-danger')
            return HttpResponseRedirect('/onlineJudge/login/')
    else:
        return HttpResponse("Usage: Method used is not POST.")

def log_out(request):
    logout(request)
    messages.success(request , "Logout succesfully.", extra_tags='alert alert-success')
    return HttpResponseRedirect('/onlineJudge')

@login_required(login_url="/onlineJudge/login/")
def problems(request):
    problems_list = Problems.objects.all()
    context = {'problems_list' : problems_list}
    return render(request,'onlineJudge/problems.html',context)

@login_required(login_url="/onlineJudge/login/")
def problemDetails(request,problem_id,msg=""):
    problem = get_object_or_404(Problems,pk=problem_id)
    context = {
        'problem':problem,
        'message':msg
    }
    return render(request,'onlineJudge/problemStatement.html',context)

@login_required(login_url="/onlineJudge/login/")
def problemSubmit(request,problem_id):
    problem=Problems.objects.get(pk=problem_id)
    test=Test_Case.objects.get(Pname__Problem_Name=problem.Problem_Name)

    if request.method == "POST":
        
        userfile=request.FILES.get('solution',False)
        codeEditor=request.POST.get('solutionText',False)
        if(userfile):
            code=userfile.read()
            with open('temp.cpp','wb+') as tempf:
                tempf.write(code)
            tempf.close()

            outputf=open('tempf_out.txt','w')
            testout=(test.test_output.url)[1:]
            subprocess.call(["g++","temp.cpp","-o","temp.exe"],shell=True)
            k=subprocess.call(['temp.exe'],stdin=test.test_input,stdout=outputf,shell=True)
            outputf.close()
            if k:
                return HttpResponse("Internal error occurs")
            else:
                result=filecmp.cmp('tempf_out.txt',testout,shallow=False)
                if result:
                    file=open('temp.cpp')
                    myfile=File(file)
                    sol=Solutions(
                        user=request.user,
                        Pname=problem,
                        Language=request.POST['language'],
                        Code_file=myfile,
                        verdict='AC'
                    )
                    sol.save()
                    file.close()
                    return HttpResponseRedirect("/onlineJudge/submit/correct_ans/")
                else:
                    file =  open('temp.cpp')
                    myfile = File(file)
                    sol = Solutions(
                        user=request.user,
                        Pname=problem,
                        Language=request.POST['language'],
                        Code_file=myfile,
                        verdict='WA'
                    )
                    sol.save()
                    file.close()
                    return HttpResponseRedirect("/onlineJudge/submit/wrong_ans/")

        elif(codeEditor):
            byteContent=codeEditor.encode()
            with open('temp.cpp','wb+') as tempf:
                tempf.write(byteContent)
            tempf.close()

            outputf=open('tempf_out.txt','w')
            testint=test.test_input
            testout=(test.test_output.url)[1:]
            subprocess.call(["g++","temp.cpp","-o","temp.exe"],shell=True)
            k=subprocess.call(['temp.exe'],stdin=testint,stdout=outputf,shell=True)
            
            outputf.close()
            if k:
                return HttpResponse("Internal error occurs")
            else:
                result=filecmp.cmp('tempf_out.txt',testout,shallow=False)
                if result:
                    file=open('temp.cpp')
                    myfile=File(file)
                    sol=Solutions(
                        user=request.user,
                        Pname=problem,
                        Language=request.POST['language'],
                        Code_file=myfile,
                        verdict='AC'
                    )
                    sol.save()
                    file.close()
                    return HttpResponseRedirect("/onlineJudge/submit/correct_ans/")
                else:
                    file =  open('temp.cpp')
                    myfile = File(file)
                    sol = Solutions(
                        user=request.user,
                        Pname=problem,
                        Language=request.POST['language'],
                        Code_file=myfile,
                        verdict='WA'
                    )
                    sol.save()
                    file.close()
                    return HttpResponseRedirect("/onlineJudge/submit/wrong_ans/")
        else: 
            message="Please select a code file!!!!!"
            return problemDetails(request,problem_id,message)

    else:
        return HttpResponse("Method is not POST")

@login_required(login_url="/onlineJudge/login/")
def result(request , status):
    context = {'status':status}
    return render(request,'onlineJudge/submit.html',context)

@login_required(login_url="/onlineJudge/login/")
def problemSubmissions(request):
    submissions = Solutions.objects.all().order_by('-id')[:10]
    return render(request,'onlineJudge/submission.html', {'submissions' : submissions})
