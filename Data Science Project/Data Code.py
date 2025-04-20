# Mock project code for Social Media & Smartphones Addiction Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report, confusion_matrix

# Generate mock dataset
np.random.seed(42)
data_size = 200

df = pd.DataFrame({
    'screen_time_hours': np.random.normal(5, 2, data_size).clip(0),
    'social_media_apps': np.random.randint(1, 10, data_size),
    'sleep_hours': np.random.normal(7, 1.5, data_size).clip(4, 10),
    'academic_score': np.random.normal(75, 10, data_size).clip(50, 100),
    'addiction_level': np.random.choice(['Low', 'Medium', 'High'], data_size, p=[0.3, 0.5, 0.2])
})

# Encode addiction_level for classification
df['addiction_label'] = df['addiction_level'].map({'Low': 0, 'Medium': 1, 'High': 2})

# EDA: Save plot
plt.figure(figsize=(8, 5))
sns.boxplot(x='addiction_level', y='screen_time_hours', data=df)
plt.title('Screen Time by Addiction Level')
plt.tight_layout()
plt.savefig('screen_time_by_addiction_level.png')
plt.close()

# Regression: Predict academic_score
X_reg = df[['screen_time_hours', 'social_media_apps', 'sleep_hours']]
y_reg = df['academic_score']
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)

lr = LinearRegression()
lr.fit(X_train_reg, y_train_reg)
y_pred_lr = lr.predict(X_test_reg)

# Regression Metrics
lr_r2 = r2_score(y_test_reg, y_pred_lr)
lr_rmse = np.sqrt(mean_squared_error(y_test_reg, y_pred_lr))

# Classification: Predict addiction_label
X_clf = df[['screen_time_hours', 'social_media_apps', 'sleep_hours']]
y_clf = df['addiction_label']
X_train_clf, X_test_clf, y_train_clf, y_test_clf = train_test_split(X_clf, y_clf, test_size=0.2, random_state=42)

clf = DecisionTreeClassifier(max_depth=5, random_state=42)
clf.fit(X_train_clf, y_train_clf)
y_pred_clf = clf.predict(X_test_clf)

# Classification Metrics
clf_accuracy = accuracy_score(y_test_clf, y_pred_clf)
clf_report = classification_report(y_test_clf, y_pred_clf)
clf_conf_matrix = confusion_matrix(y_test_clf, y_pred_clf)

# Output summary with newlines
print(f"\nLinear Regression R2:\n{lr_r2}")
print(f"\nLinear Regression RMSE:\n{lr_rmse}")
print(f"\nClassification Accuracy:\n{clf_accuracy}")
print(f"\nClassification Report:\n{clf_report}")
print(f"\nConfusion Matrix:\n{clf_conf_matrix.tolist()}")
