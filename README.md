# Application for Gathering Human-Chatbot Conversations

This Application serves as a tool for gathering human-chatbot conversations for research purposes. It offers user-friendly functionality and seamless integration with any chatbot. This repository corresponds to the paper titled ["How GPT-3 responds to different publics on climate change and Black Lives Matter: A critical appraisal of equity in conversational AI"](https://arxiv.org/abs/2209.13627).

## Overview

The application is developed using Python and relies on [Streamlit](https://www.streamlit.io/), a framework designed for creating ML and data science applications. We utilize [MongoDB](https://www.mongodb.com/) as the storage solution for the conversations and deploy the application on Streamlit's [sharing platform](https://share.streamlit.io/). This repository provides the application's source code, along with instructions for the setup and deployment process.

## Setup

### Clone the repository

To begin, clone the repository by running the following command:

```bash
git clone https://github.com/Top34051/chat-with-gpt-3.git
```

### Install dependencies

Make sure you have Python 3.7 or above installed. To install the required dependencies, execute the following command:

```bash
pip install -r requirements.txt
```

### MongoDB Setup

The application relies on MongoDB for storing conversations. To set up MongoDB, please follow the instructions [here](https://docs.mongodb.com/manual/installation/). Once MongoDB is set up, proceed with their guidelines to create a database named `survey-data` and a collection named `test`. Afterward, create a directory `.streamlit` and add your MongoDB connection string to the `.streamlit/secrets.toml` file.

### OpenAI API setup for GPT-3 access

To enable response generation using the OpenAI API, you need to set up the API. Refer to the instructions [here](https://beta.openai.com/docs/developer-quickstart/your-api-keys) for the necessary steps. Place your API key in the `secrets.toml` file. Once both MongoDB and the OpenAI API are properly configured, your `secrets.toml` file should resemble the following:

```toml
openai_api_key = <YOUR OPENAI API KEY>
db_endpoint = <YOUR MONGODB CONNECTION STRING>
```

## Deployment

### Local deployment

To run the application locally, execute one of the following commands:

```bash
streamlit run info-blm.py
streamlit run info-climate.py
streamlit run opinion-blm.py
streamlit run opinion-climate.py
```

Each command corresponds to a different survey. The first two commands are for the information-seeking survey, and the last two commands are for the opinion-seeking survey. The first two commands are for the Black Lives Matter topic, and the last two commands are for the climate change topic. The only difference between each files is the description of the survey and the topic of the conversation.

### Streamlit sharing deployment

To deploy the application on Streamlit sharing, follow the instructions [here](https://docs.streamlit.io/en/stable/deploy_streamlit_app.html). Make sure to add your MongoDB connection string and OpenAI API key to the `secrets.toml` file. Once the application is deployed, you can access it through the link provided by Streamlit sharing.

## Analyze Cleaned Data

To analyze the cleaned data, run the following command:

```bash
streamlit run analyze.py
```

The analysis application allows you to download a file that excludes conversations failing to meet the quality criteria. Additionally, it annotates each conversation round with the corresponding round index.

## Citation

If you use this application in your research, please consider citing our paper:

```bibtex
@misc{chen2023gpt3,
    title={How GPT-3 responds to different publics on climate change and Black Lives Matter: A critical appraisal of equity in conversational AI}, 
    author={Kaiping Chen and Anqi Shao and Jirayu Burapacheep and Yixuan Li},
    year={2023},
    eprint={2209.13627},
    archivePrefix={arXiv},
    primaryClass={cs.AI}
}
```