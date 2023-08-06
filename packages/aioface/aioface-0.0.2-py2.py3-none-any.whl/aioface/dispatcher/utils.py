def check_full_text(fb_full_text, filter_full_text) -> bool:
    if filter_full_text is None or fb_full_text == filter_full_text:
        return True
    return False


def check_contains(fb_contains, filter_contains) -> bool:
    if filter_contains is None:
        return True
    intersection = list(fb_contains & filter_contains)
    if len(intersection) == 0:
        return False
    return True


def check_payload(fb_payload, filter_payload) -> bool:
    if filter_payload is None or fb_payload == filter_payload:
        return True
    return False
