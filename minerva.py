# -*- coding: utf-8 -*-
"""Minerva.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jPPC9vFovXX_XhmmVQqTyI6OHmmwM9Od
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df=pd.read_csv('./realistic_student_performance (1).csv')
df.head()

df.info()

df.describe()

print("Missing Values:")
print(df.isnull().sum())

print("Duplicate Rows:")
print(df.duplicated().sum())

numerical_columns = df.select_dtypes(include=['float64', 'int']).columns
for column in numerical_columns:
    plt.figure(figsize=(6, 4))
    sns.histplot(df[column], kde=True, bins=30)
    plt.title(f"Distribution of {column}")
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.show()

plt.figure(figsize=(10, 8))
correlation_matrix = df.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title("Correlation Matrix")
plt.show()

for column in numerical_columns:
    plt.figure(figsize=(6, 4))
    sns.boxplot(df[column])
    plt.title(f"Boxplot of {column}")
    plt.xlabel(column)
    plt.show()

target = 'Future Marks'
for column in numerical_columns:
    if column != target:
        plt.figure(figsize=(6, 4))
        sns.scatterplot(x=df[column], y=df[target])
        plt.title(f"Relationship Between {column} and {target}")
        plt.xlabel(column)
        plt.ylabel(target)
        plt.show()

df.duplicated().sum()

df.rename(columns={
    "Activity Hours": "Activity_Hours",
    "Attendance (%)": "Attendance",
    "Stress Level": "Stress_Level",
    "Study Hours": "Study_Hours"
}, inplace=True)

def cap_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df[column] = df[column].clip(lower_bound, upper_bound)

numerical_columns = df.select_dtypes(include=['float64', 'int']).columns
for col in numerical_columns:
    cap_outliers(df, col)

df['Study_to_Activity_Ratio'] = df['Study_Hours'] / (df['Activity_Hours'] + 1e-5)

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

features_to_scale = ['Study_Hours', 'Activity_Hours', 'Attendance', 'Stress_Level', 'Study_to_Activity_Ratio']

df[features_to_scale] = scaler.fit_transform(df[features_to_scale])

print(df[features_to_scale].head())

print(df.head())

from sklearn.model_selection import train_test_split
X=df.drop('Future Marks',axis='columns')
Y=df['Future Marks']
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,random_state=10)

from sklearn.linear_model import LinearRegression
model1=LinearRegression()

model1.fit(X_train,Y_train)

y_lrp=model1.predict(X_test)
y_lrp

Y_test

model1.score(X_test,Y_test)

from sklearn.metrics import mean_squared_error, r2_score
mse = mean_squared_error(Y_test, y_lrp)
r2 = r2_score(Y_test, y_lrp)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

# from sklearn.model_selection import GridSearchCV
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_squared_error, r2_score


# rf_model = RandomForestRegressor(random_state=42)


# param_grid = {
#     'n_estimators': [100, 200, 300],  # Number of trees
#     'max_depth': [None, 10, 20, 30],  # Maximum depth of the trees
#     'min_samples_split': [2, 5, 10],  # Minimum samples required to split a node
#     'min_samples_leaf': [1, 2, 4],    # Minimum samples required to be at a leaf node
#     'max_features': ['auto', 'sqrt', 'log2']  # Number of features to consider at each split
# }

# grid_search = GridSearchCV(estimator=rf_model, param_grid=param_grid, cv=5,
#                            n_jobs=-1, verbose=2, scoring='neg_mean_squared_error')

# grid_search.fit(X_train, Y_train)

# # Get the best parameters and the best estimator
# best_params = grid_search.best_params_
# best_rf_model = grid_search.best_estimator_

# rf_pred = best_rf_model.predict(X_test)

# #To Evaluate the model
# rf_mse = mean_squared_error(Y_test, rf_pred)
# rf_r2 = r2_score(Y_test, rf_pred)

# print(f"Best Parameters: {best_params}")
# print(f"Random Forest MSE after tuning: {rf_mse}")
# print(f"Random Forest R² after tuning: {rf_r2}")

# from sklearn.model_selection import GridSearchCV
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_squared_error, r2_score

# rf_model = RandomForestRegressor(random_state=42)

# #refined parameter grid to avoid overfitting
# param_grid = {
#     'n_estimators': [100, 150, 200],  # Reduced number of trees
#     'max_depth': [10, 15, 20],  # Adjusted depth range
#     'min_samples_split': [2, 5, 10],
#     'min_samples_leaf': [1, 2, 4],
#     'max_features': ['sqrt', 'log2']  # Limited the feature options
# }

# #the GridSearchCV object with 10-fold cross-validation
# grid_search = GridSearchCV(estimator=rf_model, param_grid=param_grid, cv=10,
#                            n_jobs=-1, verbose=2, scoring='neg_mean_squared_error')

# grid_search.fit(X_train, Y_train)
# best_params = grid_search.best_params_
# best_rf_model = grid_search.best_estimator_


# rf_pred = best_rf_model.predict(X_test)

# rf_mse = mean_squared_error(Y_test, rf_pred)
# rf_r2 = r2_score(Y_test, rf_pred)

# print(f"Best Parameters: {best_params}")
# print(f"Random Forest MSE after tuning: {rf_mse}")
# print(f"Random Forest R² after tuning: {rf_r2}")

import joblib

# Assuming your trained Linear Regression model is stored in the variable `linear_model`
joblib.dump(model1, 'linear_model.pkl')

