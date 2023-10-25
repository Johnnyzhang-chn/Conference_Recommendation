import requests
import re
import csv
import time

class DBLPCrawler:
    def __init__(self):
        self.base_url_default = "https://dblp.org/search/publ/api?q=venue%3A[A]%3Ayear%3A[B]%3A&h=1000&format=json"
        self.base_url_backup = "https://dblp.org/search/publ/api?q=toc:db/conf/[A]/[A][B].bht:%20access:open:&h=1000&format=json"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    def validate_input(self, A, B):
        return re.match(r'^[a-z]+$', A) and re.match(r'^\d{4}$', B)

    def crawl_data(self, A_list, B_start, B_end):
        not_found_A = []  # Store [A] list for responses that do not contain 'hits' and 'hit'
        for A in A_list:
            for B in range(B_start, B_end + 1):
                B_str = str(B)

                if not self.validate_input(A, B_str):
                    print(f"Invalid input. [A] must be a lowercase letter string, and [B] must be a 4-digit number. Skipping combination: {A}_{B_str}")
                    continue

                # Build the default/backup URL
                url_default = self.base_url_default.replace("[A]", A.upper()).replace("[B]", B_str)
                url_backup = self.base_url_backup.replace("[A]", A).replace("[B]", B_str)

                # Send an HTTP request with default URL
                response = requests.get(url_default, headers=self.headers)

                # Add a 2-second delay between requests
                time.sleep(2)  # Wait for 2 seconds between requests

                # Check the response status code
                if response.status_code == 200:
                    try:
                        # Parse the JSON response
                        data = response.json()

                        # Check if the 'hit' field exists
                        if 'result' in data and 'hits' in data['result'] and 'hit' in data['result']['hits']:
                            # Create a CSV file
                            filename = f"{A}_{B_str}.csv"
                            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                                writer = csv.writer(file)
                                writer.writerow(['Index', 'Label', 'Year', 'Title', 'EE'])  # Write the CSV file header

                                # Iterate through all entries and write them to the CSV file
                                for index, item in enumerate(data['result']['hits']['hit'], start=1):
                                    # Remove the trailing period from the title
                                    title = item['info']['title'].rstrip('.')
                                    ee = item['info']['ee'] if 'ee' in item['info'] else ''
                                    label = A
                                    year = B_str
                                    writer.writerow([index, label, year, title, ee])

                            print(f"Data successfully written to the {filename} file.")
                        else:
                            # Try the backup URL
                            response = requests.get(url_backup, headers=self.headers)

                            if response.status_code == 200:
                                data = response.json()
                                if 'result' in data and 'hits' in data['result'] and 'hit' in data['result']['hits']:
                                    # Create a CSV file
                                    filename = f"{A}_{B_str}.csv"
                                    with open(filename, mode='w', newline='', encoding='utf-8') as file:
                                        writer = csv.writer(file)
                                        writer.writerow(['Index', 'Label', 'Year', 'Title', 'EE'])  # Write the CSV file header

                                        # Iterate through all entries and write them to the CSV file
                                        for index, item in enumerate(data['result']['hits']['hit'], start=1):
                                            # Remove the trailing period from the title
                                            title = item['info']['title'].rstrip('.')
                                            ee = item['info']['ee'] if 'ee' in item['info'] else ''
                                            label = A
                                            year = B_str
                                            writer.writerow([index, label, year, title, ee])

                                    print(f"Data successfully retrieved using the backup URL and written to the {filename} file.")
                            else:
                                print(f"Backup URL request failed. Please check the input and URL. Cannot retrieve combination: {A}_{B_str}")
                                not_found_A.append(A)
                    except Exception as e:
                        print(f"Error while processing the response: {str(e)}. Skipping combination: {A}_{B_str}")
                else:
                    print(f"Request failed. Please check the input and URL. Cannot retrieve combination: {A}_{B_str}")
                    not_found_A.append(A)

        # Write [A] that did not contain 'hits' and 'hit' in the response to not_found_conference.txt file
        with open("not_found_conference.txt", 'w', encoding='utf-8') as not_found_file:
            not_found_file.write(', '.join(not_found_A))
            print(f"[A] from the list that did not contain 'hits' and 'hit' in the response have been written to not_found_conference.txt file.")

    def read_A_list_from_file(self, file_path):
        # Read the [A] list from the conference_names.txt file, where elements are comma-separated
        with open(file_path, 'r', encoding='utf-8') as file:
            A_list = [item.strip() for item in file.read().split(',')]
        return A_list

    def crawl_data_for_years(self, A_list, B_start, B_end):
        self.crawl_data(A_list, B_start, B_end)

if __name__ == "__main__":
    crawler = DBLPCrawler()
    A_list = crawler.read_A_list_from_file("conference_names.txt")  # Read the [A] list from the file
    B_start = 2020
    B_end = 2022
    crawler.crawl_data_for_years(A_list, B_start, B_end)
