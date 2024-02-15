import requests
from bs4 import BeautifulSoup
import json
import constants

class RedditScraper:
    def __init__(self, subreddit, keyword):
        self.subreddit = subreddit
        self.keyword = keyword
        self.data = []

    def scrape_data(self, num_results=None):
        url = f"https://www.reddit.com/r/{constants.SUB_REDDIT_NAME}/search?q={constants.CHEESE_NAME}&sort=new&restrict_sr=1"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            submissions = soup.find_all('div')
            
            for submission in submissions:
                print(submission)
                # submission_data = {
                #     "title": submission.find('h3').text.strip(),
                #     "url": submission.find('a', class_='SQnoC3ObvgnGjWt90zD9ZC').get('href'),
                #     "author": submission.find('a', class_='author').text,
                #     "score": submission.find('div', class_='score').text,
                #     "comments": submission.find('span', class_='FHCV02u6Cp2zYL0fhQPsO').text,
                #     "body": submission.find('div', class_='selftext').text.strip(),
                # }
                # self.data.append(submission_data)

                if num_results is not None and len(self.data) >= num_results:
                    break
        else:
            print(f"Error: {response.status_code}")

    def save_to_json(self):
        with open('data.json', 'w') as json_file:
            json.dump(self.data, json_file, indent=2)

if __name__ == "__main__":
    subreddit_name = "YourSubreddit"
    keyword = "paramens"
    num_results = 10  # Set the desired number of results here

    reddit_scraper = RedditScraper(subreddit_name, keyword)
    reddit_scraper.scrape_data(num_results)
    # reddit_scraper.save_to_json()
