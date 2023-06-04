# [NER-app](ner-app-wiki.azurewebsites.net)
An app that takes a pdf file (via a button), parses various entities, such as people, locations, or events, and gives you back a list of said entities with their tags.
You also have a link for a bing search (which should preferably be used with the chat function), or you can click the result and you get back a 5 sentence summary of said
entity via the power of ChatGPT 3.5

## Techstack
* Flask
* Bootstrap
* Kaggle (for faster inference)
