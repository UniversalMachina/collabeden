import requests
import json
from tkinter import *

def remove_empty(d):
    """Recursively remove empty values (None, '', [], {}) from a dictionary."""
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [v for v in (remove_empty(v) for v in d) if v]
    return {k: v for k, v in ((k, remove_empty(v)) for k, v in d.items()) if v}

def get_listings():
    city = city_entry.get()
    url = f"https://sandbox.repliers.io/listings?city={city}&listings=true&operator=AND&sortBy=updatedOnDesc&status=A"

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

    # display the response in the text widget
    response_text.delete(1.0, END)
    response_text.insert(END, "First Listing: \n")
    response_text.insert(END, json.dumps(first_listing_clean, indent=4))  # to nicely format the dictionary

    # Print the 'mlsNumber'
    mls_number = first_listing_clean.get('mlsNumber')
    response_text.insert(END, "\nMLS Number: " + str(mls_number))

# create tkinter window
root = Tk()

# create label
city_label = Label(root, text="Enter city:")
city_label.pack()

# create entry to input the city
city_entry = Entry(root)
city_entry.pack()

# create button to get listings
submit_button = Button(root, text="Get Listings", command=get_listings)
submit_button.pack()

# create text widget to display the response
response_text = Text(root)
response_text.pack()

root.mainloop()
