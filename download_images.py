import os
import pandas as pd
import requests
from tqdm import tqdm

# Paths
csv_file = r"C:\Users\Jatin puraswani\Downloads\FactBot\data\ifnd_imageonly.csv"
output_dir = "data/images"
os.makedirs(output_dir, exist_ok=True)

# Load dataset with encoding fix
df = pd.read_csv(csv_file, encoding='ISO-8859-1')  # or encoding='utf-8', errors='ignore'

local_paths = []
for i, row in tqdm(df.iterrows(), total=len(df), desc="Downloading images"):
    url = row["Image"]
    label = row["Label"]

    try:
        filename = f"{i}_{os.path.basename(url.split('?')[0])}"
        filepath = os.path.join(output_dir, filename)

        if not os.path.exists(filepath):
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                with open(filepath, "wb") as f:
                    f.write(r.content)

        local_paths.append(filepath)

    except Exception as e:
        print(f"Failed to download {url}: {e}")
        local_paths.append(None)

df["Image"] = local_paths
df = df.dropna()
df.to_csv("data/ifnd_imageonly_local.csv", index=False)
print("✅ Images downloaded and CSV updated!")
