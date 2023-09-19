import re
import openpyxl
import requests

class ConferenceNameProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.conference_names = []

    def load_conference_names(self):
        # Open the Excel file
        workbook = openpyxl.load_workbook(self.file_path)

        # Select the worksheet to read
        sheet = workbook.active

        # Iterate through each row and extract the string part
        for row in sheet.iter_rows(min_row=2, values_only=True):  # Start reading from the 2nd row, skipping the header row
            if row[0]:  # Ensure the cell is not empty
                # Use regular expression to extract the string part, remove leading "IEEE" or "ACM," and convert to lowercase
                match = re.match(r'^(?:IEEE|ACM)?\s*(.*?)\s*\d*$', row[0], re.IGNORECASE)
                if match:
                    conference_name = match.group(1).lower()
                    self.conference_names.append(conference_name)

        # Close the Excel file
        workbook.close()

    def process_and_output(self):
        # Print elements corresponding to invalid URLs
        invalid_elements = []

        for name in self.conference_names:
            url = f"https://dblp.uni-trier.de/db/conf/{name}/index.html"
            response = requests.head(url)

            if response.status_code != 200:
                invalid_elements.append(name)

        # Print elements corresponding to invalid URLs
        print("Elements corresponding to invalid URLs:")
        for element in invalid_elements:
            print(element)

        # Write elements corresponding to valid URLs to conference_names.txt
        valid_elements = [name for name in self.conference_names if name not in invalid_elements]
        with open("conference_names.txt", "w", encoding="utf-8") as output_file:
            output_file.write(", ".join(valid_elements))

        print("Elements corresponding to valid URLs have been written to conference_names.txt.")

# Create an instance of ConferenceNameProcessor and call the respective methods
processor = ConferenceNameProcessor("ccf_conference_list.xlsx")
processor.load_conference_names()
processor.process_and_output()
