from revChatGPT.V1 import Chatbot
from google_images_search import GoogleImagesSearch
import xlsxwriter
import os

gis = GoogleImagesSearch(
    'AIzaSyCgVG5k4HEGT80flFDUDov4Q0UKNi1lTNc', '13654d507ac2445e2')


def write_excel(data):

    # Create a new Excel file
    workbook = xlsxwriter.Workbook('data.xlsx')
    # Add a new worksheet to the Excel file
    worksheet = workbook.add_worksheet()

    # Write the data to the worksheet
    for row_num, row_data in enumerate(data):
        for col_num, col_data in enumerate(row_data):
            # Check if the third column is a link
            if col_num == 2 and 'http' in col_data:
                worksheet.write_url(row_num, col_num, col_data)
            else:
                worksheet.write(row_num, col_num, col_data)

    # Close the Excel file
    workbook.close()


def export_to_csv(data):
    new_data = []
    for item in data:
        name, tag = item[0], item[1][0]
        temp = (
            name, tag, f"https://www.bing.com/search?q={name.replace(' ', '+')}")
        new_data.append(temp)
    write_excel(new_data)


def get_response(name, ner):
    _search_params = {
        'q': '...',
        'num': 1,
        'fileType': 'jpg|png',
        'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived',
    }
    ner_dict = {
        "PERSON": "You are an expert people explainer. You can explain people of today or from history in an information dense format, while keeping the main points of their character intact. Describe this person in 5 sentences: ",
        "NATIONAL/RELIGIOUS/POLITICAL GROUP": "You are a specialist in national, religious and political groups. You focus on information dense sumaries of these various groups in just a few sentences, so that people know exactly what this group is all about. Now describe this national/religious/political group in 5 sentences: ",
        "ARCHITECTURE": "You are an architect, who can perfectly explain any building, it's history, usage and architecture. You provide these information dense summaries so that it can be understood by a layman. Describe this building in 5 sentences: ",
        "ORGANIZATION": "You are an expert at explaining the main information about various organizations, of now or in history. You provide the most crucial information in such as their motives, their rise to power or decline from power, their country of origin and their size. Describe this organization in 5 sentences: ",
        "GEOPOLITICAL ENTITY": "You are an expert at explaining the main information about geopolitical entities, of now or in history. You provide the most crucial information in a dense format, so that the respondent knows the bascis of said entity. Describe this geopolitical entity in 5 sentences: ",
        "LOCATION": "You are an explorer, and know every location of the world intimately. You are able to give a vivid image of said location just using text, while also sprinkling in some details, such as where is it located. Describe this location in 5 sentences:",
        "PRODUCT": "You are a product expert, who can flawlessly describe any product in just a few sentences, while also providing a reason why anyone would use it. Describe this product in 5 sentences: ",
        "EVENT": "You are a historian, an expert at describing events, why they happened, how they got resolved, and what happened in between. You provide these information in a dense format so that a layman can perfectly understand what you have said. Explain this event in 5 sentences: ",
        "WORK_OF_ART": "You are to act as an IP EXPERT, you can describe the origins of any artwork or intelectuall property - books, games, art, songs etc. You describe who they were created by, summarize said creator and then describe the piece of art in easily understandable words. Describe this work of art in 5 sentences:",
        "LAW": "You are an excellent lawyer, who can easily explain any law to the public in just a few sentences so that a layman can undestand it without a problem, while not ommiting where details about the law could be found. Explain this law in 5 sentences: ",
        "LANGUAGE": "You are an etymologist who can explain where a language came from, how many people speak it today, and the history behind it in just a few sentences. Describe this language in 5 sentences: "
    }
    _search_params['q'] = name
    prompt = ner_dict[ner] + name

    gis.search(search_params=_search_params, width=400)
    img_url = gis.results()[0].url
    print(img_url)

    chatbot = Chatbot(config={
        "email": os.getenv("GPT_API_KEY"),
    })

    response = ""

    for data in chatbot.ask(
        prompt
    ):
        response = data["message"]

    print(response)
    return response, img_url
