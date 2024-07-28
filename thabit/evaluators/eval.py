from thabit.evaluators.by_words import (
    contains_words,
    contains_no_words,
    contains_words,
    contains_all_words,
)
from thabit.evaluators.similarity import similarity
from thabit.evaluators.exact import exact_match


def evaluate_output(output, expected_output, evaluation_method, threshold=80):
    """
    Evaluate the output based on the evaluation method
    """
    if evaluation_method.strip() == "exact":
        return exact_match(output, expected_output)
    elif evaluation_method.strip() == "contains_words":
        return contains_words(output, expected_output)
    elif evaluation_method.strip() == "contains_all_words":
        return contains_all_words(output, expected_output)
    elif evaluation_method.strip() == "similarity":
        return similarity(output, expected_output, threshold)
    elif evaluation_method.strip() == "contains_no_words":
        return contains_no_words(output, expected_output)
    return False
