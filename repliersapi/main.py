import requests
import json

def remove_empty(d):
    """Recursively remove empty values (None, '', [], {}) from a dictionary."""
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [v for v in (remove_empty(v) for v in d) if v]
    return {k: v for k, v in ((k, remove_empty(v)) for k, v in d.items()) if v}

url = "https://sandbox.repliers.io/listings?listings=true&operator=AND&sortBy=updatedOnDesc&status=A"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "REPLIERS-API-KEY": "n9ZQqhomiI697IlZBBjX8tI1HRpCOs"
}

response = requests.get(url, headers=headers)

# Load the JSON response as a Python dictionary
data = json.loads(response.text)

# Access the first listing and print it
first_listing = data["listings"][0]

# Remove the keys with empty values from the first_listing dictionary
first_listing_clean = remove_empty(first_listing)

print(first_listing_clean)

print(first_listing_clean.get('mlsNumber'))
