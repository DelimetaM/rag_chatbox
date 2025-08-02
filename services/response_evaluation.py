import re

def compute_quality_score(question: str, answer: str) -> float:
    """
    Llogarit cilësinë e përgjigjes bazuar në mbivendosjen e fjalëve (token overlap)
    midis pyetjes dhe përgjigjes. Jep një rezultat nga 0.0 në 1.0.

    :param question: Pyetja e përdoruesit
    :param answer: Përgjigja e gjeneruar
    :return: quality_score si float me 2 shifra dhjetore
    """

    def tokenize(text):
        # Heq shenjat e pikësimit dhe e kthen tekstin në fjalë të vogla
        text = re.sub(r'[^\w\s]', '', text.lower())
        return set(text.split())

    # Krijon fjalët unike për pyetjen dhe përgjigjen
    q_tokens = tokenize(question)
    a_tokens = tokenize(answer)

    if not q_tokens:
        return 0.0

    # Llogarit fjalët e përbashkëta
    overlap = q_tokens.intersection(a_tokens)
    score = len(overlap) / len(q_tokens)

    return round(score, 2)