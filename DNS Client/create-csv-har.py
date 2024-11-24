from browsermobproxy import Server
from selenium import webdriver
import json
import csv




with open('top-1mcopy.csv', 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    i=1
    for row in reader:
        # create a browsermob server instance
        server = Server("../browsermobproxy/bin/browsermob-proxy")
        server.start()
        proxy = server.create_proxy(params=dict(trustAllServers=True))
        # create a new chromedriver instance
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--proxy-server={}".format(proxy.proxy))
        chrome_options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(options=chrome_options)
        # do crawling
        url = row["Site"]
        print(f"Capturing HAR for {url}")

        proxy.new_har("myhar")
        #proxy.new_har("myhar")
        driver.get(url)
        # Save the HAR data to a file
        #output_file = f"{url.replace('://', '_').replace('/', '_')}_output.har"
        output_file = str(i) + ".har"
        i=i+1
        print(output_file)
        with open(output_file, 'w') as har_file:
            har_file.write(json.dumps(proxy.har))
       
        server.stop()
        driver.quit()
