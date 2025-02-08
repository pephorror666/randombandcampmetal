import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

# VARIABLES
RANDOM_MA_URL = "https://www.metal-archives.com/band/random"

# FUNCTIONS
def fetch_band_info(url):
    # OBTIENE INFORMACIÓN DE RANDOM ARTIST DE METAL-ARCHIVES
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    band_name_tag = soup.find('h1', class_='band_name')
    band_name = band_name_tag.text.strip() if band_name_tag else "Unknown"
    link = soup.find('h1', class_='band_name').find('a')
    url = link['href']
    details = {}
    for section in ['float_left', 'float_right']:
        info_section = soup.find('dl', class_=section)
        if info_section:
            for dt, dd in zip(info_section.find_all('dt'), info_section.find_all('dd')):
                details[dt.text.strip().strip(':')] = dd.text.strip()
    return {
        'Band Name': band_name,
        'Country of Origin': details.get('Country of origin', 'Unknown'),
        'Location': details.get('Location', 'Unknown'),
        'Genre': details.get('Genre', 'Unknown'),
        'Lyrical Themes': details.get('Themes', 'Unknown'),
        'Current Label': details.get('Current Label', 'Unknown'),
        'Status': details.get('Status', 'Unknown'),
        'M-A url': url
    }

def get_bandcamp_album_url(name):
    """
    Gets the Bandcamp album URL for a given band name.
    Args:
        name (str): The name of the band.
    Returns:
        str: The Bandcamp album URL, or an error message if not found.
    """
    search_query = f"{name}".replace(" ", "+")
    search_url = f"https://bandcamp.com/search?q={search_query}&item_type=a" # item_type=a for albums
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        result_info = soup.find('li', class_='searchresult data-search')
        if result_info:
            album_url_tag = result_info.find('a', href=True)
            if album_url_tag:
                album_url = album_url_tag['href']
                url_modificada = album_url.split("?from")[0]
                return url_modificada
            else:
                return "Error: Album URL not found."
        else:
            return "Error: No search results found."
    except requests.exceptions.RequestException as e:
        #print(f"Error fetching Bandcamp search results: {e}")
        return "Error: Unable to fetch search results."

def extract_band_and_album_name(soup):
    """
    Extracts the band and album name from the Bandcamp page HTML.
    Args:
        soup (BeautifulSoup): The BeautifulSoup object representing the HTML content.
    Returns:
        tuple: A tuple containing the band name and album name. Returns None for either if not found.
    """
    try:
        album_name = soup.find('h2', class_='trackTitle').text.strip()
        band_name_element = soup.find('h3', style='margin:0px;').find('a') # find the tag inside the h3 tag
        band_name = band_name_element.text.strip() if band_name_element else None # extract the text
        return band_name, album_name
    except Exception as e:
        #print(f"Error extracting band and album name: {e}")
        return None, None

def extract_tags(soup):
    """
    Extracts the tags from the Bandcamp page HTML.
    Args:
        soup (BeautifulSoup): The BeautifulSoup object representing the HTML content.
    Returns:
        list: A list of strings representing the tags. Returns an empty list if no tags are found.
    """
    try:
        tag_elements = soup.find_all('a', class_='tag')
        tags = [tag.text.strip() for tag in tag_elements]
        return tags
    except Exception as e:
        #print(f"Error extracting tags: {e}")
        return []

def generate_embed_code(soup, url, album, band):
    """
    Generates a simple embed code for the album. This is a placeholder.
    """
    try:
        meta_tag = soup.find('meta', property='og:video')
        if meta_tag:
            url_embed = meta_tag['content']
            iframe = f'<iframe style="border: 0; width: 100%; height: 100%;" src="{url_embed}" seamless><a href="{url}">{album} by {band}</a></iframe>'
            iframe = iframe.replace('size-large/tracklist=true/artwork-small','linkcol=0f91ff/bgcol=333333/minimal=true/transparent=true')
            return iframe
        else:
            return None
    except Exception as e:
        #print(f"Error extracting embedded URL: {e}")
        return None

def main_bandcamp(url):
    """
    Fetches the HTML content from the specified URL, extracts the band name, album name,
    and tags using BeautifulSoup, and returns extracted information.
    """
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        html_content = response.text
    except requests.exceptions.RequestException as e:
        #print(f"Error fetching URL: {e}")
        return None, None, None, None

    soup = BeautifulSoup(html_content, 'html.parser')
    # Extract the band and album name
    band_name, album_name = extract_band_and_album_name(soup)
    # Extract the tags
    tags = extract_tags(soup)
    # Extract the embedded iframe
    iframe = generate_embed_code(soup, url, album_name, band_name)

    if not band_name or not album_name:
        #print("Could not extract band and/or album name.")
        return None, None, None, None

    if not tags:
        print("No tags found.")

    return band_name, album_name, tags, iframe

def is_metal_band(tags):
    """
    Checks if the band is metal based on the tags.
    Args:
        tags (list): A list of tags.
    Returns:
        bool: True if the band is metal, False otherwise.
    """
    for tag in tags:
        if "metal" in tag.lower() or "grind" in tag.lower() or "death" in tag.lower() or "thrash" in tag.lower():
            return True
    return False

def get_random_metal_band_iframe():
    """
    Finds a random metal band on Metal-Archives, searches for it on Bandcamp,
    and extracts the embed code if it's a metal band.
    """
    while True:
        #print("Searching for a metal band...")
        random_band = fetch_band_info(RANDOM_MA_URL)
        if not random_band:
            #print("Failed to fetch band info. Retrying in 5 seconds...")
            time.sleep(5)
            continue

        #print(f"Found band on Metal-Archives: {random_band['Band Name']}")
        url_bandcamp = get_bandcamp_album_url(random_band['Band Name'])
        if "Error" in url_bandcamp:
            #print(f"Bandcamp search failed: {url_bandcamp}. Retrying...")
            time.sleep(2)
            continue

        #print(f"Found Bandcamp URL: {url_bandcamp}")
        bandcamp_name, bandcamp_album, bandcamp_tags, bandcamp_iframe = main_bandcamp(url_bandcamp)
        if not bandcamp_name or not bandcamp_album or not bandcamp_tags:
            #print("Failed to extract Bandcamp info. Retrying...")
            time.sleep(2)
            continue

        if is_metal_band(bandcamp_tags):
            #print("IT IS A METAL BAND!")
            embed_code = bandcamp_iframe
            #print("Embed Code:")
            #print(embed_code)
            return embed_code
        else:
            #print("Not a metal band. Retrying...")
            time.sleep(2)

# Streamlit App
#st.title("Random Metal Album from Bandcamp")

if 'iframe' not in st.session_state:
    st.session_state['iframe'] = None

if st.button("Get Random Metal Album from Bandcamp"):
    with st.spinner("Finding a metal bandcamp..."):
        st.session_state['iframe'] = get_random_metal_band_iframe()

if st.session_state['iframe']:
    #st.write("Here's your random metal album:")
    st.components.v1.html(st.session_state['iframe'], width = 450, height = 450)
#else:
    #st.write("Click the button to find a random metal album!")
