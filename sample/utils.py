from hashlib import md5


def encryption(chars):
    return str.upper(md5(chars.encode("utf8")).hexdigest()[:6])

