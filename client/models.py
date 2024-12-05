from django.db import models

# Create your models here.
class registration(models.Model):
    client_id = models.CharField(unique=True, null=True, max_length=20)
    fullname= models.CharField(max_length=200)
    email= models.EmailField(null=True,unique=True)
    address = models.CharField(max_length=200)
    phone=models.CharField(max_length=10)
    status = models.CharField(default="Pending", max_length=100)
    order_id = models.CharField(unique=True, null=True, max_length=20)
    approve = models.BooleanField(null=True, default=False)
    reject = models.BooleanField(null=True, default=False)
    password = models.PositiveBigIntegerField(null=True)
    login = models.BooleanField(null=True, default=False)
    logout = models.BooleanField(null=True, default=False)

    amdone = models.BooleanField(default=False, null=True)
    cdone = models.BooleanField(default=False, null=True)
    sdone= models.BooleanField(default=False, null=True)
    sysdone= models.BooleanField(default=False, null=True)

    amount = models.CharField(null=True, max_length=10)

    final = models.BooleanField(default=False, null=True)
    pay = models.BooleanField(default=False, null=True)
    end=models.BooleanField(default=True, null=True)
    p=models.BooleanField(default=False, null=True)

    report=models.BooleanField(default=False, null=True)

    # Final Report
    final_report = models.FileField(upload_to='Final_Report/', null=True)


class req_details(models.Model):
    client_id=models.CharField(unique=True,null=True,max_length=20)
    Plant_Type=models.CharField(unique=True,null=True,max_length=30)

    #AeroMistifier
    Nutrient_Solution_Temperature = models.IntegerField(null=True)
    Nutrient_Solution_pH = models.FloatField(null=True)
    Nutrient_Solution_Electrical_Conductivity = models.FloatField(null=True)
    Dissolved_Oxygen = models.FloatField(null=True)
    Air_Temperature = models.FloatField(null=True)
    Air_Humidity = models.FloatField(null=True)
    Light_Intensity = models.FloatField(null=True)
    CO2_Concentration = models.FloatField(null=True)
    Plant_Height = models.FloatField(null=True)
    Plant_Weight = models.FloatField(null=True)
    Cultivation_Time_Days = models.CharField(max_length=20, null=True)
    Distance_between_plants_cm = models.FloatField(null=True)
    Distance_between_rows_cm = models.FloatField(null=True)
    Number_of_plants_per_m2 = models.FloatField(null=True)
    Nutrient_Solution_FlowRate = models.FloatField(null=True)
    Nutrient_Solution_Reservoir_Volume = models.FloatField(null=True)
    Nutrient_Solution_Replacement_Frequency_Days = models.FloatField(null=True)
    Mist_Material_Type = models.CharField(max_length=20, null=True)

    amdone1= models.BooleanField(default=False, null=True)

    #Aero Nuterients
    a_Nitrogen = models.FloatField(null=True)
    a_Phosphorus = models.FloatField(null=True)
    a_Potassium = models.FloatField(null=True)
    a_Calcium = models.FloatField(null=True)
    a_Magnesium = models.FloatField(null=True)
    a_Sulfur = models.FloatField(null=True)
    a_Nutrition_Value = models.FloatField(null=True)

    #Soil Nuterients
    s_Nitrogen = models.FloatField(null=True)
    s_Phosphorus = models.FloatField(null=True)
    s_Potassium = models.FloatField(null=True)
    s_Calcium = models.FloatField(null=True)
    s_Magnesium = models.FloatField(null=True)
    s_Sulfur = models.FloatField(null=True)
    s_Nutrition_Value = models.FloatField(null=True)

    result = models.CharField(max_length=20, null=True)

    sdone2= models.BooleanField(default=False, null=True)

    #System Care Hub
    Monitor_pH_and_EC = models.CharField(max_length=250, null=True)
    Use_high_quality_nutrient_solution = models.CharField(max_length=250, null=True)
    Clean_nutrient_reservoir_and_misters = models.CharField(max_length=250, null=True)
    Avoid_overwatering = models.CharField(max_length=250, null=True)
    Use_drip_irrigation_system = models.CharField(max_length=250, null=True)
    Flush_nutrient_reservoir_and_misters = models.CharField(max_length=250, null=True)
    Test_nutrient_levels_regularly = models.CharField(max_length=250, null=True)
    Monitor_plants_for_signs_of_nutrient_toxicity = models.CharField(max_length=250, null=True)
    Replace_nutrient_solution = models.CharField(max_length=250, null=True)
    Increase_nutrient_concentration = models.CharField(max_length=250, null=True)
    Add_more_macronutrients = models.CharField(max_length=250, null=True)
    Monitor_plant_growth_and_adjust_nutrient_solution_as_needed = models.CharField(max_length=250, null=True)
    Give_foliar_spray_of_nutrients = models.CharField(max_length=250, null=True)

    sysdone3 = models.BooleanField(default=False, null=True)

    #Final Report
    final_report = models.FileField(upload_to='Final_Report/', null=True)

    report1 = models.BooleanField(default=False, null=True)


class payment(models.Model):
    client_id = models.CharField(unique=True,null=True,max_length=20)
    order_id = models.CharField(unique=True, null=True, max_length=20)
    amount = models.CharField(null=True, max_length=10)
    name=models.CharField(null=True,max_length=40)
    acc=models.CharField(null=True,max_length=40)
    exp=models.CharField(null=True, max_length=10)
    cvv=models.IntegerField(null=True)


