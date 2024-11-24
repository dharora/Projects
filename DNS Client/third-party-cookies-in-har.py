import json
from urllib.parse import urlparse

def is_third_party(main_domain, cookie_domain):
    return cookie_domain != main_domain

def extract_cookies_from_entries(entries, main_domain):
    third_party_cookies = {}

    for entry in entries:
        response_cookies = entry['response']['cookies'] if 'response' in entry and 'cookies' in entry['response'] else []
        request_cookies = entry['request']['cookies'] if 'request' in entry and 'cookies' in entry['request'] else []

        for cookie in response_cookies + request_cookies:
            cookie_domain = cookie.get('domain', '')
            if is_third_party(main_domain, cookie_domain):
                cookie_name = cookie.get('name', '')
                third_party_cookies[cookie_name] = third_party_cookies.get(cookie_name, 0) + 1

    return third_party_cookies

def identify_third_party_cookies(har_file_path):
    with open(har_file_path, 'r') as har_file:
        har_data = json.load(har_file)

        # Check if 'log' and 'entries' are present
        if 'log' in har_data and 'entries' in har_data['log'] and 'pages' in har_data['log']:
            entries = har_data['log']['entries']
            main_domain = urlparse(har_data['log']['pages'][0]['title']).netloc

            third_party_cookies = extract_cookies_from_entries(entries, main_domain)

            return third_party_cookies

        else:
            print("Invalid HAR file format.")
            return {}

# Replace 'path/to/your/file.har' with the actual path to your HAR file
har_file_path = 'myhar.har'
third_party_cookies = identify_third_party_cookies(har_file_path)

# Sort the third-party cookies by occurrence in descending order
sorted_third_party_cookies = sorted(third_party_cookies.items(), key=lambda x: x[1], reverse=True)

# Print the top-10 third-party cookies
for cookie_name, count in sorted_third_party_cookies[:10]:
    print(f"{cookie_name}: {count} occurrences")
