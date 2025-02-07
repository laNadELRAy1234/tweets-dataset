import streamlit as st
import pandas as pd
import requests
import io

# Function to fetch quote tweets

def get_quote_tweets(tweet_id, bearer_token):
    quotes_url = f"https://api.twitter.com/2/tweets/{tweet_id}/quote_tweets"
    
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    
    params = {
        "tweet.fields": "public_metrics",
        "max_results": 100
    }
    
    response = requests.get(quotes_url, headers=headers, params=params)
    print(response)
    return response.json().get('data', [])  # Get the 'data' field or empty list if not found

# Streamlit app
st.title("Tweet Quotes CSV ")
st.write("Remember 1 trial per 15 minutes")
# Input for Tweet ID
tweet_id = st.text_input("Enter the Tweet ID", placeholder="e.g., 1819405100861075526")

# Button to fetch data
if st.button("Collect Quote Tweets"):
    if not tweet_id:
        st.error("Please enter a valid Tweet ID.")
    else:
        try:
            # Replace with your actual Bearer Token
            bearer_token = "AAAAAAAAAAAAAAAAAAAAAPLiyQEAAAAA2krIjdfssyPvUz06%2FKiLj7rxLJM%3DYoNMzfOkBTbp92j3w0rGJcq6oYLMql84xNyZ54D9Ox7YL4jSly"
            
            # Fetch quote tweets
            st.info("Collecting quote tweets...")
            quotes = get_quote_tweets(tweet_id, bearer_token)
            
            if not quotes:
                
                st.warning("No quote tweets found for this Tweet ID.")
            else:
                # Process data into a DataFrame
                data = []
                for tweet in quotes:
                    data.append({
                        'tweet_id': tweet['id'],
                        'text': tweet['text'],
                        'retweet_count': tweet['public_metrics']['retweet_count'],
                        'reply_count': tweet['public_metrics']['reply_count'],
                        'like_count': tweet['public_metrics']['like_count'],
                        'quote_count': tweet['public_metrics']['quote_count'],
                        'impression_count': tweet['public_metrics'].get('impression_count', 0)
                    })
                
                df = pd.DataFrame(data)
                
                # Display the DataFrame in the app
                st.success(f"Collected {len(quotes)} quote tweets!")
                st.write("Preview of Quote Tweets:")
                st.dataframe(df)
                
                # Save the DataFrame to a CSV in-memory
                output = io.BytesIO()
                df.to_csv(output, index=False)
                processed_csv = output.getvalue()
                
                # Provide a download button
                st.download_button(
                    label="Download Quote Tweets as CSV",
                    data=processed_csv,
                    file_name="quote_tweets.csv",
                    mime="text/csv"
                )
        except Exception as e:
            st.error(f"An error occurred: {e}")
