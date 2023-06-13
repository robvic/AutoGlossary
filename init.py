# Import packages
import time
import pandas as pd
import defGen

# Read file
# TODO: list files and pick the latest version
list = pd.read_excel('glossary.xlsx').fillna('')

# Limit variable
LIMIT = 10

# Iterate over values
for index, row in list.iterrows():
    time.sleep(3)
    if index == LIMIT: break
    # Separate mnemonic/concept/field/subfield
    mnemonic = row['Mnemonic']
    concept = row['Concept']
    field = row['Field']
    subfield = row['Subfield']

    # Call definition-gen
    # TODO: skip for definitions already registered
    prompt = f'{mnemonic} {concept} ({field}/{subfield})'
    print(prompt)
    res = defGen.predict_large_language_model(prompt)

    # Fill value
    list.at[index, 'Definition'] = res

# Save copy
# TODO: generate new version
list.to_csv('glossary-filled.csv')