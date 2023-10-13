import arxiv
import os
import multiprocessing
import csv
import re

class ArxivTitleSearch:
    def __init__(self, input_folder, num_processes):
        self.input_folder = input_folder
        self.num_processes = num_processes

    def get_initial_csv_files(self):
        # Get initial csv list
        initial_csv_files = [os.path.join(self.input_folder, file) for file in os.listdir(self.input_folder) if file.endswith('.csv')]
        return initial_csv_files

    def search_and_save(self, csv_file):
        print(f"Processing conference: {csv_file}")

        # Create a process pool
        pool = multiprocessing.Pool(self.num_processes)

        # Read the CSV file and open a new output CSV file
        with open(csv_file, 'r', newline='', encoding='utf-8') as input_csv, \
                open(f"{os.path.splitext(csv_file)[0]}_abstract.csv", 'w', newline='', encoding='utf-8') as output_csv:
            reader = csv.reader(input_csv)
            writer = csv.writer(output_csv)

            # Write the header to the output CSV
            header = next(reader)
            writer.writerow(header + ['summary'])

            # Process each row in the input CSV
            for row in reader:
                # 使用正则表达式过滤括号及其内容
                title = re.sub(r'\([^)]*\)', '', row[header.index('Title')]).strip()

                # Use the process pool to handle query tasks
                summary = pool.apply(self.search_and_save_result, (title,))

                # Write the row with the summary to the output CSV
                writer.writerow(row + [summary])

        # Close the process pool
        pool.close()
        pool.join()

    def search_and_save_result(self, query):
        search = arxiv.Search(
            query=query,
            max_results=1,
            sort_by=arxiv.SortCriterion.Relevance
        )
        print(f'Processing paper: {query}')
        try:
            results = list(search.results())

            if results:
                # Return the summary (if results exist)
                return results[0].summary.replace('\n', ' ')
            else:
                return "No results found"

        except Exception as e:
            print(f"Error processing query: {query}. Error: {str(e)}")
            return "Error"

if __name__ == "__main__":
    folder_path = './data/'  # Replace with the folder path containing CSV files
    arxiv_search = ArxivTitleSearch(input_folder=folder_path, num_processes=32)

    # Get initial csv list
    initial_csv_files = arxiv_search.get_initial_csv_files()

    for csv_file in initial_csv_files:
        arxiv_search.search_and_save(csv_file)
