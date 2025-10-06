import os
import re
import pandas as pd
import numpy as np

# --- 1. Folder path ---
folder = "/Users/jolinluk/Downloads/lips_images"
records = []

# --- 2. List of known ethnicities ---
ethnicities = ["Chinese", "MiddleEastern", "Unknown"]

# --- 3. Process each file in the folder ---
for fname in os.listdir(folder):
    if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue

    # --- 3a. Extract numeric value (hgb) ---
    hgb_match = re.search(r'(\d+(?:\.\d+)?)gdl', fname, flags=re.IGNORECASE)
    hgb = float(hgb_match.group(1)) if hgb_match else np.nan

    # --- 3b. Extract ethnicity dynamically ---
    ethnicity_found = "Unknown" 
    for eth in ethnicities:
        # Use raw string for regex
        if eth == "MiddleEastern":
            pattern = r"Middle[\s_\-]*Eastern"
        if eth == "Chinese":
            pattern = r"Chinese"
        else:
            pattern = fr"{eth}"
        if re.search(pattern, fname, re.IGNORECASE):
            ethnicity_found = eth
            break

    # --- 3c. Append record ---
    records.append({
        "image_id": fname,
        "hgb": hgb,
        "ethnicity": ethnicity_found
    })

# --- 4. Save to CSV ---
df = pd.DataFrame(records)
os.makedirs("data/processed", exist_ok=True)
df.to_csv("data/processed/labels_extracted.csv", index=False)

# --- 5. Optional: preview ---
print(df.head(40))