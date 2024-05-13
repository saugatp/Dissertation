import csv
from google_play_scraper import Sort, reviews

firstTime = True  # Initialize as True

# This is the code used to scrape google play store reviews data for my dissertation
# This code was used during the data collection part
def fetch_and_save_reviews(app_id, token_c=None):
    global firstTime  # Declare as global to modify outside value
    # Fetch reviews
    if token_c is None:
        result, token = reviews(
            app_id,
            sort=Sort.MOST_RELEVANT,
            count=100,
            lang='en',
            country='us',
            continuation_token=None
        )
    else:
        result, token = reviews(
            app_id,
            continuation_token=token_c
        )

    # Write reviews to CSV
    csv_filename = f"reviews_duo.csv"
    with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:  # Use 'a' mode to append to existing file
        writer = csv.writer(csvfile)
        if firstTime:
            writer.writerow(["Content", "Date", "Rating"])
            firstTime = False
        for review in result:
            content = review['content']
            date = review['at']
            rating = review['score']
            writer.writerow([content, date, rating])

    print(f"Fetched and saved {len(result)} reviews to {csv_filename}")
    return token

# Start fetching reviews from selected app id
app_id = 'com.duolingo'
next_token = None

while True:
    next_token = fetch_and_save_reviews(app_id, next_token)
    if not next_token:
        break

print('All reviews fetched and saved to reviews_insta.csv.')
