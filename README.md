# Immoweb scraping
[![forthebadge made-with-python](https://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)


## 🏢 Description

This project is part of a larger initiative focused on predicting real estate sales prices in Belgium, specifically using data from the real estate company "Immo Eliza." In this stage, the task is to gather data on at least 15,000 properties across Belgium, which will later serve as the training dataset for a predictive model.

![coworking_img](https://grepsr.com/wp-content/uploads/2024/04/image.jpeg)

## 📦 Repo structure

```
.
├── immoScraping     # venv
├── output
├── main.py
├── Links
├── requirements.txt 
└── README.md
```

## 🛎️ Usage

1. Clone the repository to your local machine.

2. To run the script, you can execute the `main.py` file from your command line:

3. Install the required modules as mentioned in the Requirements file.

## Extracted Data Fields:
The dataset includes the following property attributes:

- Property ID
- Locality name
- Postal code
- Price
- Property type (house or apartment)
- Number of rooms
- Living area (in m²)
- Equipped kitchen (binary: 0 = no, 1 = yes)
- Furnished (binary: 0 = no, 1 = yes)
- Open fire (binary: 0 = no, 1 = yes)
- Terrace (area in m², null if no terrace, or 'yes' if present but unspecified area)
- Garden (area in m², null if no garden)
- Number of facades
- Swimming pool (binary: 0 = no, 1 = yes)
- Building state (e.g., new, to be renovated)

## Data Extraction Steps:

1. URL Collection: Gather URLs from pages listing the available properties.
2. Page Scraping: Scrape each page to extract individual property URLs.
3. URL Storage: Save the URLs into 10 separate CSV files, stored in the "Links" directory, named "links_1.csv," "links_2.csv," and so on.
4. Data Extraction: Loop through the CSV files in the "Links" directory using the request_url() function to scrape the targeted data for each property.
5. File Storage: Save the scraped data into the "output" directory with filenames "property_details_1.csv," "property_details_2.csv," etc.
6. Final Output: Merge all the extracted data into a single file, saved as "all_results.csv."

##  Future Improvements
1. Using selinum for overcome the cookies.

2. using asyncio abd coccurency to sepeed up the process.

3.separate the functions or the classes in different files and to be called in the "main.py" file

## ⏱️ Timeline

This project took four days for completion.

## 📌 Personal Situation
This project was done as part of the AI Boocamp at BeCode.org. 

Connect with me on [LinkedIn](https://www.linkedin.com/in/moustafa-gabil-8a4a6bab/).

