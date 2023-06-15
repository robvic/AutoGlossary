# Import packages
import time
import glob
import re
import pandas as pd
import defGen

# Read file
# Pick the latest version
ORIGINAL_FILE = 'glossary.xlsx'
file_pattern = 'glossary*.csv'
files = glob.glob(file_pattern)
version_max = 0
for file in files:
    name_pattern = 'glossary_(\d*)\.csv'
    matched_name = re.match(name_pattern,file)
    if matched_name:
        version = int(matched_name.group(1))
    else:
        version = 0
    if version >= version_max: version_max = version

if version > 0:
    current_file = f'glossary_{version_max}.xlsx'
else:
    current_file = ORIGINAL_FILE
list = pd.read_excel(current_file).fillna('')

# Limit variable
LIMIT = 1
COUNTER_MAX = 10
counter = 0

# Iterate over values
# Stop whenever limit is reached
# Skips when filled definition is found
for index, row in list.iterrows():
    time.sleep(3)
    # Stop conditions
    counter+=1
    if index == LIMIT: break
    if counter == COUNTER_MAX: break
    if row['Definition'] != "": continue
    # Separate mnemonic/concept/field/subfield
    mnemonic = row['Mnemonic']
    concept = row['Concept']
    field = row['Field']
    subfield = row['Subfield']

    # Call definition-gen
    prompt = f'{mnemonic} {concept} ({field}/{subfield})'
    print(prompt)
    res = defGen.predict_large_language_model(prompt)

    # Fill value
    list.at[index, 'Definition'] = res

# Save copy
# Add new version
file_name = f'glossary_{version_max+1}'
list.to_csv(file_name+'.csv')
list.to_excel(file_name+'.xlsx', index=None)