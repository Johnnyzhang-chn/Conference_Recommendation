import pandas as pd
import re

class ConferenceDataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_values(self, text):
        pattern = r'\[(.*?)\](.*)'  # 以[]作为标志，将[]之内的作为X，将]后面的作为Y
        match = re.match(pattern, text)
        if match:
            return match.groups()  # 返回X和Y的值
        else:
            return text, text  # 如果没有匹配，将原始值同时作为X和Y

    def process_data(self):
        df = pd.read_excel(self.file_path)
        df['X'], df['Y'] = zip(*df['Conference'].apply(lambda x: self.extract_values(x)))
        return df

    def save_to_csv(self, df, output_path):
        df.to_csv(output_path, index=False)
        print("Extraction completed and saved to the output.csv file.")

# Example usage
if __name__ == "__main__":
    input_file_path = 'conference_top100.xlsx'
    output_file_path = 'output.csv'

    processor = ConferenceDataProcessor(input_file_path)
    processed_data = processor.process_data()
    processor.save_to_csv(processed_data, output_file_path)
