import urllib3
import ssl
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
from gtts import gTTS

# Disable SSL warnings (not recommended for production use)
urllib3.disable_warnings(InsecureRequestWarning)

# Create a custom SSL context with less strict security settings
custom_ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
custom_ssl_context.set_ciphers("DEFAULT@SECLEVEL=1")

# Create an HTTP pool manager with the custom SSL context
http = urllib3.PoolManager(ssl_context=custom_ssl_context)

url = "https://pdc.lums.edu.pk/"

try:
    response = http.request("GET", url)
    # Print the content of the response
    content = response.data.decode("utf-8")
    # print(response.data.decode("utf-8"))
    print("CONTENT FETCHED")
except Exception as e:
    print("Error:", e)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')

# Initialize variables to store headings, foods, and prices
headings = ['Fusion Cafe', 'Snacks', 'The Green Olive Cafe',
            'Breakfast', 'Lunch', 'Dinner', 'Dinner (EDH Lawn)']
foods = []
prices = []

# Find all the heading elements (e.g., Fusion Cafe, Snacks, The Green Olive Cafe)
heading_elements = soup.find_all('h3')

# Find all the tables containing food items and prices
table_elements = soup.find_all('table', class_='table_border')

# Loop through the tables and extract food items and prices
for heading, table in zip(heading_elements, table_elements):
    # Extract the heading text
    heading_text = heading.text.strip()
    # headings.append(heading_text)

    # Find all the rows in the table (excluding the header row)
    rows = table.find_all('tr')[1:]

    # Initialize lists to store food items and prices for this section
    section_foods = []
    section_prices = []

    # Loop through the rows and extract food items and prices
    for row in rows:
        cells = row.find_all('td')

        # Check if there are at least 5 cells in the row (to avoid index out of range error)
        if len(cells) >= 5:
            item = cells[1].text.strip()
            price = cells[4].text.strip()
            section_foods.append(item)
            section_prices.append(price)

    # Combine the food items and prices into a single string for this section
    section_str = '\n'.join(
        [f"{item} - {price} Rs." for item, price in zip(section_foods, section_prices)])

    # Append the section string to the list of foods and prices
    foods.append(section_str)

# Combine all the headings, foods, and prices into a single string
result_str = '\n\n'.join(
    [f"{heading}\n{food}" for heading, food in zip(headings, foods)])

# Print the result
print(result_str)

# print(headings)

# Your text to convert to speech
# text = result_str

# # Create a gTTS object
# tts = gTTS(text)

# # Specify the filename for the audio file (e.g., output.mp3)
# audio_filename = "output.mp3"

# # Save the speech as an audio file
# tts.save(audio_filename)

# print(f"Audio file '{audio_filename}' has been created.")

# import pyttsx3

# # Initialize the text-to-speech engine
# engine = pyttsx3.init()

# # Set properties (optional)
# engine.setProperty("rate", 150)  # Speed of speech
# engine.setProperty("volume", 1.0)  # Volume (0.0 to 1.0)

# # Text to be converted to speech
# text = result_str

# text = text.replace("Rs.", "Rupees")

# # Specify the output audio file path (e.g., "output.mp3")
# output_file = "output.mp3"

# # Convert the text to speech and save it to the audio file
# engine.save_to_file(text, output_file)

# # Wait for the speech to be saved to the file
# engine.runAndWait()
