import string

DEFAULT_STOPWORDS = {"the", "is", "and", "a", "an", "of", "to", "in", "uses", "are", "for", "on", "with", "as", "it", "this"}

def calculate_grounding_metrics(context_text: str, answer_text: str, stopwords: set = None):
    """
    Calculates word-overlap Faithfulness (No Hallucination) and Answer Relevance scores.
    """
    if stopwords is None:
        stopwords = DEFAULT_STOPWORDS

    clean_context = context_text.lower().translate(str.maketrans("", "", string.punctuation))
    clean_answer = answer_text.lower().translate(str.maketrans("", "", string.punctuation))

    context_words = set(w for w in clean_context.split() if w not in stopwords)
    answer_words = set(w for w in clean_answer.split() if w not in stopwords)

    overlap = context_words.intersection(answer_words)
    faithfulness = len(overlap) / max(len(answer_words), 1)
    relevance = len(overlap) / max(len(context_words), 1)

    return faithfulness, relevance
