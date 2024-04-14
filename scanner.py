import argparse
import pandas as pd
import requests
import json
import io

permission_severity = {
    "cookies": "critical",
    "debugger": "critical",
    "*://*/:": "critical",
    "*://*/*:": "critical",
    "<all_urls>": "critical",
    "webRequest": "critical",
    "declarativeWebRequest": "critical",
    "clipboardRead": "high",
    "contentSettings": "high",
    "declarativeNetRequest": "high",
    "desktopCapture": "high",
    "displaySource": "high",
    "dns": "high",
    "experimental": "high",
    "proxy": "high",
    "history": "high",
    "idltest": "high",
    "mdns": "high",
    "privacy": "high",
    "tabCapture": "high",
    "pageCapture": "high",
    "tabs": "high",
    "vpnProvider": "high",
    "http://*/*:": "high",
    "https://*/*:": "high",
    "file:///*:": "high",
    "http://*/:": "high",
    "https://*/:": "high",
    "webNavigation": "medium",
    "ttsEngine": "medium",
    "signedInDevices": "medium",
    "storage": "medium",
    "system.storage": "medium",
    "topSites": "medium",
    "bookmarks": "medium",
    "clipboardWrite": "medium",
    "downloads": "medium",
    "fileSystemProvider": "medium",
    "geolocation": "medium",
    "management": "medium",
    "nativeMessaging": "medium",
    "processes": "medium",
    "activeTab": "low",
    "alarms": "none",
    "background": "low",
    "browsingData": "none",
    "certificateProvider": "low",
    "contextMenus": "none",
    "declarativeContent": "none",
    "documentScan": "low",
    "enterprise.deviceAttributes": "none",
    "enterprise.platformKeys": "low",
    "fileBrowserHandler": "none",
    "fontSettings": "none",
    "gcm": "none",
    "hid": "low",
    "identity": "low",
    "idle": "none",
    "networking.config": "low",
    "notifications": "low",
    "platformKeys": "low",
    "power": "none",
    "printerProvider": "low",
    "sessions": "none",
    "system.cpu": "none",
    "system.display": "none",
    "system.memory": "none",
    "tts": "none",
    "unlimitedStorage": "none",
    "usbDevices": "low",
    "wallpaper": "none",
    "webRequestBlocking": "low"
    }
failed_indexes = []

def file_prep(file_path):
    df = pd.read_excel(file_path)
    column_name = 'Google Chrome Extensions ID'
    skip = ['Temp', 'ghbmnnjooekpmoecnnnilnnbdlolhkhi', 'nmmhkkegccagdldgiimedpiccmgmieda', 'callobklhcbilhphinckomhgkigmfocg']
    for string in skip:
        df[column_name] = df[column_name].str.replace(string, ' ').str.replace(',', '')
    df[column_name] = df[column_name].str.strip().str.split()
    df = df.dropna(subset=['Google Chrome Extensions ID'])
    df = df[['Google Chrome Extensions ID']]
    df = df[df['Google Chrome Extensions ID'].map(len) > 0]
    df['Google Chrome Extensions ID'] = df['Google Chrome Extensions ID'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x).str.replace(' ', '')

    string = ','.join(df['Google Chrome Extensions ID'])
    unique_string = ','.join(set(string.split(',')))
    split_strings = unique_string.split(',')
    lambda_file = pd.DataFrame(split_strings, columns=['extension_id'])
    print(lambda_file)
    return lambda_file


def fetch_permissions(extension_id, version):
    if '@' in extension_id:
        url_permissions = f"https://api.crxcavator.io/v1/report/{extension_id}/{version}?platform=Firefox"
    else:
        url_permissions = f"https://api.crxcavator.io/v1/report/{extension_id}/{version}"
    #url_permissions = f"https://api.crxcavator.io/v1/report/{extension_id}/{version}"
    payload_permissions = {}
    headers_permissions = {
        'Accept': 'application/json'
    }
    permissions_response = requests.request("GET", url_permissions, headers=headers_permissions, data=payload_permissions)
    response_permissions = permissions_response.json()
    if not response_permissions:
        print("Empty response")
        return

    permissions_request = response_permissions.get('data')['manifest'].get('permissions') 
    if not permissions_request:
        print("Permissions request is empty")
        return
    '''response_permissions = permissions_response.json()
    permissions_request = response_permissions.get('data', {}).get('manifest', {}).get('permissions', [])'''
    permissions_with_severity = {}
    for permission in permissions_request:
        matched = False
        for pattern, severity in permission_severity.items():
            if permission.endswith(pattern):
                permissions_with_severity[permission] = severity
                matched = True
                break
            if not matched:
                permissions_with_severity[permission] = "Unknown"
    print(permissions_with_severity)
    return permissions_request, permissions_with_severity


