# Movie Link Scraper and Downloader

This Python project allows users to search for and download movies from [jalshamoviez.biz.in](https://www.jalshamoviez.biz.in) by providing a movie name as a command-line argument. The script automates the process of selecting download links, filtering through servers, and saving the movie with a user-friendly filename based on the movie title.

## Features

- Searches for movies based on the name provided by the user.
- Lists available download links and allows selection via `fzf`.
- Downloads the selected movie with a progress bar.
- Saves the movie in the specified `downloads` directory with a title-based filename.

## Prerequisites

- Python 3.x
- `requests`, `beautifulsoup4`, and `tqdm` libraries for web scraping and progress display.
- `fzf` command-line fuzzy finder.

### Python Library Installation

```bash
pip install requests beautifulsoup4 tqdm
```

### Install `fzf`

On **Linux/macOS**:

```bash
sudo apt install fzf     # For Debian/Ubuntu-based systems
brew install fzf         # For macOS users with Homebrew
```

On **Windows**:
Follow instructions from the [fzf GitHub repository](https://github.com/junegunn/fzf).

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/MovieLinkScraper.git
   cd MovieLinkScraper
   ```
2. Create the `downloads` directory if it doesn't already exist:
   ```bash
   mkdir downloads
   ```
3. Run the script with the movie name as a command-line argument.

## Usage

```bash
python main.py "<movie_name>"
```

Replace `<movie_name>` with the name of the movie you want to search and download. For example:

```bash
python main.py "joker"
```

The program will:

1. Search for movies matching the provided name.
2. Display available download links and servers.
3. Download the selected movie file to the `downloads` directory.

## Example

```bash
python main.py "joker"
```

**Expected Output:**

1. List of movies matching "joker" with their respective links.
2. User selects the desired movie and server via `fzf`.
3. Movie downloads to `downloads/The_Joker_2023.mp4` (based on the title of the selected movie).

## License

This project is licensed under the MIT License.

## Acknowledgements

This project uses the following open-source libraries:

- `requests` for making HTTP requests
- `BeautifulSoup` for parsing HTML content
- `tqdm` for displaying download progress bars
- `fzf` for command-line selection and filtering

## Contributing

Pull requests and issues are welcome! Please make sure to update tests as appropriate.

## Disclaimer

This script is for educational purposes only. Ensure that you have the legal right to download and use the content accessed by this script.

```

### Explanation
- **Features** section lists key functionalities.
- **Prerequisites** provides installation commands for necessary libraries and tools.
- **Usage** describes how to run the script and provides an example.
- **License** and **Disclaimer** sections clarify the open-source nature and intended use.

Replace `yourusername` with your actual GitHub username in the clone URL. Let me know if you need further customization!
```
