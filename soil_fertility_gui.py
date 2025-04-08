import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from tkinter import *
from tkinter import messagebox
import random

# File path to your dataset
file_path = ("C:\\Users\\bhuva\\Downloads\\dataset1.csv"

)


# Load dataset and prepare the model
def prepare_model():
    # Load the dataset
    dataset = pd.read_csv(file_path)

    # Separate features and target
    X = dataset.drop(columns=["Output"])
    y = dataset["Output"]

    # Feature scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Initialize and train the model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_scaled, y)

    return model, scaler, dataset, X.columns


# Function to predict soil fertility level and recommend crops
def recommend_crops(soil_data):
    # Predict the soil fertility level
    soil_data_scaled = scaler.transform(pd.DataFrame([soil_data], columns=X_columns))
    fertility_level = model.predict(soil_data_scaled)[0]

    # Map fertility level to labels
    fertility_mapping = {0: "Low Fertility", 1: "Medium Fertility", 2: "High Fertility"}
    fertility_label = fertility_mapping.get(fertility_level, "Unknown Fertility Level")

    # Crop recommendations based on fertility level
    crop_recommendations = {
        0: "Low Fertility Crops:\nMillet, Sorghum, Chickpeas, Sesame.",
        1: "Medium Fertility Crops:\nMaize, Wheat, Beans, Sunflower.",
        2: "High Fertility Crops:\nRice, Corn, Tomato, Spinach, Banana.",
    }

    return fertility_label, crop_recommendations.get(
        fertility_level, "No recommendation available"
    )


# Function for manual data entry with GUI
def manual_entry_gui():
    try:
        # Collect input from the user through GUI
        soil_data = []
        for entry in manual_entries:
            value = float(entry.get())
            soil_data.append(value)

        # Check fertility and suggest crops for the manual data
        fertility_label, recommendation = recommend_crops(soil_data)

        # Display results for manual entry
        result_text = (
            f"Fertility Level: {fertility_label}\n\nRecommendation:\n{recommendation}"
        )
        messagebox.showinfo("Soil Fertility and Crop Recommendation", result_text)
    except Exception as e:
        messagebox.showerror("Input Error", f"Invalid input. {str(e)}")


# Function for automated data selection
def auto_recommendation():
    try:
        # Get the number of rows from the user
        num_rows = int(num_rows_entry.get())
        if num_rows <= 0:
            raise ValueError("Number of rows must be positive.")

        # Fetch random rows from the dataset
        selected_rows = dataset.sample(n=num_rows, random_state=42).drop(
            columns=["Output"]
        )
        display_text = selected_rows.to_string(index=False)

        # Display the selected rows in the UI
        auto_values_label.config(text=f"Selected {num_rows} Rows:\n{display_text}")

        # Check fertility and suggest crops for each selected row
        recommendations = []
        for index, row in selected_rows.iterrows():
            soil_data = row.tolist()
            fertility_label, recommendation = recommend_crops(soil_data)
            recommendations.append(
                f"Row {index + 1}:\nFertility Level: {fertility_label}\nRecommendation: {recommendation}\n"
            )

        # Show the fertility and crop recommendations for all rows in a message box
        result_text = "\n".join(recommendations)
        messagebox.showinfo(
            "Soil Fertility and Crop Recommendations for All Rows", result_text
        )

    except Exception as e:
        messagebox.showerror("Input Error", f"Invalid input. {str(e)}")


# Function to ask the user for manual or automated input
def ask_manual_or_automated():
    response = messagebox.askquestion(
        "Input Method", "Do you want to automate the values?", icon="question"
    )
    if response == "yes":
        # Show entry for automated data selection
        auto_frame.pack()
        manual_frame.pack_forget()
    else:
        # Show entry for manual data input
        manual_frame.pack()
        auto_frame.pack_forget()


# Prepare the model, scaler, dataset, and column names
model, scaler, dataset, X_columns = prepare_model()

# Create a simple GUI using Tkinter
root = Tk()
root.title("Soil Fertility Checker and Crop Recommendation")

# Frame for manual entry with GUI input fields
manual_frame = Frame(root)
Label(manual_frame, text="Manual Entry: Enter soil data for each parameter").grid(
    row=0, column=0, columnspan=2, padx=10, pady=5
)
manual_entries = []
for idx, param in enumerate(X_columns):
    Label(manual_frame, text=f"{param}:").grid(
        row=idx + 1, column=0, padx=10, pady=5, sticky=E
    )
    entry = Entry(manual_frame)
    entry.grid(row=idx + 1, column=1, padx=10, pady=5)
    manual_entries.append(entry)

Button(manual_frame, text="Submit Manual Data", command=manual_entry_gui).grid(
    row=len(X_columns) + 1, column=0, columnspan=2, pady=20
)

# Frame for automated entry
auto_frame = Frame(root)
Label(auto_frame, text="Number of Rows for Soil Fertility Check").grid(
    row=0, column=0, padx=10, pady=5
)
num_rows_entry = Entry(auto_frame)
num_rows_entry.grid(row=0, column=1, padx=10, pady=5)
auto_values_label = Label(auto_frame, text="", fg="blue")
auto_values_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
Button(
    auto_frame,
    text="Check Soil Fertility and Get Recommendation",
    command=auto_recommendation,
).grid(row=2, column=0, columnspan=2, pady=20)

# Initial prompt to ask user for input method
ask_manual_or_automated()

# Run the GUI loop
root.mainloop()
