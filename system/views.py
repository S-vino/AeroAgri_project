from django.contrib import messages
from django.shortcuts import redirect
from aero.models import employee
from client.models import registration, req_details
from django.shortcuts import render




def systemregister(request):
    if request.method == 'POST':
        empname = request.POST['empname']
        empemail = request.POST['empemail']
        empaddress = request.POST['empaddress']
        empphone = request.POST['empphone']
        empdepartment = request.POST['empdepartment']
        employee(empname=empname, empemail=empemail, empaddress=empaddress, empphone=empphone,empdepartment=empdepartment).save()
        messages.info(request, "SystemCare Hub details registered successfully.Kindly Check Email for further Progress.")
        return render(request, 'system/system_login.html')
    return render(request, 'system/system_reg.html')

def systemlogin(request):
    if request.method == 'POST':
        empemail = request.POST.get('empemail')
        emppassword = request.POST.get('emppassword')

        try:
            emp = employee.objects.get(empemail=empemail, emppassword=emppassword)
            if emp.admit:
                messages.info(request, "SystemCare Hub Login Successful")
                request.session['user_id'] = emp.empid
                print(request.session['user_id'])
                emp.save()
                return redirect('/system_home/')
            else:
                messages.info(request, "You need management approval to access")
                return render(request, 'system/system_login.html')
        except employee.DoesNotExist:
            messages.info(request, "Invalid Email or Password")

    return render(request, 'system/system_login.html')

def system_logout(request):
    if 'user_id' in request.session:
        request.session.pop('user_id',None)
        messages.info(request,'Logout successful')
        return redirect('/system_logout/')
    else:
        messages.info(request, 'Logout successful')
        return redirect('/')

def system_home(request):
    return render(request,'system/system_home.html')


def soil_report_data(request):
    datas = req_details.objects.all()
    return render(request,'system/soil_report/soil_report.html',{'datas':datas})


def process_sch(request):
    datas = req_details.objects.all()
    return render(request,'system/process_sch/process_sch.html',{'datas':datas})



def syscare_result(request, client_id):
    data = registration.objects.get(client_id=client_id)
    data_objects = req_details.objects.get(client_id=client_id)
    d = data_objects.result

    if d == "High":
        Monitor_pH_and_EC = "Yes, Monitor pH and EC regularly"
        Use_high_quality_nutrient_solution = "Yes, specifically designed for aeroponics"
        Clean_nutrient_reservoir_and_misters = "Yes, regularly to prevent the growth of algae and bacteria"
        Avoid_overwatering = "Yes, can leach nutrients out of the root zone"
        Use_drip_irrigation_system = "Yes, delivers the nutrient solution directly to the roots of the plants"
        Flush_nutrient_reservoir_and_misters = "Yes, regularly to remove any accumulated nutrients or toxins"
        Test_nutrient_levels_regularly = "Yes, to ensure that the plants are getting the nutrients they need"
        Monitor_plants_for_signs_of_nutrient_toxicity = "Yes, such as leaf burn or nutrient lockout"
        Replace_nutrient_solution = "Maybe, if the nutrient levels are too high for the plants to tolerate"
        Increase_nutrient_concentration = "No, not necessary"
        Add_more_macronutrients = "No, not necessary"
        Monitor_plant_growth_and_adjust_nutrient_solution_as_needed = "No, not necessary"
        Give_foliar_spray_of_nutrients = "No, not necessary"

    elif d == "Equal":
        Monitor_pH_and_EC = "Yes, Monitor pH and EC regularly."
        Use_high_quality_nutrient_solution = "No"
        Clean_nutrient_reservoir_and_misters = "Yes, regularly to prevent the growth of algae and bacteria"
        Avoid_overwatering = "No, can leach nutrients out of the root zone"
        Use_drip_irrigation_system = "Yes, delivers the nutrient solution directly to the roots of the plants"
        Flush_nutrient_reservoir_and_misters = "No, not necessary"
        Test_nutrient_levels_regularly = "Yes, to ensure that the plants are getting the nutrients they need"
        Monitor_plants_for_signs_of_nutrient_toxicity = "Yes,Monitor plants for signs of nutrient toxicity"
        Replace_nutrient_solution = "Yes, Replace the nutrient with suitable nutrient"
        Increase_nutrient_concentration = "Yes, must increase the nutrient concentration"
        Add_more_macronutrients = "Yes"
        Monitor_plant_growth_and_adjust_nutrient_solution_as_needed = "Yes, It's important to moniter the plant growth and adjust the nutrient solution"
        Give_foliar_spray_of_nutrients = "No, not necessary"

    else:
        Monitor_pH_and_EC = "Yes, Monitor pH and EC regularly."
        Use_high_quality_nutrient_solution = "No"
        Clean_nutrient_reservoir_and_misters = "Yes, regularly to remove any accumulated nutrients or toxins"
        Avoid_overwatering = "No"
        Use_drip_irrigation_system = "Yes, delivers the nutrient solution directly to the roots of the plants"
        Flush_nutrient_reservoir_and_misters = "Yes, regularly to remove any accumulated nutrients or toxins"
        Test_nutrient_levels_regularly = "Yes, to ensure that the plants are getting the nutrients they need"
        Monitor_plants_for_signs_of_nutrient_toxicity = "No"
        Replace_nutrient_solution = "Yes, if the nutrient levels are too low for the plants to tolerate"
        Increase_nutrient_concentration = "Yes, to increase the nutrient levels in the nutrient solution"
        Add_more_macronutrients = "Yes, to increase the nutrient levels in the nutrient solution"
        Monitor_plant_growth_and_adjust_nutrient_solution_as_needed = "Yes, to monitor the growth of the plants and adjust the nutrient solution as needed"
        Give_foliar_spray_of_nutrients = "Yes, if the nutrient levels are too low for the plants to tolerate"

    data_objects.Monitor_pH_and_EC = Monitor_pH_and_EC
    data_objects.Use_high_quality_nutrient_solution = Use_high_quality_nutrient_solution
    data_objects.Clean_nutrient_reservoir_and_misters = Clean_nutrient_reservoir_and_misters
    data_objects.Avoid_overwatering = Avoid_overwatering
    data_objects.Use_drip_irrigation_system = Use_drip_irrigation_system
    data_objects.Flush_nutrient_reservoir_and_misters = Flush_nutrient_reservoir_and_misters
    data_objects.Test_nutrient_levels_regularly = Test_nutrient_levels_regularly
    data_objects.Monitor_plants_for_signs_of_nutrient_toxicity = Monitor_plants_for_signs_of_nutrient_toxicity
    data_objects.Replace_nutrient_solution = Replace_nutrient_solution
    data_objects.Increase_nutrient_concentration = Increase_nutrient_concentration
    data_objects.Add_more_macronutrients = Add_more_macronutrients
    data_objects.Monitor_plant_growth_and_adjust_nutrient_solution_as_needed = Monitor_plant_growth_and_adjust_nutrient_solution_as_needed
    data_objects.Give_foliar_spray_of_nutrients = Give_foliar_spray_of_nutrients
    data_objects.save()

    data.sysdone = True
    data.final = True
    data.end = False
    data.status="Waiting for Authorization"
    data_objects.sysdone3=True
    data_objects.save()
    data.save()

    messages.info(request, f"SystemCare Hub Result Stored Successfully for {data.client_id}")
    return redirect("/system_home/")

def sys_report(request):
    datas = req_details.objects.filter(sysdone3=True)
    return render(request,'system/system_report/sys_report.html',{'datas':datas})