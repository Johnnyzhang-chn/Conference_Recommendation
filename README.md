# Conference_Recommendation

## Conference_list
The main purpose of this program is to extract conference names from an Excel file, check their validity (by accessing a specific URL), and write the valid conference names to a text file. Invalid conference names are printed for user review. This is useful for processing a large number of conference names and filtering out the valid ones.

## Paper_list
This code defines a crawler that retrieves data from the DBLP database, handles both default and backup URLs, and saves the retrieved data in CSV files. It also logs invalid combinations of A and B. The main section demonstrates how to use this crawler to retrieve data for a specific range of years and a list of A values.

## Abstract_crwaler
This code is designed to take a folder containing CSV files with conference paper titles, search for the corresponding paper abstracts on ArXiv, and save the results in new CSV files with abstracts. It uses multiprocessing to speed up the process by parallelizing the searches for different titles.