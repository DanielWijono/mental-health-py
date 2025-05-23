import pandas as pd
import random

def generate_sample(risk_label):
    """Generate a sample that falls under the specified risk level."""
    while True:
        phq9 = random.randint(0, 27)
        gad7 = random.randint(0, 21)
        predicted = classify_risk(phq9, gad7)
        if predicted == risk_label:
            return phq9, gad7

def classify_risk(phq9, gad7):
    if phq9 >= 20 or gad7 >= 15:
        return "Critical"
    elif phq9 >= 15 or gad7 >= 10:
        return "High"
    elif phq9 >= 5 or gad7 >= 5:
        return "Moderate"
    else:
        return "Low"

names = ["Alice", "Bob", "Carol", "David", "Eve", "Frank", "Grace", "Hank", "Ivy", "Jack"]
genders = ["male", "female"]
data = []

# Equal samples for each class (100 each = total 400)
risk_levels = {
    "Low": 100,
    "Moderate": 100,
    "High": 100,
    "Critical": 100
}

for risk_label, count in risk_levels.items():
    for _ in range(count):
        name = random.choice(names)
        age = random.randint(18, 65)
        gender = random.choice(genders)
        phq9, gad7 = generate_sample(risk_label)

        data.append({
            "name": name,
            "age": age,
            "gender": gender,
            "phq9_score": phq9,
            "gad7_score": gad7,
            "risk_level": risk_label
        })

df = pd.DataFrame(data)
df.to_csv("user_scores.csv", index=False)
print("✅ user_scores.csv created with balanced class samples (100 each).")
