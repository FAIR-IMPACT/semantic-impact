import requests
import json
from bs4 import BeautifulSoup
import pandas as pd

def data_filter(data, query):
    return data[data['Standard'] == query]

def get_sample_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links on the page
    links = soup.find_all('section')

    for link in links:
        if link.get('id') == 'search':
            table = link.find('table')  
            thead = table.find('thead')
            rows = thead.find_all('tr')
            headers = []
            for row in rows:
                cells = row.find_all('th')
                for cell in cells:
                    if cell:
                        headers.append(cell.text.strip())
            
            tbody = table.find('tbody')
            rows = tbody.find_all('tr')
            rows = rows[1:]  # Skip header row
            data = []
            for row in rows:
                datarow = []
                cells = row.find_all('td')
                for cell in cells:
                    datarow.append(cell.text.strip())
                
                # Ensure each row has the same number of columns as headers
                while len(datarow) < len(headers):
                    datarow.append('')  # Pad with empty strings if needed
                data.append(datarow[:len(headers)])  # Truncate if too many columns
            
            # Create DataFrame with proper column alignment
            df = pd.DataFrame(data, columns=headers)
#            print("DataFrame shape:", df.shape)
#            print("\nFirst few rows:")
            print(df.head())
#            print("\nColumns:", df.columns.tolist())
            return df
    
    return pd.DataFrame()  # Return empty DataFrame if no data found

url = "https://rd-alliance.github.io/Research-Metadata-Schemas-WG/"
data = get_sample_data(url)
data.to_csv('rda_manual_mappings.csv', index=False)
data = data_filter(data, "Dataverse")
print(data['Term'])
data.to_csv('dataverse.csv', index=False)