def lambda_handler(file_path):
    lambda_file = file_prep(file_path)
    data = []
    failed_extension_ids = []

    for index, row in lambda_file.iterrows():
        try:
            extension_id = row['extension_id']
            if '@' in extension_id:
                url_submit = "https://api.crxcavator.io/v1/submit?platform=Firefox"
            else:
                url_submit = "https://api.crxcavator.io/v1/submit"
            payload_submit = json.dumps({"extension_id": extension_id})
            headers_submit = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            response_submit = requests.post(url_submit, headers=headers_submit, data=payload_submit)
            submit_data = response_submit.json()

            extension_id = submit_data.get('extensionID', '')
            platform = submit_data.get('platform', '')
            print (platform)
            version = submit_data.get('version', '')
            url_report = f"https://api.crxcavator.io/v1/report/{extension_id}/{version}?platform={platform}"
            headers_report = {'Accept': 'application/json'}
            

            response_report = requests.get(url_report, headers=headers_report)
            report_data = response_report.json()

            extension_name = report_data.get('data', {}).get('webstore', {}).get('name', '')
            risk_section = report_data.get('data', {}).get('risk', {})
            permission_value = risk_section.get('permissions', {}).get('total', 0)

            retire_section = report_data.get('data', {}).get('retire')
            if retire_section is not None:
                print('Vulnerable Extension')
                vulnerability = 'Extension has active vulnerabilities'
            else:
                print('Safe Extension')
                vulnerability = 'No active vulnerabilities'

            safety_status = "Safe" if permission_value <= 50 else "Unsafe"

            if '@' in extension_id:
                url_metadata = f"https://api.crxcavator.io/v1/metadata/{extension_id}?platform=Firefox"
            else:
                url_metadata = f"https://api.crxcavator.io/v1/metadata/{extension_id}"
            headers_metadata = {'Accept': 'application/json'}

            response_metadata = requests.get(url_metadata, headers=headers_metadata)
            metadata_data = response_metadata.json()

            users = metadata_data.get('users', '')
            rating = metadata_data.get('rating', '')
            
            #if index == 0:
                #permissions_request = fetch_permissions(extension_id, version)
            permissions_request, permissions_with_severity = fetch_permissions(extension_id, version)
            #print(permissions_request)'''
            permissions_with_severity_str = str(permissions_with_severity)

            data.append({
                "Extension ID": extension_id,
                "Extension Name": extension_name,
                "Platform": platform,
                "Version": version,
                "Vulnerability": vulnerability,
                "Safety Status": safety_status,
                "Users": users,
                "Rating": rating,
                "Permissions": permissions_with_severity_str
            })
            pass
        
        except Exception as e:
            print(f"Error processing extension ID {row['extension_id']}: {e}")
            failed_extension_ids.append(row['extension_id'])
        continue
        

    failed_df = pd.DataFrame(failed_extension_ids, columns=['Failed Extension ID'])
    failed_excel_file = '/Users/temp/extensions/failed_extensions_safety_status_output.xlsx'
    failed_df.to_excel(failed_excel_file, index=False)

    new_df = pd.DataFrame(data)
    new_excel_file = '/Users/temp/extensions/extensions_safety_status_output.xlsx'
    new_df.to_excel(new_excel_file, index=False)

    return {'statusCode': 200, 'body': json.dumps('Processed file saved locally')}

def main():
    parser = argparse.ArgumentParser(description='CLI tool to read Excel files.')
    parser.add_argument('file_path', type=str, help='The path to the Excel file.')
    args = parser.parse_args()
    lambda_handler(args.file_path)

if __name__ == "__main__":
    main()