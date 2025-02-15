def split_text_into_slices(text, slice_length=1000):
    """
    Splits the given text into manageable slices of specified length.
    
    Args:
        text (str): The text to be split.
        slice_length (int): The maximum length of each slice.
        
    Returns:
        list: A list of text slices.
    """
    return [text[i:i + slice_length] for i in range(0, len(text), slice_length)]