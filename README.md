# Conference Recommendation System

## Problem Understanding
We understand the conference recommendation for paper drafts as a text classification problem. In this classification problem, we have data consisting of previously published paper texts (data) and the conferences they were published in (labels). We assume that all papers were submitted to the most suitable conference.

## Task
Our goal is to process the drafts of papers using natural language processing, where the text serves as input, and obtain the output of one or multiple labels. This task can be divided into the following two parts: training and optimization of the classification model, and acquisition of the dataset.

## Classification Model

### TextCNN

Script for training a text classification model using convolutional neural networks (CNN) on textual data. It leverages PyTorch for deep learning and provides a flexible structure for training and evaluating text classification models.

### BERT

Train a text classification model based on the BERT architecture for a Chinese text classification task. It demonstrates how to preprocess data, create custom datasets, build a model, and perform training and evaluation using PyTorch and the Hugging Face Transformers library.

## Data Acquisition

### Conference_list
The main purpose of this program is to extract conference names from an Excel file, check their validity (by accessing a specific URL), and write the valid conference names to a text file. Invalid conference names are printed for user review. This is useful for processing a large number of conference names and filtering out the valid ones.

### Paper_list
This code defines a crawler that retrieves data from the DBLP database, handles both default and backup URLs, and saves the retrieved data in CSV files. It also logs invalid combinations of A and B. The main section demonstrates how to use this crawler to retrieve data for a specific range of years and a list of A values.

### Abstract_crwaler
This code is designed to take a folder containing CSV files with conference paper titles, search for the corresponding paper abstracts on ArXiv, and save the results in new CSV files with abstracts. It uses multiprocessing to speed up the process by parallelizing the searches for different titles.

## Todo
### Recommedation system
1. In the conference recommendation system, the state of the art currently analyzes only keywords and abstracts. We will enhance the analysis by including full-text content.
2. We can enhance author network identification by considering the conferences the author has previously submitted to, assisting in recommending suitable conferences.

### Web crawler
1. Due to access limitations on dblp and arXiv, we will add crawler proxies to bypass IP bans.
2. We will further expand the dataset, which currently includes abstracts from around 20,000 articles from 37 conferences in the CS field from 2020 to 2022. This expansion will encompass more conferences and cover a longer time span.