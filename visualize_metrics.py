import json
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Cyclomatic Complexity (CC) metrics
with open("cc_metrics.json", "r") as f:
    cc_data = json.load(f)

# Load the Maintainability Index (MI) metrics
with open("mi_metrics.json", "r") as f:
    mi_data = json.load(f)

# Load the Halstead metrics
with open("hal_metrics.json", "r") as f:
    hal_data = json.load(f)

# Function to extract relevant data from CC JSON
def extract_cc_data(data):
    functions = []
    complexities = []
    for file_metrics in data.values():
        for function_metric in file_metrics:
            functions.append(function_metric['name'])
            complexities.append(function_metric['complexity'])
    return functions, complexities

# Extract data for CC
functions, complexities = extract_cc_data(cc_data)

# Create a bar plot for Cyclomatic Complexity
plt.figure(figsize=(10, 6))
sns.barplot(x=functions, y=complexities)
plt.title("Cyclomatic Complexity of Functions")
plt.xticks(rotation=90)
plt.ylabel("Complexity")
plt.xlabel("Function")
plt.tight_layout()
plt.show()

# Create a histogram for Maintainability Index
mi_values = [value for value in mi_data.values()]

plt.figure(figsize=(10, 6))
sns.histplot(mi_values, bins=10, kde=True)
plt.title("Maintainability Index Distribution")
plt.xlabel("Maintainability Index")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# Function to extract relevant data from Halstead JSON
def extract_hal_data(data):
    functions = []
    volume = []
    difficulty = []
    effort = []
    for file_metrics in data.values():
        for function_metric in file_metrics:
            functions.append(function_metric['name'])
            volume.append(function_metric['volume'])
            difficulty.append(function_metric['difficulty'])
            effort.append(function_metric['effort'])
    return functions, volume, difficulty, effort

# Extract data for Halstead metrics
functions, volume, difficulty, effort = extract_hal_data(hal_data)

# Create a scatter plot for Halstead metrics (Volume vs. Difficulty)
plt.figure(figsize=(10, 6))
sns.scatterplot(x=volume, y=difficulty, hue=functions, s=100, legend=False)
plt.title("Halstead Metrics: Volume vs. Difficulty")
plt.xlabel("Volume")
plt.ylabel("Difficulty")
plt.tight_layout()
plt.show()

# Create a bar plot for Halstead Effort
plt.figure(figsize=(10, 6))
sns.barplot(x=functions, y=effort)
plt.title("Halstead Effort of Functions")
plt.xticks(rotation=90)
plt.ylabel("Effort")
plt.xlabel("Function")
plt.tight_layout()
plt.show()
