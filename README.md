# Random Metal Album Bandcamp Embed Streamlit App

## Overview

This Streamlit application fetches a random metal band from Metal-Archives, searches for their album on Bandcamp, and displays an embedded player for the album.  It continuously searches until a band identified as "metal" is found based on Bandcamp tags.

## Features

*   **Random Metal Band Discovery:** Fetches random band information from Metal-Archives (metal-archives.com).
*   **Bandcamp Integration:** Searches for the band's album on Bandcamp.
*   **Genre Filtering:**  Filters search results based on Bandcamp tags to ensure the displayed album is from a metal band.
*   **Embed Display:** Displays the Bandcamp album as an embedded player in the Streamlit app.
*   **Continuous Search:** Automatically retries the search process if a non-metal band or an error occurs.

## Requirements

To run this application, you need the following Python libraries:

*   streamlit
*   requests
*   beautifulsoup4

These dependencies are listed in the `requirements.txt` file.

## Installation

1.  **Clone the repository:**

    ```
    git clone [repository_url]
    cd [repository_directory]
    ```

    Replace `[repository_url]` with the actual URL of your GitHub repository and `[repository_directory]` with the name of the directory you cloned into.

2.  **Create a virtual environment (recommended):**

    ```
    python -m venv venv
    ```

3.  **Activate the virtual environment:**

    *   On Windows:

        ```
        venv\Scripts\activate
        ```

    *   On macOS and Linux:

        ```
        source venv/bin/activate
        ```

4.  **Install the dependencies:**

    ```
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the Streamlit application:**

    ```
    streamlit run app_terminal.py
    ```

2.  **Access the application:**

    Open your web browser and navigate to the URL displayed in the terminal (usually `http://localhost:8501`).

3.  **Interact with the app:**

    The application will automatically start searching for a random metal album.  Once found, the embedded player will be displayed.

## Code Structure

*   **`app_terminal.py`:** The main Python file containing the Streamlit application code.
*   **`requirements.txt`:**  A list of Python packages required to run the application.

## Functions

*   **`fetch_band_info(url)`:** Fetches band information from a Metal-Archives URL.
*   **`get_bandcamp_album_url(name)`:** Searches for a band's album on Bandcamp and returns the album URL.
*   **`extract_band_and_album_name(soup)`:** Extracts the band and album name from a Bandcamp page's HTML.
*   **`extract_tags(soup)`:** Extracts genre tags from a Bandcamp page's HTML.
*   **`generate_embed_code(soup, url, album, band)`:** Generates the HTML embed code for the Bandcamp player.  *Note: This function might need adjustments depending on Bandcamp's embed format.*
*   **`is_metal_band(tags)`:** Checks if a band is classified as metal based on its Bandcamp tags.
*   **`main()`:** The main function that orchestrates the entire process of finding and displaying a random metal album.

## Notes

*   The application relies on the HTML structure of Metal-Archives and Bandcamp. Changes to these websites may require updates to the code, especially the functions using `BeautifulSoup`.
*   The `generate_embed_code` function may need to be adjusted to properly extract and format the embed code from Bandcamp, as Bandcamp's embed format can vary.
*   Error handling is included to catch common issues like network errors or missing data, but further improvements may be necessary for production use.

## License

[If you use my code please just give me the credit for it]
[Specify the license under which your code is released.  For example:  MIT License, Apache 2.0, or GPLv3.  If you don't want to specify a license, state "No License".]

## Author

[Pep Horror - https://metalhead.club/@pephorror - @pephorror.bsky.social ]
