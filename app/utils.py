def print_first_50_words(text):
    words = text.split()  # Split the string into a list of words
    first_50_words = words[:50]  # Select the first 50 words
    truncated_text = ' '.join(first_50_words)  # Join the first 50 words back into a string
    if len(words) > 50:  # Check if the original text had more than 50 words
        truncated_text += '...'  # Append ellipsis if more than 50 words
    print(truncated_text)
