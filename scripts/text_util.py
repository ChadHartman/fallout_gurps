def remove_whitespace(value):
    value = value.replace("\n", " ")\
        .replace("\r", " ")\
        .replace("\t", " ")

    while True:
        old_len = len(value)
        value = value.replace("  ", " ")
        if old_len == len(value):
            break

    return value.strip()
