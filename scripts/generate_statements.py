from datetime import date
import re
import os
import sys

import yaml


MARKDOWN_LINK = re.compile(r"\[([^\]]+)\]\(#([^\)]+)\)")


def make_statement(title, statement_id):
    return {
        "summary": title,
        "id": statement_id,
        "status": "not_implemented",
        "last_update": date.today().isoformat(),
    }

def get_statements(markdown):
    links = MARKDOWN_LINK.findall(markdown)
    statements = [make_statement(title, link_id) for title, link_id in links]
    return yaml.safe_dump(
        statements,
        explicit_start=False,
        explicit_end=False,
        allow_unicode=True,
        default_flow_style=False
    )

def main(filename):
    dummy_file = filename + '.bak'
    with open(filename, "r") as f:
        content = f.read()
        f.seek(0) # go back to the beginning of the file
        lines = f.readlines() # read old content

    markdown = content.split('---\n')[-1]
    statements = get_statements(markdown)
    with open(dummy_file, 'w') as write_obj:
        for i in range(0,5):
            write_obj.write(lines.pop(0)) # write new content at the beginning
        write_obj.write("statements: \n") # write new content at the beginning
        write_obj.write(statements) # write new content at the beginning
        for line in lines: # write old content after new
            write_obj.write(line)

    os.remove(filename)
    # Rename dummy file as the original file
    os.rename(dummy_file, filename)


if __name__ == "__main__":
    main(*sys.argv[1:])
