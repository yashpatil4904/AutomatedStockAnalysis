import time
import random
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ✅ Stock tickers to search for (Cashtags)
stock_tickers = ["RCAT", "DKNG", "INDI", "WRBY", "HIMS", "PDD", "ARDX", "LYFT", "TMDX", "ELF"]

# ✅ Chrome Options
options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--incognito")
options.add_argument("--start-maximized")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--log-level=3")

# ✅ Random User-Agent to avoid detection
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
]
options.add_argument(f"user-agent={random.choice(user_agents)}")

# ✅ Start Chrome
driver = uc.Chrome(options=options)

try:
    # 🚨 Manually log in first
    driver.get("https://twitter.com/login")
    input("🚨 Log in to Twitter manually, then press ENTER to continue...")

    tweets_data = []

    # ✅ Loop through each stock ticker
    for ticker in stock_tickers:
        print(f"🔍 Searching for: {ticker}")
        driver.get(f"https://twitter.com/search?q=%24{ticker}&src=typed_query")  # **Uses $TICKER for stocks**

        time.sleep(random.uniform(8, 12))  # Initial wait before scraping

        collected_tweets = set()
        max_scrolls = 500  # Allow more scrolling to capture tweets
        min_tweets_required = 500  # **Ensuring at least 500 tweets per stock**
        retries = 5  # **Retry up to 5 times if needed**

        while len(collected_tweets) < min_tweets_required and retries > 0:
            initial_count = len(collected_tweets)

            for _ in range(max_scrolls):
                try:
                    # ✅ Wait for tweets to load
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH, '//article//div[@data-testid="tweetText"]'))
                    )

                    # ✅ Get fresh list of tweets each time
                    tweets = driver.find_elements(By.XPATH, '//article//div[@data-testid="tweetText"]')

                    for tweet in tweets:
                        try:
                            tweet_text = tweet.text.strip()
                            if tweet_text and tweet_text not in collected_tweets and f"${ticker}" in tweet_text:
                                collected_tweets.add(tweet_text)
                        except:
                            continue  # If element becomes stale, ignore it

                    # ✅ Stop if 500+ tweets are collected
                    if len(collected_tweets) >= min_tweets_required:
                        break

                    # ✅ Randomized scrolling (70-95% of page height)
                    scroll_range = random.uniform(0.7, 0.95)
                    driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {scroll_range});")
                    time.sleep(random.uniform(6, 10))  # **Reduced scroll speed to mimic human behavior**

                except Exception as e:
                    print(f"⚠️ Error while scrolling for {ticker}: {e}")
                    break

            # ✅ If no new tweets were added, retry search after delay
            if len(collected_tweets) == initial_count:
                print(f"🔄 Retrying {ticker} in 20 seconds...")
                time.sleep(20)
                retries -= 1
            else:
                break  # Stop retrying if new tweets were found

        # ✅ Store collected tweets
        for tweet in collected_tweets:
            tweets_data.append({
                "Stock": ticker,
                "Tweet": tweet,
                "Date": time.strftime("%Y-%m-%d")
            })

        print(f"✅ Collected {len(collected_tweets)} tweets for {ticker}")

        # ✅ Avoid detection: Random wait before next stock search
        time.sleep(random.uniform(20, 40))

    # ✅ Save to CSV
    csv_filename = f"stock_tweets.csv"
    df = pd.DataFrame(tweets_data)
    df.to_csv(csv_filename, index=False, encoding='utf-8')
    print(f"✅ Scraping complete! Data saved to {csv_filename}")

except Exception as e:
    print(f"⚠️ Error encountered: {e}")

finally:
    # ✅ Ensure browser closes properly
    if driver:
        driver.quit()
    print("🔴 Browser closed.")
