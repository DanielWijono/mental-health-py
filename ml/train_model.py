import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib

# 1. Load data
df = pd.read_csv("user_scores.csv")

# 2. Encode gender and risk_level into numeric values
df["gender"] = LabelEncoder().fit_transform(df["gender"])  # male=1, female=0
df["risk_level_encoded"] = LabelEncoder().fit_transform(df["risk_level"])  # e.g. Low=1, Critical=0

# 3. Define features and label
X = df[["age", "gender", "phq9_score", "gad7_score"]]
y = df["risk_level_encoded"]

# 4. Split into train/test sets (80/20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 6. Evaluate
y_pred = model.predict(X_test)
print("📊 Classification Report:")
print(classification_report(y_test, y_pred))

# 7. Save the model
joblib.dump(model, "risk_model.pkl")
print("✅ Model saved to risk_model.pkl")
