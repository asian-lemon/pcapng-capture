from bs4 import BeautifulSoup
import requests
import pandas as pd

# Function to scrape IPVoid
def scrape_ipvoid(ip):
    url = f"https://www.ipvoid.com/ip-blacklist-check/"
    payload = {"ip": ip}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        soup = BeautifulSoup(response.text, "html.parser")
        status = soup.find("span", {"class": "label"}).get_text()
        return {"IP": ip, "Blacklist Status": status}
    except Exception as e:
        return {"IP": ip, "Error": str(e)}

# List of IPs to check
ips_to_check = [
    "192.168.18.114",
    "239.255.255.250",
    "192.0.66.233",
    "8.8.4.4"
]
# Scrape each IP
results = [scrape_ipvoid(ip) for ip in ips_to_check]

# Convert results to a DataFrame
df = pd.DataFrame(results)

# Save results to a CSV file
df.to_csv("ip_void_results.csv", index=False)

print(df)
