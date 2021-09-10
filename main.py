# Import statements:
import json # for interfacing with .JSON files
import pandas as pd # for data wrangling
from commonfloor import ScrapeCommonfloorListing # for scraping property listings

# Global variables:
MAX_REQUEST_ATTEMPTS = 10

if __name__ == "__main__":
    output_df = pd.DataFrame() # for capturing the output

    # Reading url queries:
    with open("url_queries.json") as url_queries_file:
        url_queries = json.load(url_queries_file)
    
    url_queries = url_queries["data"]

    for region_dict in url_queries:
        area = region_dict["area"]
        
        # Scraping apartment listings:
        for apartment_url in region_dict["apartment_urls"]:
            scraper = ScrapeCommonfloorListing(
                request_url=apartment_url,
                max_request_attempts=MAX_REQUEST_ATTEMPTS,
                area=area,
                property_type="Apartment"
            )
            temp_df = scraper.scrape_listings_webpage()
            output_df = output_df.append(temp_df)
        
        # Scraping villa listings:
        for villa_url in region_dict["villa_urls"]:
            scraper = ScrapeCommonfloorListing(
                request_url=villa_url,
                max_request_attempts=MAX_REQUEST_ATTEMPTS,
                area=area,
                property_type="Villa"
            )
            temp_df = scraper.scrape_listings_webpage()
            output_df = output_df.append(temp_df)

        output_df = output_df.drop_duplicates(
            subset=[
                "listing_url"
            ]
        )