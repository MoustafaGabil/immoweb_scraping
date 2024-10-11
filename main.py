import requests
from bs4 import BeautifulSoup
import re
import math
import requests
import pandas as pd

# immoweb house and apartment fore sale's page
immoweb_sale_link = "https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page=1&orderBy=relevance"
# generating the links of 333 pages
first_group_pages_link_sale = "https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&amp%3BorderBy=relevance&amp%3Bpage=2"
p = 1
last_p = 333
group_pages_link_sale = []
# adding 1st page in 1st cell of list
group_pages_link_sale.append(first_group_pages_link_sale)
for p in range(2, last_p + 1):
    group_pages_link_sale.append(
        first_group_pages_link_sale + "&page=" + str(p)
    )  # adding the link + new number of pages
# group_pages_link_sale
# extracting all linkes (+10000 links) for sale from immoweb// by group_pages_link_sale
number_of_pages = 333
all_links = []
group_pages_link_sale_test = group_pages_link_sale[:number_of_pages]
for l in group_pages_link_sale_test:  # a loop to scrape that 333 group pages of immoweb
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = session.get(l, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    for tag_a in soup.find_all(
        "a", class_="card__title-link", href=True
    ):  # extracting all item links paer group page
        all_links.append(tag_a["href"])

unique_links = set(all_links)  # remove any duplication of links
# Filter out unwanted links that contains the real estate projects
filtered_links = [
    link for link in unique_links if "/new-real-estate-project-" not in link
]
num_files = 10
links_per_file = math.ceil(len(filtered_links) / num_files)  # Divide links evenly

for i in range(num_files):
    # Get the portion of links for the current file
    start_index = i * links_per_file
    end_index = min(
        (i + 1) * links_per_file, len(filtered_links)
    )  # to stay within the number of links and not to exceed it
    links_chunk = filtered_links[start_index:end_index]

    # Save the chunk to a CSV file
    df = pd.DataFrame(links_chunk, columns=["URL"])
    file_name = f"links_{i+1}.csv"  # Naming the files as links_1.csv, links_2.csv, etc.
    df.to_csv(
        f"C:\\Users\\mgabi\\Desktop\\becode\\becode_projects\\immoweb_scraping\\Links\\{file_name}",
        index=False,
        encoding="utf-8",
    )

print("Links saved to multiple CSV files.")
df = pd.DataFrame(all_links, columns=["URL"])  # creating a csv file for all links
df.to_csv(
    "C:\\Users\\mgabi\\Desktop\\becode\\becode_projects\\immoweb_scraping\\all_links.csv",
    index=False,
    encoding="utf-8",
)
df = pd.DataFrame(
    filtered_links, columns=["URL"]
)  # creating a csv file for all filtered links
df.to_csv(
    "C:\\Users\\mgabi\\Desktop\\becode\\becode_projects\\immoweb_scraping\\filtered_links.csv",
    index=False,
    encoding="utf-8",
)


def request_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.content, "html.parser")
    property_details = []
    # ID
    try:
        html = soup.find("meta", {"property": "og:url"}).get("content")
        html_list = html.split("/")
        Property_ID = html_list[-1]
    except Exception as e:
        print(f"Error in Property_ID: {e}")
        Property_ID = None
    # Postal code
    try:
        postal_code = html_list[-2]
    except Exception as e:
        print(f"Error in postal_code : {e}")
        postal_code = None
    # Locality
    try:
        locality = html_list[-3]
    except Exception as e:
        print(f"Error in locality : {e}")
        locality = None
    # Price
    try:
        home_meta_info = soup.find_all("div", {"class": "grid__item desktop--9"})
        price = (
            home_meta_info[0]
            .find("p", {"class": "classified__price"})
            .find_all("span", {"class": "sr-only"})[0]
            .text.strip()
        )
        price = re.sub(r"[^\d.,\-+]", "", price)
    except Exception as e:
        print(f"Error in price : {e}")
        price = None
    # Type of property
    try:
        Type_of_property = html_list[-5]
    except Exception as e:
        print(f"Error in Type_of_property: {e}")
        Type_of_property = None
    # Number of bed rooms
    try:
        home_prop_info = soup.find_all("div", {"class": "text-block__body"})[
            0
        ].find_all("div", {"class": "overview__column"})
        bed_rooms = (
            home_prop_info[0]
            .find_all("div", {"class": "overview__item"})[0]
            .find_all("span", {"class": "overview__text"})[0]
            .text.strip()
        )
        bed_rooms = re.search(r"\d+", bed_rooms)
        if bed_rooms:
            bed_rooms = bed_rooms.group()  # Extract the matched number as a string
        else:
            bed_rooms = None
    except Exception as e:
        print(f"Error in bed_rooms : {e}")
        bed_rooms = None

    try:
        space = (
            home_prop_info[1]
            .find_all("div", {"class": "overview__item"})[0]
            .find_all("span", {"class": "overview__text"})[0]
            .text.strip()
        )
        space = re.findall(r"\d+", space)[0]  # Extract only the digits
    except Exception as e:
        print(f"Error in space: {e}")
        space = None
    # Kitchen
    try:
        kitchen_keywords = (
            "Kitchen type",
            "Type of kitchen",
        )  # as sometimes it has one of these names, I am not using regex here but, it could be used too
        kitchen_th = soup.find(
            "th", string=lambda x: x and x.strip() in kitchen_keywords
        )
        if kitchen_th:
            kitchen = kitchen_th.find_next_sibling("td").contents[0].strip()

            # Now, check for the kitchen types you're interested in
            if kitchen in (
                "Installed",
                "Installed",
                "Hyper equipped",
                "USA  Hyper equipped",
                "Semi equipped",
                "USA hyper equipped",
            ):
                kitchen_type = 1
            else:
                kitchen_type = 0
        else:
            kitchen_type = (
                0  # Default value if 'Kitchen type' or 'Type of kitchen' not found
            )
    except Exception as e:
        print(f"Error in kitchen: {e}")
        kitchen_type = None
    # Building cindition
    try:
        building_condition_header = soup.find(
            "th", string=lambda x: x and x.strip() == "Building condition"
        ).find_parent("tr")

        building_condition = (
            building_condition_header.find("td", class_="classified-table__data")
            .contents[0]
            .strip()
        )
    except Exception as e:
        print(f"Error in building_condition: {e}")
        building_condition = None
    # Number of facades
    try:
        facade_keywords = re.compile(r"Number of (frontages|facades)", re.IGNORECASE)
        facades_th = soup.find("th", string=facade_keywords)
        facades = (
            facades_th.find_next_sibling("td").contents[0].strip()
            if facades_th
            else None
        )
        if facades:
            Number_of_facades = facades
        else:
            Number_of_facades = None

    except Exception as e:
        print(f"Error in Number_of_facades : {e}")
        Number_of_facades = None

    # Furnished
    try:
        Furnished = (
            soup.find("th", string=lambda x: x and x.strip() == "Furnished")
            .find_next_sibling("td")
            .contents[0]
            .strip()
        )
        if Furnished == "Yes":
            Furnished = 1
        else:
            Furnished = 0
    except Exception as e:
        print(f"Error in Furnished: {e}")
        Furnished = 0
    # open fire space
    try:
        Open_fire = (
            soup.find("th", string=lambda x: x and x.strip() == "How many fireplaces?")
            .find_next_sibling("td")
            .contents[0]
            .strip()
        )
        if Open_fire:
            Open_fire = 1
        else:
            Open_fire = 0
    except Exception as e:
        print(f"Error in Open_fire: {e}")
        Open_fire = 0
    # Swimming_pool

    try:
        Swimming_pool = (
            soup.find(
                "th", string=lambda text: text and "Swimming pool" in text.strip()
            )
            .find_next_sibling("td")
            .contents[0]
            .strip()
        )

        if Swimming_pool == "Yes":
            Swimming_pool = 1
        else:
            Swimming_pool = 0

    except Exception as e:
        print(f"Error in Swimming_pool: {e}")
        Swimming_pool = 0
    # Garden
    try:
        # garden = soup.find('th', string=lambda x: x and x.strip() == 'Garden surface').find_next_sibling('td').contents[0].strip()
        garden = (
            soup.find("th", string=re.compile(r"^Garden.*"))
            .find_next_sibling("td")
            .contents[0]
            .strip()
        )
        if garden:
            garden = garden
        else:
            garden = None
    except Exception as e:
        print(f"Error in garden: {e}")
        garden = None
    # Terrace
    try:
        Terrace = (
            soup.find("th", string=re.compile(r"^Terrace.*"))
            .find_next_sibling("td")
            .contents[0]
            .strip()
        )
        if Terrace:
            Terrace = Terrace
        else:
            Terrace = None

    except Exception as e:
        print(f"Error in Terrace: {e}")
        Terrace = None
    property_details.append(
        {
            "Property ID": Property_ID,
            "Postal code": postal_code,
            "Locality name": locality,
            "Price": price,
            "Type of property": Type_of_property,
            "Number of rooms": bed_rooms,
            "Living area": space,
            "Equipped kitchen": kitchen_type,
            "State of building": building_condition,
            "Number of facades": Number_of_facades,
            "Furnished": Furnished,
            "Open fire": Open_fire,
            "Swimming pool": Swimming_pool,
            "Garden (m²)": garden,
            "Terrace (m²)": Terrace,
        }
    )
    return property_details


