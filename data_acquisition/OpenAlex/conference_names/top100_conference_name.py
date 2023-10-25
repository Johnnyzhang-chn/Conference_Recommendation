import pandas as pd
import re
import os

class ConferenceDataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_values(self, text):
        pattern = r'\[(.*?)\](.*)'
        match = re.match(pattern, text)
        if match:
            return match.groups()
        else:
            return text, text

    def process_data(self):
        df = pd.read_excel(self.file_path)
        df['X'], df['Y'] = zip(*df['Conference'].apply(lambda x: self.extract_values(x)))

        # Extract content within "[]" into a list
        conference_names = [x.lower() for x in df['X']]

        # Write the content into conference_names.txt file, separated by commas and spaces
        with open('conference_names.txt', 'w', encoding='utf-8') as file:
            file.write(', '.join(conference_names))

        return df

    def save_to_csv(self, df, output_path):
        df.to_csv(output_path, index=False)
        print("Extraction completed and saved to the output.csv file.")

# Example usage
if __name__ == "__main__":
    input_file_path = 'conference_top100.xlsx'
    output_file_path = 'output.csv'
    conference_names_file = 'conference_names.txt'

    processor = ConferenceDataProcessor(input_file_path)
    processed_data = processor.process_data()
    processor.save_to_csv(processed_data, output_file_path)

    # Check if conference_names.txt file exists, if not, create a new file and write the data into it
    if not os.path.exists(conference_names_file):
        with open(conference_names_file, 'w', encoding='utf-8') as file:
            file.write(', '.join(processed_data['X']))
