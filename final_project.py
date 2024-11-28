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
    for source in sources.source:
        print(apa7_source(source))
