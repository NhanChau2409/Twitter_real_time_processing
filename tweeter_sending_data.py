import tweepy
import socket
from apikey import *             # Import authenticated key from private file

# Twitter authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

# Create inheritance class for retrieve stream data
class TweetListener(tweepy.StreamingClient):
    
    # Set socket to put data in
    def __init__(self, custom_socket: socket.socket) -> None:
        super().__init__(bearer_token= bearer_token)
        self.client_socket = custom_socket
        
    # Override on_data method
    def on_data(self, data) -> bool:
        try:
            print(f'Message text: {data}')
            self.client_socket.send(data)
            return True
        except BaseException as e:
            print(f'Error: {e}')
        return True

def send_tweets(custom_socket: socket.socket):    
    twitter_stream = TweetListener(custom_socket)
    rule = tweepy.StreamRule(value='#worldcup')
    twitter_stream.add_rules(rule)
    
    # Trigger sending tweet 
    twitter_stream.filter(tweet_fields=['text'])

if __name__ == "__main__":
    
    # Create our custom socket
    custom_socket = socket.socket()
    host = "127.0.0.1"                      # local machine address
    port = 5555                             # specify random port  
    custom_socket.bind((host, port))        # binding them together

    # Start connection
    custom_socket.listen(5)
    client, address = custom_socket.accept() 
    
    # Start sending stream data
    send_tweets(client)
            
    