"""
Here you open each file that has been created before to loop over them, please specify the inputfile path and the output path 
and number of files which is must be the same number of created files links. 
"""
num_files = 10  # Define number of files that will contain the results, it must be the same number as the links files
input_file_path = "C:\\Users\\mgabi\\Desktop\\becode\\becode_projects\\immoweb_scraping\\Links\\links_{}.csv"
output_file_path_template = "C:\\Users\\mgabi\\Desktop\\becode\\becode_projects\\immoweb_scraping\\output\\property_details_{}.csv"


for i in range(1, num_files + 1):  # Loop from 1 to 10
    input_file_path = input_file_path.format(i)
    property_details = []
    try:
        df = pd.read_csv(input_file_path)
        List_url = df["URL"].tolist()
        for url in List_url:
            property_details.extend(request_url(url))
        df_properties = pd.DataFrame(property_details)
        output_file_path = output_file_path_template.format(i)
        df_properties.to_csv(output_file_path, index=False, encoding="utf-8")

        print(f"CSV file created: {output_file_path}")

    except Exception as e:
        print(f"The file with the path: {input_file_path}: {e}")
# looping over the whole created files after creation and combine them in one file. It will be after creation as the creation of the files might have problems
file_path_for_all_pro = "C:\\Users\\mgabi\\Desktop\\becode\\becode_projects\\immoweb_scraping\\output\\property_details_{}.csv"

all_files = []
for i in range(1, num_files + 1):
    try:
        input_file_path = file_path_for_all_pro.format(i)
        df = pd.read_csv(input_file_path)
        all_files.append(df)
        print(f"Data from {input_file_path} loaded successfully.")
    except Exception as e:
        print(f"Failed to load {input_file_path}: {e}")
df_combined = pd.concat(all_files, ignore_index=True)
output_file_path = "C:\\Users\\mgabi\\Desktop\\becode\\becode_projects\\immoweb_scraping\\output\\all_results.csv"
df_combined.to_csv(output_file_path, index=False, encoding="utf-8")
print(f"Final file has been created in: {output_file_path}")
