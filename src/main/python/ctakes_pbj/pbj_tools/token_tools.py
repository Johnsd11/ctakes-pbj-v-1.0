def get_token_index_by_offset(tokens, s_begin):
    i = 0
    for token in tokens:
        if token.begin == s_begin:
            return i
        i += 1
    return -1


def get_token_by_offset(tokens, s_begin):
    for token in tokens:
        if token.begin == s_begin:
            return token
