columns = {
    "to_use_in_seq_table": ["tweet_id", "response_tweet_id", "in_response_to_tweet_id"],
    "for_tweet_meta_table": ["tweet_id", "author_id", "inbound", "created_at"],
    "for_dialog_meta_table": ["dialog_id", "supporter"],
    "for_text_table": ["tweet_id", "processed_text"],
    "for_seq_table": ["utterance_id", "sequence", "dialog_id"],
}
