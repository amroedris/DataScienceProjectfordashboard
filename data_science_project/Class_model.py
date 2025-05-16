import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load Data
url = r"addiction after scaling and imputation.csv"
data = pd.read_csv(url)

# Select features and target
features = [
    'daily_screen_time',
    'app_sessions',
    'social_media_usage',
    'gaming_time',
    'night_usage',
    'stress_level'
]
target = 'addicted'

# Drop missing values
data_clean = data[features + [target]].dropna()

# Define X and y
X = data_clean[features]
y = data_clean[target]

# Normalize Data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Naive Bayes
nb_model = GaussianNB() 
nb_model.fit(X_train, y_train)
y_pred_nb = nb_model.predict(X_test)

# kNN with Hyperparameter Tuning
param_grid = {
    'n_neighbors': list(range(1, 21)),
    'weights': ['uniform', 'distance'],
    'metric': ['euclidean', 'manhattan']
}
grid_knn = GridSearchCV(KNeighborsClassifier(), param_grid, cv=5, scoring='accuracy')
grid_knn.fit(X_train, y_train)

# Best kNN model
print("Best kNN Parameters:", grid_knn.best_params_)
print("Best kNN CV Score:", grid_knn.best_score_)
y_pred_knn = grid_knn.best_estimator_.predict(X_test)

# Evaluation
print("\nNaive Bayes Report")
print("Accuracy:", accuracy_score(y_test, y_pred_nb))
print(classification_report(y_test, y_pred_nb))

print("\nk-Nearest Neighbors Report (Tuned)")
print("Accuracy:", accuracy_score(y_test, y_pred_knn))
print(classification_report(y_test, y_pred_knn))

# Visualization
plt.figure(figsize=(12, 5))

# Naive Bayes Confusion Matrix
plt.subplot(1, 2, 1)
sns.heatmap(confusion_matrix(y_test, y_pred_nb), annot=True, fmt='d', cmap='Blues')
plt.title("Naive Bayes Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

# kNN Confusion Matrix
plt.subplot(1, 2, 2)
sns.heatmap(confusion_matrix(y_test, y_pred_knn), annot=True, fmt='d', cmap='Greens')
plt.title("kNN Confusion Matrix (Tuned)")
plt.xlabel("Predicted")
plt.ylabel("Actual")

# Extra info
print("Original rows:", data.shape[0])
print("After cleaning:", data_clean.shape[0])
print("Test set size:", X_test.shape[0])
print("Test set class distribution:\n", pd.Series(y_test).value_counts())

plt.tight_layout()
plt.show()

