import numpy as np
import pandas as pd

data = pd.read_excel("results/DryAll_results.xlsx", sheet_name="Sheet1")

#data should have a colmun called "deltaR", we would like to plt.hist of this column

import matplotlib.pyplot as plt

plt.rcParams['font.size'] = 16

plt.xlim(0,1.2)
plt.hist(data["deltaR"], bins=100)
plt.show()

#keep any data that has deltaR < 1.25 
data = data[data["deltaR"] < 1.25]

plt.xlim(0,1.25)

plt.hist(data["deltaR"], bins=100)
plt.show()

#print the min, max, mean and median of deltaR

print("min: ", min(data["deltaR"]))
print("max: ", max(data["deltaR"]))
print("mean: ", np.mean(data["deltaR"]))
print("median: ", np.median(data["deltaR"]))