def contains_all_words(output, words):
    """
    This function evaluates if the output contains all the words in the expected_output.
    """
    list_of_words = [word.strip() for word in words.split(",")]
    # remove empty strings
    list_of_words = [word for word in list_of_words if word != ""]
    return all(word in output for word in list_of_words)


def contains_words(output, words):
    """
    This function evaluates if the output contains some of the words in the expected_output.
    """
    if output == "" or len(words) == 0:
        return False
    list_of_words = [word.strip() for word in words.split(",")]
    # remove empty strings
    list_of_words = [word for word in list_of_words if word != ""]
    return any(word in output for word in list_of_words)


def contains_no_words(output, words):
    """
    This function evaluates if the output contains none of the words in the expected_output.
    """
    if output == "" or len(words) == 0:
        return False
    list_of_words = [word.strip() for word in words.split(",")]
    # remove empty strings
    list_of_words = [word for word in list_of_words if word != ""]
    return not any(word in output for word in list_of_words)
