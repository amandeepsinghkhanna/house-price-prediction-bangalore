# Import statements:
import requests # for making web requests
import pandas as pd # for data wrangling
from bs4 import BeautifulSoup # for extracting patterns from string of HTML code
from datetime import datetime # for datetime operations
from requests.api import request # for extracting content from HTML

class ScrapeCommonfloorListing(object):
    """
        class-name: ScrapeCommonfloorListing
        ------------------------------------
        class-description:
        ------------------
        This class that makes a request to the website https://commonfloor.com 
        and extracts the relevant information from its source code.
        class-attributes:
        -----------------
        1. request_url -> str -> The url that needs to be scraped.
        2. max_request_attemps -> int -> Maximum requests to make if the
        previous request attempt did not result in a status == 200.
        3. area -> str -> The area for which the property listings will be 
        scraped.
        class-methods:
        --------------
        1. make_requests
        2. extract_text_content(staticmethod)
        3. scrape_listings_webpage
    """
    def __init__(
        self,
        request_url,
        max_request_attempts,
        area
    ):
        self.request_url = request_url
        self.max_request_attempts = max_request_attempts
        self.area = area
        self.current_timestamp = datetime.now()
        
    @staticmethod
    def make_requests(request_url, max_request_attempts):
        """
            method-name: make_requests
            --------------------------
            This method
            method-attributes:
            ------------------
            1. request_url
            2. max_request_attempts
            method-output:
            --------------
            1. request_result.text -> str -> Source code of the requested 
            website.
        """
        for request_attempt in range(max_request_attempts):
            request_result = requests.get(url=request_url)
            if request_result.ok:
                return request_result.text
            else:
                exception_msg = (
                    f"All of the {max_request_attempts}"+ 
                    "made to https://commonfloor.com have failed!"
                )
                raise Exception(
                    exception_msg
                )

    @staticmethod
    def extract_text_content(soup_object):
        """
            method-name: extract_text_content(staticmethod)
            ---------------------------------
            method-input-parameters:
            ------------------------
            1. soup_object -> bs4.BeautifulSoup -> The soup object with the
            source code of the requested website.
            method-outputs:
            ---------------
            1. df -> pandas.core.DataFrame -> The pandas DataFrame object 
            with the required data extracted from the source code.
        """
        listing_title = (
            soup_object.find("div", attrs={"class": "st_title"}).text
        )
        listing_price = (
            soup_object.find("span", attrs={"class": "s_p"}).text
        )
        listing_url = (
            soup_object.find("div", attrs={"class": "st_title"})
            .find("a").attrs["href"]
        )
        info_data = soup_object.findAll("div", attrs={"class": "infodata"})
        info_data_dict = {}
        for info_datum in info_data:
            key = info_datum.find("small").text
            value = info_datum.find("span").text
            info_data_dict[key] = value
        df = pd.DataFrame({
            "listing_title": [listing_title],
            "listing_price": [listing_price],
            "listing_url": [listing_url]
        })
        for key, value in info_data_dict.items():
            df[key] = value
        return df

    def scrape_listings_webpage(self):
        """
            method-name: scrape_listings_webpage
            ------------------------------------
            method-outputs:
            ---------------
            1. extracted_listings -> pandas.core.DataFrame -> The pandas
            DataFrame object with the required listing data.
        """
        html_code = self.make_requests(
            self.request_url, self.max_request_attempts
        )
        soup_object = BeautifulSoup(html_code)
        scraped_listings = soup_object.findAll(
            "div", attrs={"class": "snb-tile-info"}
        )
        extracted_listings = pd.DataFrame()
        for scraped_listing in scraped_listings:
            extracted_row = self.extract_text_content(
                soup_object=scraped_listing
            )
            extracted_listings = (
                extracted_listings
                .append(extracted_row)
                .reset_index(drop=True)
            )
        extracted_listings["scrapped_timestamp"] = self.current_timestamp
        extracted_listings["area"] = self.area
        extracted_listings["listing_url"] = (
            "https://commonfloor.com" + extracted_listings["listing_url"]
        )
        return extracted_listings