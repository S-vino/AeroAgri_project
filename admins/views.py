from aero.models import employee
from client.models import registration, req_details
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
import random


def admins_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if username == "admin" and password == "admin":
            messages.success(request, "Admin Login Successful")
            return render(request, 'admins/admins_home.html')
        elif username != "admin" and password == "admin":
            messages.error(request, "Wrong Username")
            return render(request, 'admins/admins_login.html')
        elif password != "admin" and username == "admin":
            messages.error(request, "wrong Password")
            return render(request, 'admins/admins_login.html')
        elif username != "admin" and password != "admin":
            messages.error(request, "Invalid Username and Password")
        else:
            return render(request, 'admins/admins_login.html.html')
    return render(request,'admins/admins_login.html')

def admins_logout(request):
    if 'user_id' in request.session:
        request.session.pop('user_id',None)
        messages.success(request,'Logout successful')
        return redirect('/admins_logout/')
    else:
        messages.success(request, 'Logout successful')
        return redirect('/')

def admins_home(request):
    return render(request, 'admins/admins_home.html')

def client_details(request):
    datas = registration.objects.all()
    return render(request, 'admins/client_details.html', {"datas": datas})

def approve(request, id):
    datas =registration.objects.get(id=id)
    c=datas.fullname
    p = random.randint(10000, 50000)
    datas.password = p
    datas.client_id = f"CLI-{p}"
    print(p)
    send_mail(
        'Your Client Registration has been Approved',
        'Hello "{0}", Your profile has been Approved. Your password is "{1}". Make sure your enter this pasword while your logging in to the portal. '.format(c,p),
        'anvi.aadiv@gmail.com',
        [datas.email],
        fail_silently=False,
    )
    datas.approve = True
    datas.reject = False
    datas.save()
    messages.info(request, f"{datas.client_id} Approval Email send to {datas.email} Successfully.")
    return render(request, 'admins/client_details.html')

def reject(request, id):
    datas =registration.objects.get(id=id)
    c=datas.fullname
    send_mail(
        'Your Client Registration Rejected',
        'Hello "{0}", We regret to inform you that, Your profile got rejected.'.format(c),
        'anvi.aadiv@gmail.com',
        [datas.email],
        fail_silently=False,
    )

    datas.reject = True
    datas.approve = False
    datas.save()
    messages.info(request, "Rejection Email send to Client.")
    return render(request, 'admins/client_details.html')

def am_details(request):
    datas=employee.objects.filter(empdepartment="AeroMistfier")
    return render(request,'admins/aero_details.html',{"datas":datas})

def aero_approve(request, id):
    datas = employee.objects.get(id=id)
    c = datas.empname
    p = random.randint(10000, 50000)
    datas.emppassword = p
    s=datas.id
    datas.id=s
    datas.empid = f"EMP-100{s}"
    print(p)
    send_mail(
        'Your Aero-Mistifier Registration has been Approved',
        'Hi "{0}", your Aero-Mistifier profile has been Approved. Your password is "{1}". Make sure you enter this password while you logging in to the portal. '.format(
            c, p),
        'anvi.aadiv@gmail.com',
        [datas.empemail],
        fail_silently=False,
    )
    datas.grant = True
    datas.revoke = False
    datas.save()
    messages.info(request, "Acceptance Email send to Aero-Mistifier Successfully.")
    return render(request, 'admins/aero_details.html')


def aero_reject(request, id):
    datas =employee.objects.get(id=id)
    c=datas.empname
    send_mail(
        'Your Aero-Mistifier Registration Rejected',
        'Hi "{0}", We regret to inform you that, Your Aero-Mistifier profile got rejected.'.format(c),
        'anvi.aadiv@gmail.com',
        [datas.empemail],
        fail_silently=False,
    )
    datas.revoke = True
    datas.grant = False
    datas.save()
    messages.info(request, "Rejection Email send to Aero-Mistifier.")
    return render(request, 'admins/aero_details.html')

