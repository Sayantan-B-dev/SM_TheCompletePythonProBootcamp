def calculate_bmi(weight_kg: float, height_m: float) -> dict:
    """
    Calculate Body Mass Index (BMI) and return detailed classification.

    Parameters:
    weight_kg (float): Weight in kilograms
    height_m (float): Height in meters

    Returns:
    dict: BMI value, category, and health interpretation
    """

    if weight_kg <= 0 or height_m <= 0:
        raise ValueError("Weight and height must be positive values")

    bmi = weight_kg / (height_m ** 2)

    if bmi < 18.5:
        category = "Underweight"
        interpretation = "You may need to gain weight for optimal health."
    elif 18.5 <= bmi < 25:
        category = "Normal weight"
        interpretation = "You are within the healthy weight range."
    elif 25 <= bmi < 30:
        category = "Overweight"
        interpretation = "You may benefit from weight management."
    else:
        category = "Obese"
        interpretation = "Medical advice is recommended."

    return {
        "BMI": round(bmi, 2),
        "Category": category,
        "Health Interpretation": interpretation
    }


# Example usage
weight = float(input("Enter weight (kg): "))
height = float(input("Enter height (m): "))

result = calculate_bmi(weight, height)

print("\nBMI Report")
print("----------")
print(f"BMI Value : {result['BMI']}")
print(f"Category  : {result['Category']}")
print(f"Note      : {result['Health Interpretation']}")
