# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 15:08:38 2024

@author: sipos_f
"""


from dataclasses import dataclass
import yaml
from typing import List
from datetime import datetime, date


@dataclass
# dataclass examines the class to find fields, which are class
# variables that have type annotations, here the first and last name, title,
# etc. are the variables and the data types specified for each are the
# annotations
class Source:
    # defining the class for the list of sources with the same keys as in the
    # data_of_sources, keeping to the yaml format
    first_name: str
    last_name: str
    title: str
    date: datetime
    journal: str
    page_range: int
    doi: str
    volume_number: int
    issue_number: int
    date_viewed: datetime


"""Give dates in yyyy-mm-dd format"""
"""Put titles that contain ':' between quotation marks!"""
"""Middle namesshould be included in the first_name, as initials or fully"""
"""If month and/or day is unkown for either dates put 01"""


@dataclass
class Sources:
    source: List[Source]
# class used for internal typing representation of string forward references


def load_source(filepath: str) -> Sources:
    with open(filepath, "r") as file:
        data = yaml.safe_load(file)
# loading the source file through the Sources class and defining 'data'

    def parse_date(date_value):
        # making sure that the date is in the correct format
        if isinstance(date_value, str):
            return datetime.strptime(date_value, "%Y-%m-%d")
        elif isinstance(date_value, datetime):
            return date_value
        elif isinstance(date_value, date):
            return datetime.combine(date_value, datetime.min.time())
        raise ValueError(f"Unexpected date format: {date_value}")

    sources = Sources(source=[
        Source(
            first_name=source["first_name"],
            last_name=source["last_name"],
            title=source["title"],
            date=parse_date(source["date"]),
            journal=source["journal"],
            page_range=source["page_range"],
            doi=source["doi"],
            volume_number=source["volume_number"],
            issue_number=source["issue_number"],
            date_viewed=parse_date(source["date_viewed"]),
        )
        for source in data["source"]
    ])
    return sources
# unpacks each dictionary from data["source"] into keyword arguments
# so that the keys in each dictionary match the parameters of Source, a list is
# built by iterating over each source in data["source"] and a list of Source
# objects is the result


# defining the different citation styles and both printing them and writing
# them into markdown files, for a bibliography and for in-text citation as well


# bibliography entry for apa 7
# the order of the variables for apa7
# last_name, first_name. (date). title. *journal*, *volume_number*(issue_number
# ), page_range. <doi>


def apa7_source(data: Source) -> str:
    date_str = data.date.strftime("%Y")
    # only the year is needed for the publication date
    return (f"{data.last_name}, {data.first_name[0]}. ({date_str}). " +
            f"{data.title}. *{data.journal}*, " +
            f"*{data.volume_number}*({data.issue_number}), " +
            f"{data.page_range}. " +
            f"<{data.doi}>")
    # the correct formatting of an apa 7th edition citation


if __name__ == "__main__":
    sources = load_source("data_of_sources.txt")
    for source in sources.source:
        print(apa7_source(source))
    with open("apa7_bib.md", "w") as fout:
        fout.write("Bibliography \n")
    # writing the first line which is "Bibliography" and linebreak at the end
    for source in sources.source:
        with open("apa7_bib.md", "a") as fout:  # a is for append
            fout.write(apa7_source(source) + "\n")
    # writing each citation into a new line


# in-text citation for apa 7


def apa7_in_text(data: Source) -> str:
    date_str = data.date.strftime("%Y")
    return (f"({data.last_name}, {date_str})")


if __name__ == "__main__":
    sources = load_source("data_of_sources.txt")
    for source in sources.source:
        print(apa7_in_text(source))
    with open("apa7_in_text.md", "w") as fout:
        fout.write(apa7_in_text(source) + "\n")


# bibliography entry for chicago manual of style 17th ediion author-date
# the order of the variables for chicago
# last_name, first_name. date. \"title.\" *journal* volume_number(issue_number)
# : page_range. <doi>


def chicago_author_date_source(data: Source):
    date_str = data.date.strftime("%Y")
    return (f"{data.last_name}, {data.first_name}. {date_str}. " +
            f"\"{data.title}.\" *{data.journal}* " +
            f"{data.volume_number}({data.issue_number}): " +
            f"{data.page_range}. " +
            f"<{data.doi}>")
    # the correct formatting of a chicago author date citation


if __name__ == "__main__":
    sources = load_source("data_of_sources.txt")
    for source in sources.source:
        print(chicago_author_date_source(source))
    with open("chicago_bib.md", "w") as fout:
        fout.write("Bibliography \n")
    for source in sources.source:
        with open("chicago_bib.md", "a") as fout:
            fout.write(chicago_author_date_source(source) + "\n")


# in-text citation for chicago manual of style 17th ediion author-date

def chicago_in_text(data: Source) -> str:
    date_str = data.date.strftime("%Y")
    return (f"({data.last_name} {date_str})")


if __name__ == "__main__":
    sources = load_source("data_of_sources.txt")
    for source in sources.source:
        print(chicago_in_text(source))
    with open("chicago_in_text.md", "w") as fout:
        fout.write(chicago_in_text(source) + "\n")


# bibliography entry for mla 9
# the order of the variables for mla9
# last_name, first_name. \"title.\" *journal*, vol. volume_number, no.
# issue_number, date, pp. page_range, <doi>. Accessed date_viewed.


def mla9_source(data: Source):
    date_str = data.date.strftime("%Y")
    date_str_viewed = data.date_viewed.strftime("%d %b %Y")
    # for date date_viewed/when the source was last accessed it requires date
    # and month as well if possible, and the month written out and abbreviated
    # if it's longer, and in day month year order

    abbreviated_month = {
        "Jan": "Jan.", "Feb": "Feb.", "Mar": "Mar.", "Apr": "Apr.",
        "May": "May",  "Jun": "June", "Jul": "July", "Aug": "Aug.",
        "Sep": "Sep.", "Oct": "Oct.", "Nov": "Nov.", "Dec": "Dec."}
    # changing the written out month into the correct forms

    day = str(data.date_viewed.day)
    month = data.date_viewed.strftime("%b")
    year = data.date_viewed.strftime("%Y")
    date_str_viewed = f"{day} {abbreviated_month[month]} {year}"
    # formatting the correct form of the date and it also removes 0s if the day
    # or month starts with it

    return (f"{data.last_name}, {data.first_name}. \"{data.title}.\" " +
            f"*{data.journal}*, vol. {data.volume_number}, " +
            f"no. {data.issue_number}, {date_str}, " +
            f"pp. {data.page_range}, <{data.doi}>. " +
            f"Accessed {date_str_viewed}.")
    # the correct formatting of an mla 9th edition citation


if __name__ == "__main__":
    sources = load_source("data_of_sources.txt")
    for source in sources.source:
        print(mla9_source(source))
    with open("mla_bib.md", "w") as fout:
        fout.write("Bibliography \n")
    for source in sources.source:
        with open("mla_bib.md", "a") as fout:
            fout.write(mla9_source(source) + "\n")


# in-text citation for mla 9

def mla9_in_text(data: Source) -> str:
    return (f"({data.last_name})")


if __name__ == "__main__":
    sources = load_source("data_of_sources.txt")
    for source in sources.source:
        print(mla9_in_text(source))
    with open("mla9_in_text.md", "w") as fout:
        fout.write(mla9_in_text(source) + "\n")
