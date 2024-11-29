# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 15:08:38 2024

@author: sipos_f
"""


from dataclasses import dataclass
import yaml
from typing import List


@dataclass
# dataclass examines the class to find fields, which are class
# variables that have type annotations, here the first and last name, title,
# etc. are the variables and the data types specified for each are the
# annotations
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
    date_viewed1: str
    date_viewed2: str
    date_viewed3: str


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

    sources = [Source(**source) for source in data["source"]]
# **source unpacks each dictionary from data["source"] into keyword arguments
# so that the keys in each dictionary match the parameters of Source, a list is
# built by iterating over each source in data["source"] and a list of Source
# objects is the result
    return Sources(source=sources)


# last_name, first_name. (date). title. *journal*, *volume_number*(issue_number
# ), page_range. <doi>


def apa7_source(data: Source):

    return (f"{data.last_name}, {data.first_name:.1s}. ({data.date:.4s}). " +
            f"{data.title}. *{data.journal}*, " +
            f"*{data.volume_number}*({data.issue_number}), " +
            f"{data.page_range}. " +
            f"<{data.doi}>")


if __name__ == "__main__":
    sources = load_source("data_of_sources.txt")
    for source in sources.source:
        print(apa7_source(source))


# last_name, first_name. date. \"title.\" *journal* volume_number(issue_number)
# : page_range. <doi>


def chicago_author_date_source(data: Source):

    return (f"{data.last_name}, {data.first_name}. {data.date:.4s}. " +
            f"\"{data.title}.\" *{data.journal}* " +
            f"{data.volume_number}({data.issue_number}): " +
            f"{data.page_range}. " +
            f"<{data.doi}>")


if __name__ == "__main__":
    sources = load_source("data_of_sources.txt")
    for source in sources.source:
        print(chicago_author_date_source(source))


# last_name, first_name. \"title.\" *journal*, vol. volume_number, no.
# issue_number, date, pp. page_range, <doi>. Accessed date_viewed.


def mla9_source(data: Source):

    return (f"{data.last_name}, {data.first_name}. \"{data.title}.\" " +
            f"*{data.journal}*, vol. {data.volume_number}, " +
            f"no. {data.issue_number}, {data.date:.4s}, " +
            f"pp. {data.page_range}, <{data.doi}>. " +
            f"Accessed {data.date_viewed1} {data.date_viewed2} " +
            f"{data.date_viewed3}.")


if __name__ == "__main__":
    sources = load_source("data_of_sources.txt")
    for source in sources.source:
        print(mla9_source(source))
