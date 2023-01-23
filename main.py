import difflib as dl

import requests
from bs4 import BeautifulSoup

r = requests.get('https://learn.microsoft.com/en-us/connectors/common/outbound-ip-addresses#power-platform')
soup = BeautifulSoup(r.text, features='html.parser')
# print(soup.prettify())

# find all tables
find_tables = soup.find_all('table')

# list to store the realtime data
managedConnectorsIP = []

for table in find_tables:
    # find table for `Managed connectors IP`
    if 'Managed connectors IP' in table.text:
        rows = table.find_all('tr')
        # display the table
        for i in rows:
            table_data = i.find_all('td')
            data = [j.text for j in table_data]
            # data.append("foo")
            if len(data) != 0:
                managedConnectorsIP.append(" ".join(data))

# compare the realtime data with previous saved data
with open("managedConnectorsIP.txt", "r+") as read_file:
    read_file_data = read_file.read()
    managedConnectorsIP_str = '\n'.join(managedConnectorsIP)

    if read_file_data != managedConnectorsIP_str:
        # we can notify with email or other ways
        print("Got changes in the web page!")
        # diff the data
        for diff in dl.unified_diff(managedConnectorsIP_str, read_file_data):
            print(diff)
        # replace with the new data
        with open("managedConnectorsIP.txt", "w") as write_file:
            write_file.writelines(managedConnectorsIP_str)
