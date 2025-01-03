import json
from datetime import datetime

def convert_proton_to_bitwarden(input_file):
    # Load JSON
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    stats = {'vaults': 0, 'items': 0, 'passkeys': 0}
    bitwarden_items = []
    
    print("Starting Proton Pass export processing...")
    
    # Process each vault
    for vault_id, vault_data in data['vaults'].items():
        stats['vaults'] += 1
        vault_name = vault_data.get('name', 'Unknown Vault')
        print(f"\nProcessing vault: {vault_name}")
        
        # Process items in vault
        for item in vault_data.get('items', []):
            stats['items'] += 1
            
            try:
                content = item['data']['content']
                passkeys = content.get('passkeys', [])
                
                if not passkeys:
                    continue
                
                stats['passkeys'] += len(passkeys)
                metadata = item['data']['metadata']
                print(f"Found {len(passkeys)} passkey(s) in: {metadata.get('name', 'Unnamed')}")
                
                # Convert each passkey
                for passkey in passkeys:
                    bitwarden_item = {
                        "type": 1,
                        "name": metadata.get('name', ''),
                        "notes": metadata.get('note', ''),
                        "login": {
                            "username": content.get('itemEmail', ''),
                            "password": content.get('password', ''),
                            "fido2Credentials": [{
                                "credentialId": passkey.get('credentialId', ''),
                                "keyType": "public-key",
                                "keyAlgorithm": "ECDSA",
                                "keyCurve": "P-256",
                                "keyValue": passkey.get('content', ''),
                                "rpId": passkey.get('rpId', ''),
                                "rpName": passkey.get('rpName', ''),
                                "userHandle": passkey.get('userHandle', ''),
                                "userName": passkey.get('userName', ''),
                                "counter": "1",
                                "userDisplayName": passkey.get('userDisplayName', ''),
                                "discoverable": "true",
                                "creationDate": datetime.fromtimestamp(item.get('createTime', 0)).isoformat() + "Z"
                            }]
                        }
                    }
                    bitwarden_items.append(bitwarden_item)
            except Exception as e:
                print(f"Error processing item: {str(e)}")
                continue

    # Print summary
    print(f"\nConversion Summary:")
    print(f"Vaults processed: {stats['vaults']}")
    print(f"Items checked: {stats['items']}")
    print(f"Passkeys found: {stats['passkeys']}")

    # Create Bitwarden export
    bitwarden_export = {
        "encrypted": False,
        "items": bitwarden_items,
        "folders": [],
        "collections": []
    }

    # Save to file
    output_file = 'bitwarden_converted_passkeys.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(bitwarden_export, f, indent=2, ensure_ascii=False)

    return output_file

if __name__ == "__main__":
    input_file = "data.json"
    output = convert_proton_to_bitwarden(input_file)
    print(f"\nConverted file saved to: {output}")