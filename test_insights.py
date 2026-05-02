import json
import re

def get_state_insights(ipynb_path):
    with open(ipynb_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    insights = []
    for cell in data.get('cells', []):
        if cell.get('cell_type') == 'markdown':
            source = "".join(cell.get('source', []))
            lines = source.split('\n')
            for i, line in enumerate(lines):
                if 'Insight' in line:
                    text = line.strip()
                    # If the line is just "Insight 1:" or similar, grab the next line
                    if len(text) < 15 and i + 1 < len(lines):
                        text += " " + lines[i+1].strip()
                    # Clean up
                    text = re.sub(r'#+\s*', '', text)
                    if len(text) > 20:
                        insights.append(text)
                        
    # Ensure exactly 25 insights if possible, or all of them.
    # Now map to states
    states_mapping = {
        'Andaman & Nicobar': 'Andaman & Nicobar Island',
        'Andhra Pradesh': 'Andhra Pradesh',
        'Arunachal Pradesh': 'Arunachal Pradesh',
        'Assam': 'Assam',
        'Bihar': 'Bihar',
        'Chandigarh': 'Chandigarh',
        'Chhattisgarh': 'Chhattisgarh',
        'Dadra and Nagar Haveli and Daman and Diu': 'Dadra and Nagar Haveli and Daman and Diu',
        'Delhi': 'NCT of Delhi',
        'Goa': 'Goa',
        'Gujarat': 'Gujarat',
        'Haryana': 'Haryana',
        'Himachal Pradesh': 'Himachal Pradesh',
        'Jammu & Kashmir': 'Jammu & Kashmir',
        'Jharkhand': 'Jharkhand',
        'Karnataka': 'Karnataka',
        'Kerala': 'Kerala',
        'Ladakh': 'Ladakh',
        'Lakshadweep': 'Lakshadweep',
        'Madhya Pradesh': 'Madhya Pradesh',
        'Maharashtra': 'Maharashtra',
        'Manipur': 'Manipur',
        'Meghalaya': 'Meghalaya',
        'Mizoram': 'Mizoram',
        'Nagaland': 'Nagaland',
        'Odisha': 'Odisha',
        'Puducherry': 'Puducherry',
        'Punjab': 'Punjab',
        'Rajasthan': 'Rajasthan',
        'Sikkim': 'Sikkim',
        'Tamil Nadu': 'Tamil Nadu',
        'Telangana': 'Telangana',
        'Tripura': 'Tripura',
        'Uttar Pradesh': 'Uttar Pradesh',
        'Uttarakhand': 'Uttarakhand',
        'West Bengal': 'West Bengal'
    }
    
    # We will return the insights list and state mapping
    return insights
