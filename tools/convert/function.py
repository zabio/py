def insert(old_text, text, index):
    if index == 0:
        new_text = text + old_text
    elif index == -1:
        new_text = old_text + text
    else:
        new_text = old_text[: index] + text + old_text[index:]
    return new_text


def replace(old_text, old_str, new_str):
    new_text = old_text.replace(old_str, new_str)
    return new_text


def replace2(old_text, new_str, start, end):
    new_text = old_text[:start] + new_str + old_text[end:]
    return new_text


def delete(old_text, text):
    return old_text.replace(text, "")


def delete2(old_text, start, end):
    new_text = old_text[:start] + old_text[end + 1:]
    return new_text
