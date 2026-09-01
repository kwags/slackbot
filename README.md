# MNRD Slackbot

A Python-based Slackbot built to help members of the Minnesota Roller Derby (MNRD) community quickly find information about league policies, bylaws, leave policies, and other organizational documentation.

The bot runs as a serverless application using **AWS Lambda** and responds to questions and requests submitted through Slack.

## Features

* Searches organizational documentation to provide relevant answers to Slack users
* Uses an FAQ system for frequently asked questions
* Supports exact, keyword, and fuzzy matching for improved question recognition
* Uses **TF-IDF** and cosine similarity to identify relevant sections of organizational documents when an FAQ match isn't found
* Includes configurable similarity thresholds to reduce incorrect or unrelated responses
* Handles multiple Slack workspaces
* Logs application activity for troubleshooting and monitoring

## Technologies

* **Python**
* **AWS Lambda**
* **AWS API Gateway**
* **AWS SAM (Serverless Application Model)**
* **Slack API**
* **scikit-learn**
* **TF-IDF / cosine similarity**

## Project Structure

```text
slackbot/
├── mnrd_slackbot/       # Main application code
├── events/              # Sample/test invocation events
├── tests/               # Unit and integration tests
├── template.yaml        # AWS SAM infrastructure configuration
├── requirements.txt     # Python dependencies
└── README.md
```


## How It Works

When a user sends a question to the Slackbot, the application processes the message and attempts to find the most appropriate response first looking at a predefined FAQ list, then searching organizational documents.

The matching process uses several levels of matching, including:

1. Exact and keyword matching
2. Keyword matching
3. Fuzzy matching
4. TF-IDF similarity matching against organizational documents

If the similarity score does not meet the threshold, the bot will return no match rather than providing a potentially incorrect answer.

## Local Development

Create and activate a Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

The application can be built and tested using the AWS SAM CLI:

```bash
sam build --use-container
```

## Deployment

This project uses AWS SAM for deployment.

```bash
sam build --use-container
sam deploy --guided
```

The deployment configuration and AWS resources are defined in `template.yaml`.

## Configuration

Secrets and environment-specific configuration should be stored in environment variables or AWS configuration rather than committed to the repository.

**Do not commit API keys, Slack tokens, AWS credentials, or other secrets to Git.**

## Background

This project was developed as a way to automate answers and access to organizational information through Slack. Development included designing the question-matching system, organizing source documentation, improving matching accuracy, and implementing safeguards against unrelated or incorrect responses.
