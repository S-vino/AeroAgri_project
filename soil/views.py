from django.contrib import messages
from django.shortcuts import render, redirect
import pandas as pd
from aero.models import employee
from client.models import registration, req_details

from pandas.errors import EmptyDataError, ParserError

def soilregister(request):
    if request.method == 'POST':
        empname = request.POST['empname']
        empemail = request.POST['empemail']
        empaddress = request.POST['empaddress']
        empphone = request.POST['empphone']
        empdepartment = request.POST['empdepartment']
        employee(empname=empname, empemail=empemail, empaddress=empaddress, empphone=empphone,empdepartment=empdepartment).save()
        messages.info(request, "SoilProfiler details registered successfully. Kindly Check Email for further Progress.")
        return render(request, 'soil/soil_login.html')
    return render(request, 'soil/soil_reg.html')

def soillogin(request):
    if request.method == 'POST':
        empemail = request.POST.get('empemail')
        emppassword = request.POST.get('emppassword')

        try:
            emp = employee.objects.get(empemail=empemail, emppassword=emppassword)
            if emp.accept:
                messages.info(request, "SoilProfiler Login Successful")
                request.session['user_id'] = emp.empid
                print( request.session['user_id'])
                emp.save()
                return render(request,'soil/soil_home.html')
            else:
                messages.info(request, "You need management approval to access")
                return render(request, 'soil/soil_login.html')
        except employee.DoesNotExist:
            messages.info(request, "Invalid Email or Password")

    return render(request, 'soil/soil_login.html')

def soil_logout(request):
    if 'user_id' in request.session:
        request.session.pop('user_id',None)
        messages.success(request,'Logout successful')
        return redirect('/')
    else:
        messages.success(request, 'Logout successful')
        return redirect('/soil_logout/')

def soil_home(request):
    return render(request,'soil/soil_home.html')

def s_aero_report(request):
    datas = req_details.objects.filter(amdone1=True)
    return render(request, 'soil/aero_report/aero_report.html', {'datas': datas})

def aero_process_data(request):
    datas = req_details.objects.filter(amdone1=True)
    return render(request, 'soil/soil_view/aero_process_data.html', {'datas': datas})



from django.shortcuts import redirect
from django.contrib import messages
from sklearn.model_selection import train_test_split
import lightgbm as lgb
import pandas as pd

def compare_plant_types(request, client_id):
    try:
        # Fetch data for the specific client
        data = req_details.objects.filter(client_id=client_id)

        # Load nutrient data from CSV files
        aeroponics_csv_path = r'C:\aero\aerophonics\Aerophonics Nuterients.csv'
        soil_csv_path = r'C:\aero\aerophonics\Soil Nuterients.csv'
        df_aero = pd.read_csv(aeroponics_csv_path)
        df_soil = pd.read_csv(soil_csv_path)

        # Update Aeroponics nutrient values
        for _, row in df_aero.iterrows():
            for item in data:
                if item.Plant_Type == row['Plant_Type']:
                    item.a_Nitrogen = row['a_Nitrogen']
                    item.a_Phosphorus = row['a_Phosphorus']
                    item.a_Potassium = row['a_Potassium']
                    item.a_Calcium = row['a_Calcium']
                    item.a_Magnesium = row['a_Magnesium']
                    item.a_Sulfur = row['a_Sulfur']
                    item.save()

        # Update Soil nutrient values
        for _, row in df_soil.iterrows():
            for item in data:
                if item.Plant_Type == row['Plant_Type']:
                    item.s_Nitrogen = row['s_Nitrogen']
                    item.s_Phosphorus = row['s_Phosphorus']
                    item.s_Potassium = row['s_Potassium']
                    item.s_Calcium = row['s_Calcium']
                    item.s_Magnesium = row['s_Magnesium']
                    item.s_Sulfur = row['s_Sulfur']
                    item.save()

        # Create feature and label datasets for aeroponics and soil data
        aero_features = df_aero[['a_Nitrogen', 'a_Phosphorus', 'a_Potassium', 'a_Calcium', 'a_Magnesium', 'a_Sulfur']]
        aero_label = df_aero['a_Nutrition_Value']
        soil_features = df_soil[['s_Nitrogen', 's_Phosphorus', 's_Potassium', 's_Calcium', 's_Magnesium', 's_Sulfur']]
        soil_label = df_soil['s_Nutrition_Value']

        # Split the data into training and testing sets
        X_train_aero, X_test_aero, y_train_aero, y_test_aero = train_test_split(aero_features, aero_label, test_size=0.2)
        X_train_soil, X_test_soil, y_train_soil, y_test_soil = train_test_split(soil_features, soil_label, test_size=0.2)

        # Create the LightGBM datasets
        lgb_train_aero = lgb.Dataset(X_train_aero, label=y_train_aero)
        lgb_test_aero = lgb.Dataset(X_test_aero, label=y_test_aero)
        lgb_train_soil = lgb.Dataset(X_train_soil, label=y_train_soil)
        lgb_test_soil = lgb.Dataset(X_test_soil, label=y_test_soil)

        # Set the LightGBM parameters
        params = {
            'boosting_type': 'gbdt',
            'objective': 'regression',
            'metric': 'rmse',
            'num_leaves': 31,
            'learning_rate': 0.05,
            'feature_fraction': 0.9,
            'bagging_fraction': 0.8,
            'bagging_freq': 5,
            'verbose': -1,
            'early_stopping_rounds': 100
        }

        # Train the LightGBM models
        lgb_model_aero = lgb.train(params, lgb_train_aero, num_boost_round=1000, valid_sets=[lgb_train_aero, lgb_test_aero])
        lgb_model_soil = lgb.train(params, lgb_train_soil, num_boost_round=1000, valid_sets=[lgb_train_soil, lgb_test_soil])

        # Predict nutrition values for aeroponics and soil data
        aeroponics_predicted = lgb_model_aero.predict(aero_features)
        aero = int(aeroponics_predicted[0])
        soil_predicted = lgb_model_soil.predict(soil_features)
        soil = int(soil_predicted[0])

        # Update the data objects with the predicted nutrition values
        for item, aero_pred, soil_pred in zip(data, aeroponics_predicted, soil_predicted):
            item.a_Nutrition_Value = aero_pred
            item.s_Nutrition_Value = soil_pred
            item.save()

        # Compare predicted values and update the 'result' field
        for item in data:
            if item.a_Nutrition_Value > item.s_Nutrition_Value:
                item.result = "High"
            elif item.a_Nutrition_Value == item.s_Nutrition_Value:
                item.result = "Equal"
            else:
                item.result = "Low"
            item.save()

        # Mark the process as done in the registration and req_details
        registration.objects.filter(client_id=client_id).update(sdone=True)
        req_details.objects.filter(client_id=client_id).update(sdone2=True)

        # Inform the user and redirect
        messages.info(request, f"{client_id} SoilProfiler Result Stored Successfully.")
        return redirect("/soil_home/")

    except Exception as e:
        # Handle exceptions
        print(f"Error: {e}")
        messages.error(request, f"Error: {e}")
        return redirect("/soil_home/")


def soil_result(request):
    datas = req_details.objects.filter(sdone2=True)
    return render(request,'soil/soil_result/soil_result.html',{'datas':datas})