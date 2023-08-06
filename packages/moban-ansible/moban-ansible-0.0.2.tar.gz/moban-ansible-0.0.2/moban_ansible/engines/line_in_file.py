import re

from moban.core.content_processor import ContentProcessor


@ContentProcessor("lineinfile", "Checking", "Checked")
def line_in_file(content: str, options: dict) -> str:
    content = content.decode()
    regexp = options.get("regexp")
    state = options.get("state", "present")

    lines = content.split("\n")

    if state == "present":
        if regexp:
            lines = present(lines, options)
        else:
            # regexp is None or ''
            # append the line to the end
            line = options.get("line")
            if line:
                lines += [line]

    else:
        lines = list(absent(lines, options))

    content = "\n".join(lines)
    return content.encode()


def present(lines, options):
    ensure_line = options.get("line")
    regexp = options["regexp"]

    for line in lines:
        if re.match(regexp, line):
            yield ensure_line
        else:
            yield line


def absent(lines, options):
    regexp = options["regexp"]

    for line in lines:
        if re.match(regexp, line):
            continue

        yield line
