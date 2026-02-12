import pandas as pd

# Display full table properly
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)

print("Loading dataset...\n")

# Load dataset
df = pd.read_csv("raw_customer_data.csv")

# ================= BEFORE CLEANING =================
print("===== BEFORE CLEANING (First 10 Rows) =====\n")
print(df.head(10).to_string())

# Check missing values
print("\n===== MISSING VALUES COUNT =====\n")
print(df.isnull().sum())

# Store original shape
original_shape = df.shape

# ================= CLEANING PROCESS =================

# Remove duplicates
df = df.drop_duplicates()

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Fill missing values
for col in df.columns:
    if df[col].dtype == "int64" or df[col].dtype == "float64":
        df[col] = df[col].fillna(df[col].median())
    else:
        df[col] = df[col].fillna(df[col].mode()[0])

# Clean text columns
for col in df.select_dtypes(include=["object", "string"]).columns:
    df[col] = df[col].str.strip().str.title()

# Standardize Gender
df["gender"] = df["gender"].replace({
    "M": "Male",
    "F": "Female"
})

# Standardize Country
df["country"] = df["country"].replace({
    "Usa": "USA",
    "Uk": "UK"
})

# Convert Join Date to datetime
df["join_date"] = pd.to_datetime(df["join_date"], format="mixed", dayfirst=True)



# ================= AFTER CLEANING =================

print("\n===== AFTER CLEANING (First 10 Rows) =====\n")
print(df.head(10).to_string())

# Show rows removed
print("\n===== DATASET SHAPE COMPARISON =====")
print("Before Cleaning:", original_shape)
print("After Cleaning :", df.shape)

# Save cleaned dataset
df.to_csv("cleaned_customer_data.csv", index=False)

print("\nCleaning complete ✅")
print("File saved as: cleaned_customer_data.csv")
