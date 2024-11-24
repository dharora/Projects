import json
from urllib.parse import urlparse

def is_third_party(main_domain, url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.split('.')[-2] + '.' + parsed_url.netloc.split('.')[-1]

    return domain != main_domain

def count_third_party_domains(har_file_path):
    with open(har_file_path, 'r') as har_file:
        har_data = json.load(har_file)

        # Check if 'log' and 'entries' are present
        if 'log' in har_data and 'entries' in har_data['log'] and 'pages' in har_data['log']:
            entries = har_data['log']['entries']

            main_domain = urlparse(har_data['log']['pages'][0]['title']).netloc

            third_party_domains = {}

            for entry in entries:
                request_url = entry['request']['url']

                if is_third_party(main_domain, request_url):
                    domain = urlparse(request_url).netloc
                    third_party_domains[domain] = third_party_domains.get(domain, 0) + 1

            return third_party_domains

        else:
            print("Invalid HAR file format.")
            return {}

for i in range(179, 299):
    # Replace 'path/to/your/file.har' with the actual path to your HAR file
    har_file_path = str(i) + ".har"
    third_party_domains = count_third_party_domains(har_file_path)

    # Sort the third-party domains by request count in descending order
    sorted_third_party_domains = sorted(third_party_domains.items(), key=lambda x: x[1], reverse=True)

    # Print the top-10 third-party domains
    for domain, count in sorted_third_party_domains[:10]:
        print(f"{domain}: {count} requests")
