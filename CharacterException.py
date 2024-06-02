class CharacterException(Exception):
    """
        Wrapper around exception for easier error handling
        flavor_text: the normal error message
        char_num: optional line number argument to specify location of error if applicable

    """

    def __init__(self, flavor_text: str, char_num: int = None):
        if (char_num):
            message = "Error at: " + str(char_num) + " " + flavor_text
        else:
            message = "Error: " + flavor_text
        super().__init__(message)
