class RegexPatterns:
    URL = r"https?://(?:www\.)?[^\s/$.?#].[^\s]*"
    PARENTHESES_WITH_TEXT = r"\(.*?\)"
    MENTIONS = r"@\w+"
    TAGS = r"#\w+"
    PAGE_NOTATION = r"\d+/\d+"
    SYMBOLS = r"[\"#$%&()*+-/:;<=>@[\]^_`{|}~�©®™]"
