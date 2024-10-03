import pandas as pd
import os

folder_path = '/Users/naveenbighan/Desktop/GOOGLEMAPS/Master'
files = os.listdir(folder_path)

all_data = []

for file in files:
    if file.endswith('.csv'):
        print(f"Processing file: {file}")
        file_path = os.path.join(folder_path, file)
        data = pd.read_csv(file_path)
        all_data.append(data)

master_data = pd.concat(all_data, ignore_index=True)

master_data_cleaned = master_data.drop_duplicates()

# master_data_cleaned.insert(0, 'Company name', 'Microsoft')

if 'Review' in master_data_cleaned.columns:
    master_data_cleaned['Review'] = master_data_cleaned['Review'].str.replace(r'More|\.{3}', '', regex=True)

master_file_path = os.path.join(folder_path, 'Master_file.csv')
master_data_cleaned.to_csv(master_file_path, index=False, encoding='utf-8-sig')

print(f"Master file saved as: {master_file_path}")
print(f"Total records after removing duplicates: {len(master_data_cleaned)}")
