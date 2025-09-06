"""
Service for fetching data from Twitter API
"""
import tweepy
from typing import List, Dict, Any, Optional
from app.core.config import settings

class TwitterService:
    def __init__(self):
        self.bearer_token = settings.TWITTER_BEARER_TOKEN
        self.api_key = settings.TWITTER_API_KEY
        self.api_secret = settings.TWITTER_API_SECRET
        self.access_token = settings.TWITTER_ACCESS_TOKEN
        self.access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET
        
        # Initialize Twitter API client
        if self.bearer_token:
            self.client = tweepy.Client(bearer_token=self.bearer_token)
        elif all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
            self.client = tweepy.Client(
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret
            )
        else:
            self.client = None
    
    async def fetch_tweets(
        self, 
        query: str, 
        count: int = 100
    ) -> List[Dict[str, Any]]:
        """Fetch tweets using Twitter API v2"""
        if not self.client:
            raise ValueError("Twitter API credentials not configured")
        
        try:
            # Search for tweets
            tweets = tweepy.Paginator(
                self.client.search_recent_tweets,
                query=query,
                tweet_fields=['created_at', 'author_id', 'public_metrics'],
                max_results=min(count, 100)  # API limit
            ).flatten(limit=count)
            
            # Convert to list of dictionaries
            tweet_data = []
            for tweet in tweets:
                tweet_dict = {
                    "id": tweet.id,
                    "text": tweet.text,
                    "author_id": tweet.author_id,
                    "created_at": tweet.created_at,
                    "public_metrics": tweet.public_metrics
                }
                tweet_data.append(tweet_dict)
            
            return tweet_data
            
        except tweepy.TooManyRequests:
            raise Exception("Twitter API rate limit exceeded")
        except tweepy.Unauthorized:
            raise Exception("Twitter API authentication failed")
        except Exception as e:
            raise Exception(f"Failed to fetch tweets: {str(e)}")
    
    async def fetch_user_tweets(
        self, 
        username: str, 
        count: int = 100
    ) -> List[Dict[str, Any]]:
        """Fetch tweets from a specific user"""
        if not self.client:
            raise ValueError("Twitter API credentials not configured")
        
        try:
            # Get user by username
            user = self.client.get_user(username=username)
            if not user.data:
                raise Exception(f"User {username} not found")
            
            # Get user's tweets
            tweets = tweepy.Paginator(
                self.client.get_users_tweets,
                id=user.data.id,
                tweet_fields=['created_at', 'public_metrics'],
                max_results=min(count, 100)
            ).flatten(limit=count)
            
            # Convert to list of dictionaries
            tweet_data = []
            for tweet in tweets:
                tweet_dict = {
                    "id": tweet.id,
                    "text": tweet.text,
                    "author_id": user.data.id,
                    "created_at": tweet.created_at,
                    "public_metrics": tweet.public_metrics
                }
                tweet_data.append(tweet_dict)
            
            return tweet_data
            
        except tweepy.TooManyRequests:
            raise Exception("Twitter API rate limit exceeded")
        except tweepy.Unauthorized:
            raise Exception("Twitter API authentication failed")
        except Exception as e:
            raise Exception(f"Failed to fetch user tweets: {str(e)}")
