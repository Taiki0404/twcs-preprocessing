COLUMNS_TO_USE_IN_META_TABLE = ["tweet_id", "author_id", "inbound", "created_at"]
COLUMNS_TO_USE_IN_TEXT_TABLE = ["tweet_id", "text"]
COLUMNS_TO_USE_IN_PAIR_TABLE = ["tweet_id", "response_tweet_id", "in_response_to_tweet_id"]

META_TABLE_COLUMNS = ["tweet_id", "author_id", "inbound", "created_at"]
TEXT_TABLE_COLUMNS = ["tweet_id", "processed_text"]
PAIR_TABLE_COLUMNS = ["utterance", "response", "dialog_id"]
