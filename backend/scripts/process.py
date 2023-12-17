from tqdm import tqdm
from bs4 import BeautifulSoup
import re

def extract_project_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

        # Extracting the title
        title = soup.find_all('h2')[1].get_text(strip=True) if len(soup.find_all('h2')) > 1 else "Not Available"

        # Function to find the text for given label
        def find_label_text(label):
            label_tag = soup.find('strong', text=lambda t: t and label in t)
            if label_tag and label_tag.parent:
                return label_tag.parent.get_text(strip=True).replace(label, '').strip()
            return "Not Available"

        # Extracting booth ID, year, abstract
        booth_id = find_label_text('Booth Id:')
        year = find_label_text('Year:')
        abstract = find_label_text('Abstract:')

        # Extracting and processing finalist names
        finalist_names_text = find_label_text('Finalist Names:')
        finalist_names = [name+")" for name in finalist_names_text.split(')')]
        if finalist_names[-1] == ")":
            finalist_names = finalist_names[:-1]

        # Extracting award information and splitting into a list
        awards_tag = soup.find('p', style="background-color: lightblue; display: inline-block;")
        awards_won_text = awards_tag.get_text().replace("Awards Won:", "").strip() if awards_tag else ""
        awards_won = awards_won_text.split("  ")
        while '' in awards_won:
            awards_won.remove('')

        return {
            'title': title,
            'booth_id': booth_id,
            'year': year,
            'finalist_names': finalist_names,
            'abstract': abstract,
            "project_id": filepath.replace(".html", "").replace("data/", ""),
            'awards_won': awards_won
        }


import os

filepaths = os.listdir('data')

import pandas as pd
import json

abstracts = []
for filepath in tqdm(filepaths):
    project_data = extract_project_data("data/"+filepath)
    if len(project_data['finalist_names']) == 0:
        raise Exception("No finalist names found for project: "+filepath)
    abstracts.append(project_data)

with open('abstracts.json', 'w') as outfile:
    data = json.dumps(abstracts, indent=4)
    outfile.write(data)