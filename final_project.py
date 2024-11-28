# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 15:08:38 2024

@author: sipos_f
"""


from dataclasses import dataclass
import yaml
import markdown
from typing import List


@dataclass
class Source:
    first_name: str
    last_name: str
    title: str
    date: str
    journal: str
    page_range: int
    doi: str
    volume_number: int
    issue_number: int
    date_viewed: str


"""give date in yyyy-mm-dd format"""
"""put titles between quotation marks"""


@dataclass
class Sources:
    source: List[Source]


def load_source(filepath: str) -> Sources:
    with open(filepath, "r") as file:
        data = yaml.safe_load(file)

    sources = [Source(**source) for source in data["source"]]
    return Sources(source=sources)


# last_name, first_name. (date). title. *journal*, *volume_number*(issue_number), page_range. <doi>


def apa7_source(data: Source):

    return (f"{data.last_name}, {data.first_name:.1s}. ({data.date:.4s}). " +
            f"{data.title}. *{data.journal}*, " +
            f"*{data.volume_number}*({data.issue_number}), " +
            f"{data.page_range}. " +
            f"<{data.doi}>")


if __name__ == "__main__":
    sources = load_source("Tigno_2006.txt")
#    print(source)
    for source in sources.source:
        print(apa7_source(source))



















# f = open("citation.txt", "w")
# htmlmarkdown = markdown.markdown(f.write(Source))


def yaml_to_markdown(source: str, citation: str, key_order=None, styles=None,
                     italic_keys=None):
    with open(source, "r") as file:
        yaml_data = yaml.safe_load(file)

    markdown_content = generate_markdown(yaml_data, key_order=key_order,
                                         styles=styles,
                                         italic_keys=italic_keys)

    with open(citation, "w") as file:
        file.write(markdown_content)


def generate_markdown(data, level=1, key_order=None, styles=None,
                      italic_keys=None):
    markdown1 = ""
    styles = styles or {}
    italic_keys = italic_keys or set()
    for key, value in data.items():
        markdown1 += f"{'#' * level}{key}\n\n"
        if isinstance(value, dict):
            markdown1 += generate_markdown(value, level + 1)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    markdown1 += generate_markdown(item, level + 1)
                else:
                    markdown1 += f"{value}\n\n"
    return markdown1
    if isinstance(data, dict):
        keys = key_order if key_order else data.keys()
        for key in keys:
            if key in data:
                # Apply font style to the key if specified
                styled_key = apply_style(key, "italic" if key in italic_keys
                                         else styles.get("key", ""))
                markdown1 += f"{'#' * level} {styled_key}\n\n"

                value = data[key]
                if isinstance(value, dict):
                    # Recurse for nested dictionaries
                    markdown1 += generate_markdown(value, level + 1, key_order,
                                                   styles, italic_keys)
                elif isinstance(value, list):
                    # Handle lists
                    for item in value:
                        if isinstance(item, dict):
                            markdown1 += generate_markdown(item, level + 1,
                                                           key_order, styles,
                                                           italic_keys)
                        else:
                            markdown1 += (f"{apply_style(str(item), )}" +
                                          f"{str(styles.get('list', ''))}\n")
                else:
                    # Add styled value
                    markdown1 += (f"{apply_style(str(value), )}" +
                                  f"{str(styles.get('value', ''))}\n\n")
    return markdown1


def apply_style(text, style):
    """
    Apply a Markdown style to text (bold, italic, monospace, etc.).
    """
    if style == "bold":
        return f"**{text}**"
    elif style == "italic":
        return f"*{text}*"
    elif style == "monospace":
        return f"`{text}`"
    elif style == "bold-italic":
        return f"***{text}***"
    return text


if __name__ == "__main__":
    source = "Tigno_2006.txt"
    citation = "Tigno_2006_cited.md"
    yaml_to_markdown(source, citation)
#    key_order = [first_name, last_name, year, title, page, journal,
#                 volume_number, issue_number, doi, date_viewed]
    styles = {
        "key": "bold",      # Keys will be bold
        "value": "italic",  # Values will be italic
        "list": "monospace"  # List items will be monospace
    }
    italic_keys = {"journal", "volume_number"}
yaml_to_markdown(source, citation,  styles, italic_keys)
