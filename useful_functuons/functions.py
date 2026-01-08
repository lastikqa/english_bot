
def replacer_escaped_symbols(sentences: tuple | dict | str | list) -> str| list:
    """the function adds '\' in front of symbols of must_to_be_escaped list if the item of must_be_escaped is
    in the sentence the function gets"""
    def replacing(sentence: str) -> str:
        must_be_escaped = [".", "!", "(", ")", "-", "_", "[", "]"]
        for symbol in must_be_escaped:
            replace = fr"\{symbol}"
            sentence = sentence.replace(symbol, replace)
        return sentence
    
    if type(sentences) in (list, tuple):
        new_list = []
        for item in sentences:
            item = replacing(item)
            new_list.append(item)
        return new_list

    return replacing(str(sentences))





