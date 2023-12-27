# Train Picker Utility

This Python script scrapes train information between two stations and provides historical delay information for each train based on the specified timeline.

## Overview

The Train Picker utility fetches trains running between two specified stations and gathers historical delay data for each train based on the timeline provided. It utilizes web scraping techniques with BeautifulSoup and requests libraries to extract information from eTrain's website.

## Usage

To use this utility, you need Python installed along with the `requests` and `BeautifulSoup` libraries.

### Command-line Usage

Run the script using the command line and provide necessary arguments:

```bash
python train_picker.py --timeline 1m --start-stn New-Delhi-NDLS --destn-stn Chandigarh-CDG
```
