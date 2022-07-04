import fileinput
import imp,os,filecmp,subprocess
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.files.base import ContentFile, File
from onlineJudge.models import Problems,Solutions

# Create your views here.
def problems(request):
    problems_list = Problems.objects.all()
    context = {'problems_list' : problems_list}
    return render(request,'onlineJudge/homepage.html',context)

def problemDetails(request,problem_id,msg=""):
    problem = get_object_or_404(Problems,pk=problem_id)
    context = {
        'problem':problem,
        'message':msg
    }
    return render(request,'onlineJudge/problemStatement.html',context)

def problemSubmission(request,problem_id):
    if request.method == "POST":
        f=request.FILES.get('solution',False)
        code=request.POST.get('solutionText',False)
        lang=request.Post.get('language',False)
        if(f):
            code=f.read()
            
        if(code):
            return render(request,'onlineJudge/submission.html',{'code':code})
        else: 
            message="Please select a code file"
            return problemDetails(request,problem_id,message)
    
        
        
