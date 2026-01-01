KEYWORDS = [
    "कीर्ति चक्र", "शौर्य", "वीरगति",
    "मरणोपरांत", "बलिदान", "आतंक"
]

def is_bravery_story(text):
    return any(k in text for k in KEYWORDS)