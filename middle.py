import sys
import json
import requests

#url = "http://192.168.191.232:8085/test/"
#url="http://localhost:8080"
url="http://192.168.191.2:8000/check_code/"
headers = {
    "Content-Type": "application/json"
}

def main():
    try:
        # Read input from stdin
        input_data = sys.stdin.read()
        input_json = json.loads(input_data)
        
        # Process the input data
        response = requests.post(url, json=input_json, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"Failed to get response. Status code: {response.status_code}")
        
#        print("B")
        response_json=response.json()
        
        output_json = {
            'length_of_code': len(input_json['code']),
            'lines_of_code': len(input_json['code'].splitlines()),
            'message': 'Received and processed successfully',
            'bugs': response_json['bugs']
        }

        # Write output to stdout
        print(json.dumps(output_json))
    except Exception as e:
        error_json = {
            'error': str(e)
        }
        print(json.dumps(error_json), file=sys.stderr)

if __name__ == '__main__':
    main()