
from difflib import get_close_matches

def fuzzy_match(word: str, possibilities: list[str], n: int = 1, cutoff: float = 0.6) -> list[str]:
    """
    Finds the best "n" matches for a "word" from a list of "possibilities".
    """
    return get_close_matches(word, possibilities, n, cutoff)
