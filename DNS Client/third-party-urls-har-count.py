import json

def read_request_urls_from_har(har_file_path):
    with open(har_file_path, 'r') as har_file:
        har_data = json.load(har_file)

        # Check if 'log' and 'entries' are present
        if 'log' in har_data and 'entries' in har_data['log']:
            entries = har_data['log']['entries']

            # Extract request URLs
            request_urls = [entry['request']['url'] for entry in entries]

            return request_urls
        else:
            print("Invalid HAR file format.")
            return []

# Replace 'path/to/your/file.har' with the actual path to your HAR file
har_file_path = 'myhar.har'
urls = read_request_urls_from_har(har_file_path)

# Print the extracted URLs
for url in urls:
    print(url)
