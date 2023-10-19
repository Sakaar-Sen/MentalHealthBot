# MentalHealthBot
An AI-powered mental health chatbot created using the LangChain framework.

## Features

- Utilizes Retrieval Augmented Generation (RAG) with the [Mistral AI 7B Model](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1) to generate long and helpful responses to user input.
- Leverages a collection of [case studies](https://huggingface.co/datasets/Amod/mental_health_counseling_conversations) of previous patients and appropriate responses to provide more relevant answers, improving the quality of interactions.
- Maintains a chat history, allowing users and the AI therapist to refer back to previous interactions, ensuring a coherent and continuous conversation experience.


## Homepage
![image](https://github.com/Sakaar-Sen/MentalHealthBot/assets/52592149/7884fb5c-0e02-4064-b49c-c5eb9449abc9)


## Examples
The prompt examples below were taken from reddit and not included in the case studies dataset. 
![image](https://github.com/Sakaar-Sen/MentalHealthBot/assets/52592149/c093bf5b-8b12-43df-81cd-0a9270ee8887)
![image](https://github.com/Sakaar-Sen/MentalHealthBot/assets/52592149/9e006820-3254-4990-8ae2-fa23a60db9ae)


## Usage

To use the Mental Health Assistant, follow these steps:

1. Clone the repository: `git clone https://github.com/Sakaar-Sen/MentalHealthBot`

2. Install the required libraries: `pip install -r requirements.txt`

3. Start the chainlit app with `chainlit run app.py` 


# Contributing
Contributions to improve the chatbots's performance, add new features, or fix any issues are welcomed. 


