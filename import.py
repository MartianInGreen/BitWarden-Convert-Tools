import json
from datetime import datetime

def extract_passkeys(input_file):
    # Read the original export
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Filter items with fido2Credentials
    passkey_items = [
        item for item in data['items'] 
        if item.get('login', {}).get('fido2Credentials', [])
    ]
    
    # Create new export structure
    new_export = {
        "encrypted": False,
        "items": passkey_items,
        "folders": data.get('folders', []),
        "collections": data.get('collections', []),
    }
    
    # Generate output filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = f'bitwarden_passkeys_{timestamp}.json'
    
    # Save new export
    with open(output_file, 'w') as f:
        json.dump(new_export, f, indent=2)
    
    return output_file

if __name__ == "__main__":
    input_file = "data.json"
    output_file = extract_passkeys(input_file)
    print(f"Passkeys extracted to: {output_file}")