def has_all_words(output, words):
    """
    This function evaluates if the output contains all the words in the expected_output.
    """
    return all(word in output for word in words.split())


def has_some_words(output, words):
    """
    This function evaluates if the output contains some of the words in the expected_output.
    """
    return any(word in output for word in words.split())


def has_no_words(output, words):
    """
    This function evaluates if the output contains none of the words in the expected_output.
    """
    if output == "" or len(words) == 0:
        return False
    return not any(word in output for word in words.split())
