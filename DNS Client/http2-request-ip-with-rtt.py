import httpx
import requests
import time

def http2_request(url):
    try:
        # Create an HTTPX client with HTTP/2 support
        with httpx.Client(http2=True) as client:
            # Make an HTTP/2 GET request
            start_time = time.time()
            response = client.get(url)
            end_time = time.time()
            rtt = end_time - start_time
            print("RTT1 (Accessed site first time): ", rtt)

            # Check if the response is a redirect (HTTP status code 301 or 302)
            if response.status_code in [301, 302]:
                # Extract the new URL from the 'Location' header
                new_url = response.headers['Location']

                # Make a request to the new URL
                new_response = client.get(new_url)
                end_time = time.time()
                rtt = end_time - start_time
                print("RTT2 (Accessed site after redirection): ", rtt)

                # Print the response content
                print(new_response.text)
            else:
                # Print the response content if it's not a redirect
                print(response.text)    
            # Print the response content
            #print(response.text)

    except httpx.HTTPError as e:
        print(f"HTTP error: {e}")


# Example for tmz.com IP address
#ip_address = "64.225.154.37"
ip_address = "142.250.191.46"
url = f"http://{ip_address}"  # Replace with the actual URL
print(url)
http2_request(url)