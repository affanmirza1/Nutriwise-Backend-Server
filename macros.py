def calculate_bmr(weight_kg, height_cm, age, gender, activity_level):
    import math
    activity_levels = {'sedentary': 1.2, 'light activity': 1.375, 'moderate activity':1.55, 'very active':1.725}
    
    if gender.lower() == 'male':
        bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
    elif gender.lower() == 'female':
        bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)
    else:
        raise ValueError("Invalid gender")
    bmr = round(bmr * activity_levels[activity_level])
    protein_c = round(bmr*.25)
    carbohydrate_c = round(bmr*.50)
    fat_c = round(bmr*.25)
    protein_g= round(protein_c/4)
    carbohydrate_g = round(carbohydrate_c/4)
    fat_g= round(fat_c/9)
    macros = {"bmr":bmr,
              "protein_c":protein_c,
              "carbohydrate_c":carbohydrate_c,
              "fat_c": fat_c,
              "protein_g":protein_g,
              "carbohydrate_g":carbohydrate_g,
              "fat_g":fat_g}
    return macros