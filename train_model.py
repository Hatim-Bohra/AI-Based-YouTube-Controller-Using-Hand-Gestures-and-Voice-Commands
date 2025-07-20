import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

X, y = [], []

print("📂 Loading gesture CSV files...")
for file in os.listdir("gesture_data"):
    print(f"🔄 Loading: {file}")
    df = pd.read_csv(f"gesture_data/{file}", header=None)
    
    if df.empty:
        print(f"⚠️ Skipped {file} (empty)")
        continue

    label = file.replace(".csv", "")
    X.extend(df.values)
    y.extend([label] * len(df))

if len(X) == 0:
    print("❌ No data found! Training aborted.")
    exit()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
clf = RandomForestClassifier()
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)

print(f"✅ Model trained with accuracy: {accuracy:.2f}")
joblib.dump(clf, "../gesture_model.pkl")  # Saves one level above
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
model_path = os.path.join(project_root, "gesture_model.pkl")
joblib.dump(clf, model_path)
print(f"💾 Model saved at: {model_path}")

