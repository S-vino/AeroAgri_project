
from django.shortcuts import render, redirect
import pandas as pd
from django.contrib import messages
from aero.models import employee
from client.models import registration, req_details

def aeroregister(request):
    if request.method == 'POST':
        empname = request.POST['empname']
        empemail=request.POST['empemail']
        empaddress = request.POST['empaddress']
        empphone = request.POST['empphone']
        empdepartment = request.POST['empdepartment']
        employee(empname=empname,empemail=empemail,empaddress=empaddress,empphone=empphone,empdepartment=empdepartment).save()
        messages.info(request, "Aero Mistfier details registered successfully. Kindly Check Email for further Progress.")
        return render(request, 'aero/aero_login.html')
    return render(request, 'aero/aero_reg.html')

def aerologin(request):
    if request.method == 'POST':
        empemail = request.POST.get('empemail')
        emppassword = request.POST.get('emppassword')

        try:
            emp = employee.objects.get(empemail=empemail, emppassword=emppassword)
            if emp.grant:
                messages.info(request, "Aero Mistifier Login Successful")
                request.session['user_id'] = emp.empid
                print( request.session['user_id'])
                emp.save()
                return redirect('/aero_home/')
            else:
                messages.info(request, "You need management approval to access")
                return render(request, 'aero/aero_login.html')
        except employee.DoesNotExist:
            messages.info(request, "Invalid Email or Password")

    return render(request, 'aero/aero_login.html')

def aero_logout(request):
    if 'user_id' in request.session:
        request.session.pop('user_id',None)
        messages.success(request,'Logout successful')
        return redirect('/')
    else:
        messages.success(request, 'Logout successful')
        return redirect('/aero_logout/')

def aero_home(request):
    return render(request,'aero/aero_home.html')

def requirement(request):
    datas=req_details.objects.all()
    return render(request,'aero/prerequisite_report/view.html',{'datas':datas})


def process(request):
    datas=req_details.objects.all()
    return render(request,'aero/process data/process_view.html',{'datas':datas})


def process_aero(request, client_id):
    data = req_details.objects.filter(client_id=client_id)
    csv_path = r'C:\aero\aerophonics\Aeromistifier.csv'
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        for i in data:
            if (i.Plant_Type) == (row['Plant_Type']):
                i.Nutrient_Solution_Temperature = row['Nutrient_Solution_Temperature']
                i.Nutrient_Solution_pH = row['Nutrient_Solution_pH']
                i.Nutrient_Solution_Electrical_Conductivity = row['Nutrient_Solution_Electrical_Conductivity']
                i.Dissolved_Oxygen = row['Dissolved_Oxygen']
                i.Air_Temperature = row['Air_Temperature']
                i.Air_Humidity = row['Air_Humidity']
                i.Light_Intensity = row['Light_Intensity']
                i.CO2_Concentration = row['CO2_Concentration']
                i.Plant_Weight = row['Plant_Weight']
                i.Plant_Height = row['Plant_Height']
                i.Cultivation_Time_Days = row['Cultivation_Time_Days']
                i.Distance_between_plants_cm = row['Distance_between_plants_cm']
                i.Distance_between_rows_cm = row['Distance_between_rows_cm']
                i.Number_of_plants_per_m2 = row['Number_of_plants_per_m2']
                i.Nutrient_Solution_FlowRate = row['Nutrient_Solution_FlowRate']
                i.Nutrient_Solution_Reservoir_Volume = row['Nutrient_Solution_Reservoir_Volume']
                i.Nutrient_Solution_Replacement_Frequency_Days = row['Nutrient_Solution_Replacement_Frequency_Days']
                i.Mist_Material_Type = row['Mist_Material_Type']
                i.save()
                data_instance = registration.objects.get(client_id=client_id)
                data_instance.amdone = True
                data_instance.status = "Aeromistifier Progress Completed!"
                data_instance.save()
                data1 = req_details.objects.get(client_id=client_id)
                data1.amdone1 = True
                data1.save()
    messages.info(request, f"{client_id} Aeromistifier Processed Successfully!")
    return render(request, 'aero/process data/process_view.html', {'message': 'Results stored successfully!'})


def view_report(request):
    datas=req_details.objects.filter(amdone1=True)
    return render(request,'aero/view_report/report.html',{'datas':datas})

