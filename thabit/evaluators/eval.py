from thabit.evaluators.by_words import contains_words, has_no_words, contains_words
from thabit.evaluators.similarity import similarity
from thabit.evaluators.exact import exact_match


def evaluate_output(output, expected_output, evaluation_method, threshold=80):
    """
    Evaluate the output based on the evaluation method
    """
    if evaluation_method.strip() == "Exact":
        return exact_match(output, expected_output)
    elif evaluation_method.strip() == "Has word(s)":
        return contains_words(output, expected_output)
    elif evaluation_method.strip() == "Similarity":
        return similarity(output, expected_output, threshold)
    return False
