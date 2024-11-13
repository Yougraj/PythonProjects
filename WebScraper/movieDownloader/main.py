import argparse  # Import argparse for command-line argument handling
import os
import re
import subprocess
import tempfile
import threading

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# Define the download directory
download_location = "./downloads"  # Adjust this path as needed

# Ensure the download directory exists
os.makedirs(download_location, exist_ok=True)

# Function to fetch download links for a specific movie
def fetch_download_links(movie_page_url):
    response = requests.get(movie_page_url)
    
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        download_divs = soup.find_all('div', class_='Let')
        
        download_links = []
        for div in download_divs:
            link = div.find('a', class_='fileName')
            if link:
                download_title = link.get_text(strip=True)
                download_url = link['href']
                download_links.append((download_title, download_url))
        
        return download_links
    else:
        print(f"Failed to fetch movie page: {movie_page_url}")
        return []

# Function to fetch all "Click Here To Download" links from the download page
def fetch_all_click_here_links(download_page_url):
    response = requests.get(download_page_url)
    
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        click_here_links = []

        links = soup.find_all('a', class_='dwnLink', title=lambda t: t and "Download" in t)
        
        for link in links:
            if "Click Here To Download" in link.get_text():
                download_title = link.get_text(strip=True)
                download_url = link['href']
                click_here_links.append((download_title, download_url))
        
        return click_here_links
    else:
        print(f"Failed to fetch download page: {download_page_url}")
        return []

# Function to scrape the specific download link from the page
def fetch_specific_download_link(download_page_url):
    response = requests.get(download_page_url)

    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        specific_link = soup.find('a', class_='dwnLink', title=lambda t: t and "Download" in t)

        if specific_link:
            return specific_link['href']
        else:
            print("No specific download link found.")
            return None
    else:
        print(f"Failed to fetch download page for specific link: {download_page_url}")
        return None

# Function to download the video file and show progress
def download_video(video_url, file_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Referer': 'https://www.jalshamoviez.biz.in/'
    }
    
    response = requests.get(video_url, headers=headers, stream=True)

    if response.ok:
        # Get total file size for progress bar
        total_size = int(response.headers.get('content-length', 0))

        print(f"Starting download to {file_path}...")  # Debug print

        # Download file with a progress bar
        with open(file_path, 'wb') as f, tqdm(
            total=total_size, unit='B', unit_scale=True, desc='Downloading'
        ) as bar:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                bar.update(len(chunk))

        print("Download complete!")
        if os.path.exists(file_path):
            print(f"File saved at: {file_path}")
        else:
            print("Download completed but file not found. Check file path.")
    else:
        print(f"Failed to download video: {video_url}")

# Main function to search, download, and play the selected video
def main(movie_name):
    # URL for the search query
    search_url = f"https://www.jalshamoviez.biz.in/mobile/search?find={movie_name}&per_page=1"
    
    response = requests.get(search_url)

    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', class_='L')

        movie_results = []
        for result in results:
            link = result.find('a')
            title = link.get_text(strip=True)

            if movie_name.lower() in title.lower():
                movie_url = link['href']
                movie_results.append((title, movie_url))

        if movie_results:
            with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
                for title, movie_url in movie_results:
                    temp_file.write(f"{title}\n{movie_url}\n\n")
                temp_file_path = temp_file.name

            selected_movie = subprocess.run(['fzf', '--header', f'Select a {movie_name} movie:'], stdin=open(temp_file_path), capture_output=True, text=True)

            if selected_movie.stdout:
                selected_movie_lines = selected_movie.stdout.strip().split('\n')
                selected_movie_url = selected_movie_lines[-1]

                download_links = fetch_download_links(selected_movie_url)
                
                if download_links:
                    with tempfile.NamedTemporaryFile(delete=False, mode='w') as download_file:
                        for title, url in download_links:
                            download_file.write(f"{title} | {url}\n")
                        download_file_path = download_file.name

                    selected_download = subprocess.run(['fzf', '--header', 'Select a download link:'], stdin=open(download_file_path), capture_output=True, text=True)

                    if selected_download.stdout:
                        selected_link = selected_download.stdout.strip().split(" | ")[1]
                        print(f"\nSelected download link:\n{selected_link}")

                        click_here_links = fetch_all_click_here_links(selected_link)
                        
                        if click_here_links:
                            with tempfile.NamedTemporaryFile(delete=False, mode='w') as click_file:
                                for title, url in click_here_links:
                                    click_file.write(f"{title} | {url}\n")
                                click_file_path = click_file.name

                            selected_click_here = subprocess.run(['fzf', '--header', 'Select a download server:'], stdin=open(click_file_path), capture_output=True, text=True)

                            if selected_click_here.stdout:
                                server_2_download_link = selected_click_here.stdout.strip().split(" | ")[1]
                                print(f"\nClick here to download from the selected server:\n{server_2_download_link}")

                                specific_download_link = fetch_specific_download_link(server_2_download_link)
                                if specific_download_link:
                                    print(f"Direct download link: {specific_download_link}")

                                    # Extract title and sanitize it for filename
                                    download_title = selected_download.stdout.strip().split(" | ")[0]
                                    sanitized_title = re.sub(r'[<>:"/\\|?*]', '_', download_title)  # Replace invalid characters
                                    file_path = os.path.join(download_location, f"{sanitized_title}.mp4")

                                    download_thread = threading.Thread(target=download_video, args=(specific_download_link, file_path))
                                    download_thread.start()

                                    download_thread.join()
                                else:
                                    print("Failed to get the specific download link.")
                            else:
                                print("No server selected.")
                        else:
                            print("No 'Click Here To Download' links found.")
                    else:
                        print("No download link selected.")
                else:
                    print("No download links found for the selected movie.")
            else:
                print("No movie selected.")
        else:
            print(f"No results found for '{movie_name}'.")
    else:
        print("Failed to perform search.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Movie Downloader")
    parser.add_argument("movie_name", help="The name of the movie to search and download.")
    args = parser.parse_args()
    main(args.movie_name)
