import praw
import json
from constants import CHEESE_NAME, CLIENT_ID, CLIENT_SECRET, USER_AGENT, USER_NAME, PASSWORD, SUB_REDDIT_NAME

class RedditScraper:
    def __init__(self, client_id, client_secret, username, password, user_agent, subreddit_name, keyword):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password
        )
        self.subreddit_name = subreddit_name
        self.keyword = keyword
        self.data = []

    def scrape_data(self, num_results=None):
        subreddit = self.reddit.subreddit(self.subreddit_name)
        submissions = subreddit.search(self.keyword, sort="new", syntax="lucene", time_filter="all")

        for submission in submissions:
            submission_data = {
                "title": submission.title,
                "url": submission.url,
                "author": submission.author.name,
                "score": submission.score,
                "comments": submission.num_comments,
                "body": submission.selftext,
                "author_info": self.get_author_info(submission.author),
            }
            print(submission_data)
            self.data.append(submission_data)

            # Break the loop if the desired number of results is reached
            if num_results is not None and len(self.data) >= num_results:
                break

    def get_author_info(self, author):
        try:
            author_info = self.reddit.get(f"/user/{author.name}/about")
            print(author_info)
            return author_info.name
            
        except praw.exceptions.PRAWException as e:
            print(f"Error while fetching author info: {e}")
            return {}

    def save_to_json(self):
        with open('data.json', 'w') as json_file:
            json.dump(self.data, json_file, indent=2)

if __name__ == "__main__":
    client_id = CLIENT_ID
    client_secret = CLIENT_SECRET
    username = USER_NAME
    password = PASSWORD
    user_agent = USER_AGENT
    subreddit_name = SUB_REDDIT_NAME
    keyword = CHEESE_NAME
    num_results = 10  # Set the desired number of results here

    reddit_scraper = RedditScraper(
        client_id, client_secret, username, password, user_agent, subreddit_name, keyword
    )

    reddit_scraper.scrape_data(num_results)
    reddit_scraper.save_to_json()