def soil_details(request):
    datas=employee.objects.filter(empdepartment="SoilProfiler")
    return render(request,'admins/soil_details.html',{"datas":datas})

def soil_approve(request, id):
    datas = employee.objects.get(id=id)
    c = datas.empname
    p = random.randint(10000, 50000)
    datas.emppassword = p
    s = datas.id
    datas.id = s
    datas.empid = f"EMP-100{s}"
    print(p)
    send_mail(
        'Your Soil-Profiler Registration has been Approved',
        'Hi "{0}", your Soil-Profiler profile has been Approved. Your password is "{1}". Make sure you enter this password while you logging in to the portal. '.format(
            c, p),
        'anvi.aadiv@gmail.com',
        [datas.empemail],
        fail_silently=False,
    )
    datas.accept = True
    datas.decline = False
    datas.save()
    messages.info(request, "Acceptance Email send to Soil-Profiler Successfully.")
    return render(request, 'admins/soil_details.html')

def soil_reject(request, id):
    datas =employee.objects.get(id=id)
    c=datas.empname
    send_mail(
        'Your Soil-Profiler Registration Rejected',
        'Hi "{0}", We regret to inform you that, Your Aero-Mistifier profile got rejected.'.format(c),
        'anvi.aadiv@gmail.com',
        [datas.empemail],
        fail_silently=False,
    )
    datas.decline = True
    datas.accept = False
    datas.save()
    messages.info(request, "Rejection Email send to Soil-Profiler.")
    return render(request, 'admins/soil_details.html')

def system_details(request):
    datas=employee.objects.filter(empdepartment="SystemCare Hub")
    return render(request,'admins/system_details.html',{"datas":datas})

def system_approve(request, id):
    datas = employee.objects.get(id=id)
    c = datas.empname
    p = random.randint(10000, 50000)
    datas.emppassword = p
    s = datas.id
    datas.id = s
    datas.empid = f"EMP-100{s}"
    print(p)
    send_mail(
        'Your SystemCare Hub Registration has been Approved',
        'Hi "{0}", your SystemCare Hub profile has been Approved. Your password is "{1}". Make sure you enter this password while you logging in to the portal. '.format(
            c, p),
        'anvi.aadiv@gmail.com',
        [datas.empemail],
        fail_silently=False,
    )
    datas.admit = True
    datas.deny = False
    datas.save()
    messages.info(request, "Acceptance Email send to SystemCare Hub Successfully.")
    return render(request, 'admins/system_details.html')

def system_reject(request, id):
    datas =employee.objects.get(id=id)
    c=datas.empname
    send_mail(
        'Your SystemCare Hub Registration Rejected',
        'Hi "{0}", We regret to inform you that, Your SystemCare Hub profile got rejected.'.format(c),
        'anvi.aadiv@gmail.com',
        [datas.empemail],
        fail_silently=False,
    )
    datas.deny = True
    datas.admit = False
    datas.save()
    messages.info(request, "Rejection Email send to SystemCare Hub.")
    return render(request, 'admins/system_details.html')


def aero_report(request):
    datas = req_details.objects.filter(amdone1=True)
    return render(request,'admins/Reports/aero_view_report.html',{'datas':datas})

def soil_report(request):
    datas = req_details.objects.filter(sdone2=True)
    return render(request,'admins/Reports/soil_view_report.html',{'datas':datas})

def system_report(request):
    datas = req_details.objects.filter(sysdone3=True)
    return render(request,'admins/Reports/system_view_report.html',{'datas':datas})

def invoicehome(request):
    datas=registration.objects.filter(sysdone=True)
    return render(request, 'admins/invoice.html', {'datas': datas})

def invoice(request,id):
    data=registration.objects.get(id=id)
    if request.method == 'POST':
        amount=request.POST['amount']
        data.amount=amount
        data.save()
        messages.info(request, "Bill sent to client successfully")
        return render(request, 'admins/invoice.html')
    return render(request, 'admins/invoice.html')


def payslip(request):
    datas=registration.objects.filter(sysdone=True)
    return render(request, 'admins/payslip_status.html', {'datas': datas})