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


"""Give date in yyyy-mm-dd format for the publication!"""
"""Put titles between quotation marks!"""
"""Give date_viewed_month in abbreviated form if it's longer than 4 letters"""
# for the date last viewed, this could be changed that the input is in three
# separate parts (year, month spelled out, and day) and then write a code that
# does the abbreviation if it's longer than four letters


@dataclass
class Sources:
    source: List[Source]
# class used for internal typing representation of string forward references


def load_source(filepath: str) -> Sources:
    with open(filepath, "r") as file:
        data = yaml.safe_load(file)
#    sources = Sources(source=[Source(**source) for source in data["source"]])
#    sources = [Source(**source) for source in data["source"]]
# **source unpacks each dictionary from data["source"] into keyword arguments
# so that the keys in each dictionary match the parameters of Source, a list is
# built by iterating over each source in data["source"] and a list of Source
# objects is the result
#    return Sources(source=sources)

    def parse_date(date_value):
        if isinstance(date_value, str):  # Parse string to datetime
            return datetime.strptime(date_value, "%Y-%m-%d")
        elif isinstance(date_value, datetime):  # Already a datetime
            return date_value
        elif isinstance(date_value, date):  # Convert to datetime
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


# datetime.strftime("%d. %B %Y")  # almost correct format for date_viewed


# last_name, first_name. (date). title. *journal*, *volume_number*(issue_number
# ), page_range. <doi>


def apa7_source(data: Source) -> str:
    date_str = data.date.strftime("%Y")
    return (f"{data.last_name}, {data.first_name[0]}. ({date_str}). " +
            f"{data.title}. *{data.journal}*, " +
            f"*{data.volume_number}*({data.issue_number}), " +
            f"{data.page_range}. " +
            f"<{data.doi}>")


if __name__ == "__main__":
    sources = load_source("data_of_sources.txt")
    for source in sources.source:
        print(apa7_source(source))
    with open("apa7_bib.md", "w") as fout:
        fout.write("Bibliography \n")
    for source in sources.source:
        with open("apa7_bib.md", "a") as fout:
            fout.write(apa7_source(source) + "\n")
#    Func = open("apa7.html", "w")
#    Func.write("<html>\n<head>\n<title> \nOutput Data in an HTML file \
#               </title>\n/head> <body><h1>Bibliography<h1>\
#                   \n<h2> {apa7_source(source)}<h2> \n<body></html>")
#    Func.close()


# last_name, first_name. date. \"title.\" *journal* volume_number(issue_number)
# : page_range. <doi>


def chicago_author_date_source(data: Source):
    date_str = data.date.strftime("%Y")
    return (f"{data.last_name}, {data.first_name}. {date_str}. " +
            f"\"{data.title}.\" *{data.journal}* " +
            f"{data.volume_number}({data.issue_number}): " +
            f"{data.page_range}. " +
            f"<{data.doi}>")


if __name__ == "__main__":
    sources = load_source("data_of_sources.txt")
    for source in sources.source:
        print(chicago_author_date_source(source))
    with open("chicago_bib.md", "w") as fout:
        fout.write("Bibliography \n")
    for source in sources.source:
        with open("chicago_bib.md", "a") as fout:  # a is for append
            fout.write(chicago_author_date_source(source) + "\n")


# last_name, first_name. \"title.\" *journal*, vol. volume_number, no.
# issue_number, date, pp. page_range, <doi>. Accessed date_viewed.


def mla9_source(data: Source):
    date_str = data.date.strftime("%Y")
    date_str_viewed = data.date_viewed.strftime("%d %b %Y")

    abbreviated_month = {
        "Jan": "Jan.", "Feb": "Feb.", "Mar": "Mar.", "Apr": "Apr.",
        "May": "May",  "Jun": "Jun.", "Jul": "Jul.", "Aug": "Aug.",
        "Sep": "Sep.", "Oct": "Oct.", "Nov": "Nov.", "Dec": "Dec."}

    day = str(data.date_viewed.day)
    month = data.date_viewed.strftime("%b")
    year = data.date_viewed.strftime("%Y")
    date_str_viewed = f"{day} {abbreviated_month[month]} {year}"

    return (f"{data.last_name}, {data.first_name}. \"{data.title}.\" " +
            f"*{data.journal}*, vol. {data.volume_number}, " +
            f"no. {data.issue_number}, {date_str}, " +
            f"pp. {data.page_range}, <{data.doi}>. " +
            f"Accessed {date_str_viewed}.")


if __name__ == "__main__":
    sources = load_source("data_of_sources.txt")
    for source in sources.source:
        print(mla9_source(source))
    with open("mla_bib.md", "w") as fout:
        fout.write("Bibliography \n")
    for source in sources.source:
        with open("mla_bib.md", "a") as fout:
            fout.write(mla9_source(source) + "\n")
