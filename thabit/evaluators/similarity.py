from fuzzywuzzy import fuzz


def similarity(output, expected_output, threshold=80):
    """
    This function evaluates the similarity between two strings using the
    fuzzywuzzy library's token_sort_ratio method. It compares the output
    generated by the AI model with the expected output and determines
    if they are similar based on a specified threshold.

    Parameters:
        output (str): The output string generated by the AI model.
        expected_output (str): The expected output string for comparison.
        threshold (int, optional): The minimum similarity score (0-100)
                                    required for a positive match. Default is 80.

    Returns:
        bool: True if the similarity score is greater than or equal to
            the threshold, False otherwise.
    """
    similarity = fuzz.token_sort_ratio(output, expected_output)
    return similarity >= threshold