import requests
import time


class ConferenceDataFetcher:
    def __init__(self, input_file):
        with open(input_file, 'r') as file:
            self.conference_names = file.read().split(', ')
        self.successful_conferences = []
        self.failed_conferences = []

    def fetch_data(self):
        for conference_name in self.conference_names:
            url = f"https://dblp.org/search/publ/api?q=toc:db/conf/{conference_name}/{conference_name}2022.bht:%20access:open:&h=1000&format=json"
            # url = f'https://dblp.org/search/publ/api?q=venue%3A{conference_name}%3A2022%3A{conference_name}%3A&h=1000&format=json'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200 and self.check_hit(response):
                print(f'Successfully fetched data for conference: {conference_name}')
                self.successful_conferences.append(conference_name)
                # 处理返回的数据（在这里可以添加您的处理逻辑）
            else:
                print(f'Failed to fetch data for conference: {conference_name}')
                self.failed_conferences.append(conference_name)
            time.sleep(2)

    def check_hit(self, response):
        try:
            # Parse the JSON response
            data = response.json()

            # Check if the 'hit' field exists
            if 'result' in data and 'hits' in data['result'] and 'hit' in data['result']['hits']:
                return True
        except Exception as e:
            print(f'Error occurred while checking hit: {e}')
        return False

    def save_to_file(self, successful_output_file, failed_output_file):
        with open(successful_output_file, 'w') as file_A:
            file_A.write(', '.join(self.successful_conferences))
        with open(failed_output_file, 'w') as file_B:
            file_B.write(', '.join(self.failed_conferences))


# 创建ConferenceDataFetcher的实例
data_fetcher = ConferenceDataFetcher('conference_names.txt')

# 获取数据
data_fetcher.fetch_data()

# 保存到文件
data_fetcher.save_to_file('conference_names_A.txt', 'conference_names_B.txt')
