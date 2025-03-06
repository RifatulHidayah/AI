# -*- coding: utf-8 -*-
"""PROGRES TUGAS BESAR.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1R96qmQlYzEj-bjQzUnLkMdUgTXcKz3QM

MEMPELAJARI DATASET
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns

# Memuat data
data = pd.read_csv("/content/drive/MyDrive/Kecerdasan Artificial/Data Set baby nutrition classification.csv")

# Melihat beberapa data awal
data.head()

from google.colab import drive
drive.mount('/content/drive')

#Memastikan data terbaca dengan benar
print('data shape: ', data.shape)

#Memastikan tidak ada data yang kosong
data.info()

#Eksplorasi status gizi
data["STATUS GIZI"].value_counts()

data['JENIS KELAMIN'].value_counts()

sns.histplot(data['UMUR'])

"""EKSPLOR DATA ANALISIS"""

sns.set_theme(style='ticks')
sns.countplot(y='STATUS GIZI', data=data, hue ='STATUS GIZI', palette='flare', legend=False)
plt.ylabel('Status Gizi')
plt.xlabel('Jumlah')
plt.show()

sns.set_theme(style='darkgrid')
sns.countplot(x='JENIS KELAMIN', data=data, hue ='JENIS KELAMIN', palette='rocket', legend=False)
plt.ylabel('Jumlah')
plt.xlabel('Jenis Kelamin')
plt.show()

"""DATA PREPARATION"""

data.head()

#Mengubah tipe data non integer ke integer
from sklearn.preprocessing import LabelEncoder

label_encoder = LabelEncoder()

data['JENIS KELAMIN'] = label_encoder.fit_transform(data['JENIS KELAMIN'])
data['STATUS GIZI'] = label_encoder.fit_transform(data['STATUS GIZI'])

data.head()

for col in data.columns:
    if data[col].dtype == 'object':  # Check if the column is of object type (likely string)
        data[col] = data[col].str.replace(',', '.', regex=False).astype(float)
    else:
        data[col] = pd.to_numeric(data[col], errors='coerce') # Keep the column as is if already numeric

# Hapus kolom 'NAMA BALITA'
data = data.drop(columns=['NAMA BALITA'])

data.head()

for col in data.columns:
    if data[col].dtype == 'object':  # Hanya kolom tipe string
        data[col] = pd.to_numeric(data[col].str.replace(',', '.'), errors='coerce')

data.head()

x = data.drop(columns = ['STATUS GIZI'])
y = data['STATUS GIZI']

print('X : ',x.shape)
print('Y : ',y.shape)

x_train,x_test,y_train,y_test = train_test_split(x, y, test_size = 0.2, random_state=42)

print(f'x_train : {x_train.shape}')
print(f'x_test : {x_test.shape}')
print(f'y_train : {y_train.shape}')
print(f'y_test : {y_test.shape}')

"""MODELING"""

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(x_train,y_train)

y_pred = knn.predict(x_test)

# Evaluasi
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Analisis akurasi terbaik
def find_best_k(X_train, y_train, X_test, y_test):
    accuracies = []
    for k in range(1, 21):
        model = KNeighborsClassifier(n_neighbors=k)
        model.fit(X_train, y_train)
        accuracies.append(model.score(X_test, y_test))
    return accuracies

accuracies = find_best_k(x_train, y_train, x_test, y_test)
print("\nAkurasi berdasarkan nilai k:")
for i, acc in enumerate(accuracies, start=1):
    print(f"k={i}: {acc:.2f}")