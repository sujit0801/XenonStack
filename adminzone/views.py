from django.shortcuts import render,redirect
from genzone.models import AdminLogin,JobSeeker,Enquiry
from django.core.exceptions import ObjectDoesNotExist
from .models import Notification
import datetime

# Create your views here.
def adminhome(request):
    try:
        if request.session['adminid'] is not None:
            nf=Notification.objects.all()
            return render(request,"adminhome.html",{'nf':nf})
    except KeyError:
        return render(request,"login.html")
def jobseekers(request):
    try:
        if request.session['adminid'] is not None:
            jobs=JobSeeker.objects.all()
            return render(request,"jobseekers.html",{'jobs':jobs})
    except KeyError:
        return render(request, "login.html")
def enquiries(request):
    try:
        if request.session['adminid'] is not None:
            enq=Enquiry.objects.all()
            return render(request,"enquiries.html",{'enq':enq})
    except KeyError:
        return render(request, "login.html")
def changepassword(request):
    try:
        if request.session['adminid'] is not None:
            return render(request,"changepassword.html")
    except KeyError:
        return render(request, "login.html")
def logout(request):
    request.session['adminid']=None
    return render(request,"login.html")
def adminchangepwd(request):
    oldpassword=request.POST['oldpassword']
    newpassword=request.POST['newpassword']
    confirmpassword=request.POST['confirmpassword']
    msg='Message: '
    if newpassword!=confirmpassword:
        msg=msg+'New Password And Confirm Password are not Matched'
        return render(request,"changepassword.html",{'msg':msg})
    adminid=request.session['adminid']
    try:
        admin=AdminLogin.objects.get(adminid=adminid,password=oldpassword)
        if admin is not None:
            ad=AdminLogin(adminid=adminid,password=newpassword)
            ad.save()
            return redirect('adminzone:logout')
    except ObjectDoesNotExist:
        msg=msg+'Old Password is not Matched'
    return render(request,"changepassword.html",{'msg':msg})
def deleteenquiries(request,id):
    e=Enquiry.objects.get(id=id)
    e.delete()
    return redirect('adminzone:enquiries')

def deletejobseekers(request,emailid):
    j=JobSeeker.objects.get(emailaddress=emailid)
    j.delete()
    return redirect('adminzone:jobseekers')

def addnotification(request):
    notificationtext=request.POST['notificationtext']
    notificationdate=datetime.datetime.today()
    n=Notification(notificationtext=notificationtext,notificationdate=notificationdate)
    n.save()
    return redirect('adminzone:adminhome')

def deletenotification(request,id):
    n=Notification.objects.get(id=id)
    n.delete()
    return redirect('adminzone:adminhome')


