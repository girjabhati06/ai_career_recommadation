import pandas as pd
import random
import joblib

from sklearn.ensemble import RandomForestClassifier


# Career profiles
career_profiles = {
    "Software Developer":      [5, 4, 4, 3, 5, 5, 4],
    "Data Scientist":          [5, 5, 3, 3, 5, 5, 4],
    "Data Analyst":             [4, 5, 4, 3, 4, 4, 4],
    "Web Developer":            [5, 3, 4, 4, 4, 5, 4],
    "UI/UX Designer":           [2, 2, 5, 5, 4, 3, 5],
    "Cybersecurity Analyst":    [5, 4, 3, 2, 5, 5, 4],
    "Digital Marketer":         [2, 2, 5, 5, 4, 3, 5],
    "Database Administrator":   [4, 5, 3, 2, 4, 5, 3],
    "Cloud Engineer":           [5, 4, 3, 2, 5, 5, 4],
    "AI/ML Engineer":            [5, 5, 3, 3, 5, 5, 5]
}


# Feature names
features = [
    "programming",
    "mathematics",
    "communication",
    "creativity",
    "problem_solving",
    "technology_interest",
    "learning_ability"
]


# Generate training dataset
data = []

for career, profile in career_profiles.items():

    for _ in range(50):

        values = []

        for value in profile:

            # Add small variation to create different student profiles
            new_value = value + random.choice([-1, 0, 0, 0, 1])

            # Keep values between 1 and 5
            new_value = max(1, min(5, new_value))

            values.append(new_value)

        data.append(values + [career])


# Create DataFrame
columns = features + ["career"]

df = pd.DataFrame(data, columns=columns)


# Save dataset
df.to_csv("career_dataset.csv", index=False)


# Separate input and output
X = df[features]
y = df["career"]


# Create AI model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)


# Train model
model.fit(X, y)


# Save trained model
joblib.dump(model, "career_model.pkl")


print("======================================")
print("AI MODEL TRAINED SUCCESSFULLY!")
print("======================================")
print("Training records:", len(df))
print("Number of careers:", len(career_profiles))
print("Dataset saved as: career_dataset.csv")
print("Model saved as: career_model.pkl")
print("======================================")