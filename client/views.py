import PyPDF2
from django.contrib import messages
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
import random
from client.models import registration, payment, req_details


def index(request):
    return render(request,'index.html')

def Clientlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            client = registration.objects.get(email=email, password=password)
            if client.approve:
                messages.info(request, f"{client.client_id} Login Successful")
                request.session['user_id'] = client.client_id
                print( request.session['user_id'])
                client.login = True
                client.logout = False
                client.cdone = True
                client.save()
                return redirect("/client_home/")
            else:
                messages.info(request, "You need management approval to access")
                return render(request, 'client/client_login.html')
        except registration.DoesNotExist:
            messages.info(request, "Invalid Email or Password")
    return render(request, 'client/client_login.html')

def register(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        email=request.POST['email']
        address = request.POST['address']
        phone = request.POST['phone']
        registration(fullname=fullname,email=email,address=address,phone=phone).save()
        messages.info(request, f"{fullname} details registered successfully. Kindly Check {email}.")
        return render(request, 'client/client_login.html')
    return render(request,'client/client_reg.html')



def client_logout(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        try:
            client = registration.objects.get(client_id=user_id)
            client.logout = True
            client.login = False
            client.save()
            del request.session['user_id']
            messages.success(request, f'{client.client_id} Logout successful')
            return redirect('/')
        except registration.DoesNotExist:
            messages.error(request, 'User not found')

        request.session.pop('user_id', None)
    else:
        c = registration.objects.all()
        messages.info(request, f'Logout successful')

    return redirect('/')

def client_home(request):
    return render(request,'client/client_home.html')

def client_upload(request):
    try:
        data = registration.objects.get(login=True)
        client_id = data.client_id
        crp_data = req_details.objects.get(client_id=client_id)
        messages.info(request, "Requirements already uploaded")
        return redirect("/client_home/")
    except:
        data = registration.objects.get(login=True)
        data1 = data.client_id
        client_id = data1
        if request.method == "POST":
            client_id = data1
            Plant_Type = request.POST['Plant_Type']

            req_details(
                client_id=client_id,
                Plant_Type=Plant_Type,
            ).save()
            p = random.randint(10000, 50000)
            data.order_id = f"ORD-{p}"
            data.save()

            messages.info(request, f"{client_id} Requirement Uploaded successfully..!")
            return redirect(request, '/product_status/')
        return render(request, 'client/upload_datasource.html', {'client_id': client_id})


def product_status(request):
    datas = registration.objects.get(login=True)
    s=datas.final
    return render(request,'client/product_status.html', {"datas": datas, 's':s})

def status(request):
    return render(request,'client/reports/status.html')

def id(request):
    client_id = None
    order_id = None
    amount = None
    try:

        client = registration.objects.get(login=True)
        client_id = client.client_id
        order_id = client.order_id
        amount = client.amount
        data1=client.pay

    except registration.DoesNotExist:
        pass

    return render(request, 'client/payment.html', {'client_id': client_id, 'order_id': order_id,'amount':amount,'data1':data1})



def process_payment(request,client_id):
    data = registration.objects.get(client_id=client_id,login=True)
    data1 = data.client_id
    data2 = data.order_id
    data3 = data.amount

    if request.method == 'POST':
        client_id = data1
        order_id = data2
        amount = data3
        name = request.POST['name']
        acc = request.POST['acc']
        exp = request.POST['exp']
        cvv = request.POST['cvv']

        payment_instance = payment(
            client_id=client_id,
            order_id=order_id,
            amount=amount,
            name=name,
            acc=acc,
            exp=exp,
            cvv=cvv
        )
        payment_instance.save()

        a = registration.objects.get(client_id=client_id)
        a.pay = True
        a.p=True
        a.final = False
        a.save()
        messages.info(request, "Payment Successful")
        return render(request, 'client/payment.html',{'client_id':client_id})

    return render(request, 'client/payment.html')

def client(request):
    data = registration.objects.filter(login=True, pay=True)
    return render(request,'client/reports/client_reg.html', {"data": data})


from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io

def final_report(request, client_id):
    data = req_details.objects.get(client_id=client_id)
    data1 = registration.objects.get(client_id=client_id)
    title = "AEROPONICS CROP GROWTH OPTIMIZATION REPORT"
    list_data = [

        "********************************************************************************************************************",
        f"C.ID: {data.client_id}",
        f"Plant Type: {data.Plant_Type}",
        "*************************************************************************",
        "AEROMISTIFIER",
        "*************************************************************************",
        f"Nutrient Solution Temperature: {data.Nutrient_Solution_Temperature}",
        f"Nutrient Solution PH Rate: {data.Nutrient_Solution_pH}",
        f"Nutrient_Solution_Electrical_Conductivity: {data.Nutrient_Solution_Electrical_Conductivity}",
        f"Dissolved_Oxygen: {data.Dissolved_Oxygen}",
        f"Air_Temperature: {data.Air_Temperature}",
        f"Air_Humidity: {data.Air_Humidity}",
        f"Light_Intensity: {data.Light_Intensity}",
        f"CO2_Concentration: {data.CO2_Concentration}",
        f"Plant_Height: {data.Plant_Height}",
        f"Plant_Weight: {data.Plant_Weight}",
        f"Cultivation_Time_Days: {data.Cultivation_Time_Days}",
        f"Distance_between_plants_cm: {data.Distance_between_plants_cm}",
        f"Distance_between_rows_cm: {data.Distance_between_rows_cm}",
        f"Number_of_plants_per_m2: {data.Number_of_plants_per_m2}",
        f"Nutrient_Solution_FlowRate: {data.Nutrient_Solution_FlowRate}",
        f"Nutrient_Solution_Reservoir_Volume: {data.Nutrient_Solution_Reservoir_Volume}",
        f"Nutrient_Solution_Replacement_Frequency_Days: {data.Nutrient_Solution_Replacement_Frequency_Days}",
        f"Mist_Material_Type: {data.Mist_Material_Type}",

        "*************************************************************************",
        "SOILPROFILER: AEROPONIC METHOD",
        "*************************************************************************",
        f"Nitrogen: {data.a_Nitrogen}",
        f"Phosphorus: {data.a_Phosphorus}",
        f"Potassium: {data.a_Potassium}",
        f"Calcium: {data.a_Calcium}",
        f"Magnesium: {data.a_Magnesium}",
        f"Sulfur: {data.a_Sulfur}",
        f"Nutrition_Value: {data.a_Nutrition_Value}",
        "\n",

        "*************************************************************************",
        "SOILPROFILER: TRADITIONAL METHOD",
        "*************************************************************************",
        f"Nitrogen: {data.s_Nitrogen}",
        f"Phosphorus: {data.s_Phosphorus}",
        f"Potassium: {data.s_Potassium}",
        f"Calcium: {data.s_Calcium}",
        f"Magnesium: {data.s_Magnesium}",
        f"Sulfur: {data.s_Sulfur}",
        f"Nutrition_Value: {data.s_Nutrition_Value}",
        "\n",

        "*************************************************************************",
        "SOILPROFILER: RESULT",
        "*************************************************************************",
        f"Result: {data.result}",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",



        "*************************************************************************",
        "SYSTEMCARE HUB",
        "*************************************************************************",
        f"Monitor pH and EC: {data.Monitor_pH_and_EC}",
        f"Use High quality nutrient solution: {data.Use_high_quality_nutrient_solution}",
        f"Clean nutrient reservoir and misters: {data.Clean_nutrient_reservoir_and_misters}",
        f"Avoid Overwatering: {data.Avoid_overwatering}",
        f"Use drip irrigation System: {data.Use_drip_irrigation_system}",
        f"Flush Nutrient reservoir and Misters: {data.Flush_nutrient_reservoir_and_misters}",
        f"Test Nutrient levels regularly: {data.Test_nutrient_levels_regularly}",
        f"Monitor Plants for signs of Nutrient Toxicity: {data.Monitor_plants_for_signs_of_nutrient_toxicity}",
        f"Replace Nutrient Solution: {data.Replace_nutrient_solution}",
        f"Increase Nutrient Concentration: {data.Increase_nutrient_concentration}",
        f"Add more Macronutrients: {data.Add_more_macronutrients}",
        f"Monitor plant growth and adjust nutrient solution: {data.Monitor_plant_growth_and_adjust_nutrient_solution_as_needed}",
        f"Give foliar spray of Nutrients: {data.Give_foliar_spray_of_nutrients}",
    ]

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='AEROPONICS CROP GROWTH OPTIMIZATION - REPORT', fontName='Helvetica-Bold', fontSize=16, textColor=colors.black, spaceBefore=20, spaceAfter=10, underline=True))

    pdf_buffer = io.BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72, pagesize=letter)
    story = []

    story.append(Paragraph(title, styles['Title']))

    for item in list_data:
        story.append(Paragraph(item, styles['Normal']))
        story.append(Spacer(1, 12))

    pdf.build(story)
    pdf_data = pdf_buffer.getvalue()
    pdf_buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{title}_{data.client_id}.pdf"'
    response.write(pdf_data)

    data.final_report.save(f"{title}_{data.client_id}.pdf", ContentFile(pdf_data))
    data.report1 = True
    data.save()
    data1.final_report.save(f"{title}_{data.client_id}.pdf", ContentFile(pdf_data))
    data1.report = True
    data1.p = False
    data1.save()


    messages.info(request,f"Aeroponics Crop Growth Optimization Final Report Generated Successfully for {data.client_id}")
    return redirect('/client_home/')


import os
import pyttsx3
import PyPDF2
from django.shortcuts import redirect
def read(request, client_id):
    try:
        data = req_details.objects.get(client_id=client_id)
        title = "AEROPONICS_CROP_GROWTH_OPTIMIZATION_REPORT"
        file_name = f"{title}_{data.client_id}.pdf"
        file_path = os.path.join(r'C:\aero\aerophonics\media\Final_Report', file_name)
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text_content = ''
            for page_num in range(len(pdf_reader.pages)):
                page_text = pdf_reader.pages[page_num].extract_text()
                text_content += page_text
        speaker = pyttsx3.init()
        speaker.say(text_content)
        speaker.runAndWait()
    except Exception as e:
        print(f"An error occurred: {e}")
    return redirect('/product_status/')

