import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("datachurn.csv")

print(df.head())
print(df.info())

# -----------------------------
# Data Cleaning
# -----------------------------
# Replace empty values
df.replace(" ", np.nan, inplace=True)
df.dropna(inplace=True)

# Convert target variable
df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

# Encode categorical variables
categorical_cols = df.select_dtypes(include=["object"]).columns

le = LabelEncoder()
for col in categorical_cols:
    df[col] = le.fit_transform(df[col])

# -----------------------------
# Exploratory Data Analysis
# -----------------------------
churn_rate = df["Churn"].mean()
print(f"Churn Rate: {churn_rate:.2%}")

plt.figure()
df["Churn"].value_counts().plot(kind="bar")
plt.title("Churn Distribution")
plt.xlabel("Churn")
plt.ylabel("Count")
plt.show()

plt.figure()
plt.scatter(df["MonthlyCharges"], df["Churn"])
plt.title("Monthly Charges vs Churn")
plt.xlabel("Monthly Charges")
plt.ylabel("Churn")
plt.show()

# -----------------------------
# Modeling
# -----------------------------
X = df.drop("Churn", axis=1)
y = df["Churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", accuracy)

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
