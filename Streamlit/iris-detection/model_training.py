import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import joblib
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("iris.csv")

# deleting Id
if "Id" in df.columns:
    df = df.drop("Id", axis=1)

# X is the features and y is the target
X = df.drop("Species", axis=1)
y = df["Species"]

# training and testing dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initializing SVM model
model = SVC(kernel='linear',  C=2.0, gamma='scale')  
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Calculate accuracy
acc = accuracy_score(y_test, y_pred)
print(f" Model trained with accuracy: {acc:.2f}")

# Save the model
joblib.dump(model, "iris_model.pkl")
print(" Model saved as iris_model.pkl")
