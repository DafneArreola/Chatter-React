import csv
from faker import Faker
import random
import time
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Constants
NUM_ENTRIES = 350
USER_ID = 1
MEDIA_ID = 2

# Generate a random timestamp within the last year
def generate_random_timestamp():
    randomness = random.randint(0, 133)
    return int(randomness*1000)

# Generate random comments
def generate_comment_data(num_entries):
    comments = []
    for _ in range(num_entries):
        comment = {
            'user_id': USER_ID,
            'media_id': MEDIA_ID,
            'timestamp': generate_random_timestamp(),  # Random timestamp
            'text': fake.text(max_nb_chars=200),  # Random text up to 200 characters
            'season_number': '',  # Empty value
            'episode_number': ''  # Empty value
        }
        comments.append(comment)
    return comments

# Write comments to CSV
def write_comments_to_csv(filename, comments):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['user_id', 'media_id', 'timestamp', 'text', 'season_number', 'episode_number']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for comment in comments:
            writer.writerow(comment)

if __name__ == '__main__':
    comments = generate_comment_data(NUM_ENTRIES)
    write_comments_to_csv('comments.csv', comments)