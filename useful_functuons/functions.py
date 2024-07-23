
def replacer_escaped_symbols(sentences: tuple | dict | str | list) -> str:
    """the function adds '\' in front of symbols of must_to_be_escaped list if the item of must_be_escaped is
    in the sentence the function gets"""
    def replacing(sentence: str) -> str:
        must_be_escaped = [".", "!", "(", ")", "-", "_", "[", "]"]
        for symbol in must_be_escaped:
            replace = fr"\{symbol}"
            sentence = sentence.replace(symbol, replace)
        return sentence

    for item in sentences:
        item_index = sentences.index(item)
        replaced = replacing(item)
        sentences.remove(item)
        sentences.insert(item_index, replaced)
    return sentences
