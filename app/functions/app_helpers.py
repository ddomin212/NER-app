"""
This module contains helper functions for the AI chatbot application. 
It includes functions for writing data to an Excel file and exporting data to CSV.
"""
import os

import xlsxwriter
from google_images_search import GoogleImagesSearch
from revChatGPT.V1 import Chatbot

from .prompts import ner_dict

gis = GoogleImagesSearch(
    "AIzaSyCgVG5k4HEGT80flFDUDov4Q0UKNi1lTNc", "13654d507ac2445e2"
)


def write_excel(data):
    """
    Writes data to an Excel file. This is a helper function for : func : ` get_excel `.

    @param data - A list of lists where each list is a row
    """
    # Create a new Excel file
    workbook = xlsxwriter.Workbook("data.xlsx")
    # Add a new worksheet to the Excel file
    worksheet = workbook.add_worksheet()

    # Write the data to the worksheet
    for row_num, row_data in enumerate(data):
        for col_num, col_data in enumerate(row_data):
            # Check if the third column is a link
            if col_num == 2 and "http" in col_data:
                worksheet.write_url(row_num, col_num, col_data)
            else:
                worksheet.write(row_num, col_num, col_data)

    # Close the Excel file
    workbook.close()


def export_to_csv(data):
    """
    Export data to CSV. This is a helper function for : func : ` write_excel `.

    @param data - List of data to export. Each item is a 2 - tuple ( name tag
    """
    new_data = []
    # Add a search query to the data.
    for item in data:
        name, tag = item[0], item[1][0]
        temp = (
            name,
            tag,
            f"https://www.bing.com/search?q={name.replace(' ', '+')}",
        )
        new_data.append(temp)
    write_excel(new_data)


def get_images(name):
    """
    Queries Google Images for images of the entity.

    @param name - Name of the entity to search for

    @return The URL of the first image result
    """
    _search_params = {
        "num": 1,
        "fileType": "jpg|png",
        "rights": "cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived",
        "q": name,
    }

    gis.search(search_params=_search_params, width=400)
    img_url = gis.results()[0].url

    return img_url


def prompt_gpt(name, ner):
    """
    Prompts ChatGPT for a summary given the name and NER tag.

    @param name - Name of the person to check
    @param ner - NER of the person to check

    @return The response from ChatGPT
    """
    prompt = ner_dict[ner] + name
    chatbot = Chatbot(
        config={
            "email": os.getenv("GPT_API_KEY"),
        }
    )

    response = ""

    # ask for a prompt and return the message
    for data in chatbot.ask(prompt):
        response = data["message"]

    return response


def get_response(name, ner):
    """
    Returns response for name and NER.

    @param name - Name of the person to check
    @param ner - NER of the person to check

    @return A dictionary of response information to send to the test_server. py for the name and NER
    """

    img_url = get_images(name)
    response = prompt_gpt(name, ner)
    return response, img_url
