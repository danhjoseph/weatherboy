import os
import tweepy
import requests
from dotenv import load_dotenv


def main():
    load_dotenv()

    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    access_token = os.getenv('ACCESS_TOKEN')
    access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    twit_handle = "@heyweatherboy"
    query = api.mentions_timeline()
    result = query[0].text.strip("@heyweatherboy ")
    number_of_tweets = 1

    response = requests.get(
        "https://api.weatherapi.com/v1/current.json?key=032e7d2533b0484e8ac175455221106&q="+result+"&aqi=no").json()

    temp = response["current"]["temp_f"]
    condition = response["current"]["condition"]["text"]

    tweetback = ("It's currently " + str(temp) +
                 " degrees & " + condition + " in " + result)

    for tweet in tweepy.Cursor(api.search_tweets, twit_handle).items(number_of_tweets):
        try:
            tweetId = tweet.user.id
            username = tweet.user.screen_name
            api.update_status("@" + username + " " + tweetback,
                              in_reply_to_status_id=tweetId)
            print("Tweeted back " + tweetback)
        except tweepy.errors.TweepyException as e:
            print(e.reason)
        except StopIteration:
            break


if __name__ == '__main__':
    main()
