def lines(text: str):
    for line in text.splitlines():
        yield line
    yield "\n"


def blocks(file):
    block = ""
    for line in lines(file):
        if line.strip():
            block += line + "\n"
        elif block:
            yield ''.join(block)
            block = ""
