"""
This script assigns a product tag to each item of the test data set to compute accuracy of
our tagging algorithm
"""
import collections
import logging
import operator
import re

from fuzzywuzzy import fuzz, process
import pandas as pd

script_name = "tutti-product-tagger"
log = logging.getLogger(script_name)

# Dict that maps each tag to the related keywords for regex tagging
tag_keyword_mapping = {
    "furniture": collections.OrderedDict(
        [
            ("armchair", [r"sessel"]),
            ("bean bag chair", [r"sitzsack"]),
            ("bed", [r"bett", r"bettgestell", r"lattenrost", r"lättlirost"]),
            ("bench", [r"bank"]),
            ("carpet/rug", [r"teppich"]),
            ("chair", [r"stuhl", r"stühle"]),
            ("chest/box", [r"kasten"]),
            ("clothes rack", [r"kleiderständer"]),
            ("commode", [r"kommode", r"kommoden", r"komode"]),
            ("cupboard", [r"schrank", r"buffet"]),
            ("desk", [r"schreibtisch", r"bürotisch", r"sekretär", r"pult"]),
            ("display cabinet", [r"vitrine"]),
            ("door", [r"tür"]),
            ("filing cabinet", [r"aktenschrank", r"korpus"]),
            ("garden chair", [r"gartenstuhl", r"gartenstühle"]),
            ("garden table", [r"gartentisch"]),
            ("mattress", [r"matratze"]),
            ("mirror", [r"spiegel"]),
            ("picture frame", [r"bilderrahmen"]),
            ("pillow", [r"kissen"]),
            ("shelf", [r"regal", r"regale", r"kallax", r"ablage"]),
            ("bookcase", [r"bücher" r"bücherregal", r"bücherregale" r"büchergestell", r"bücherschrank"]),
            ("shoe cabinet", [r"schuhschrank", r"schuhkasten", r"schuhregal"]),
            ("sideboard", [r"sideboard", r"sideboards", r"tv-", r"fernsehmöbel", r"tv möbel"]),
            ("sofa", [r"sofa", r"couch", r"polstergruppe", r"bett-sofa"]),
            ("stool", [r"hocker", r"hoker"]),
            ("table", [r"tisch", r"tische", r"tischli"]),
            ("wardrobe", [r"kleiderschrank", r"garderobe"]),
        ]
    )
}

# Compile regex expressions for faster execution
word_terminations = r"(\s|$|,|\.)"
tag_keyword_mapping_compiled = {
    cat: collections.OrderedDict(
        [
            (key, [re.compile(x + r"{}".format(word_terminations)) for x in val])
            for key, val in tag_keyword_mapping[cat].items()
        ]
    )
    for cat in tag_keyword_mapping
}


def assign_fuzzy_tag(text: str, category: str, threshold: int = 70) -> str:
    """
    Use fuzzy search to assign a tag to a string. The keyword mapping is the same
    used by regex, but there is a threshold to control the similarity required

    :param text: text to tag
    :param category: category of the tags (used for filtering the keyword map)
    :param threshold: confidence required to return a match
    :return: string, the tag ('other' if not found with required confidence)
    """
    scores0 = {key: process.extractOne(text.lower(), val)[1] for key, val in tag_keyword_mapping[category].items()}
    scores1 = {
        key: process.extractOne(text.lower(), val, scorer=fuzz.partial_ratio)[1]
        for key, val in tag_keyword_mapping[category].items()
    }
    scores2 = {
        key: process.extractOne(text.lower(), val, scorer=fuzz.token_set_ratio)[1]
        for key, val in tag_keyword_mapping[category].items()
    }
    scores3 = {
        key: process.extractOne(text.lower(), val, scorer=fuzz.token_sort_ratio)[1]
        for key, val in tag_keyword_mapping[category].items()
    }
    max0 = max(scores0.items(), key=operator.itemgetter(1))
    max1 = max(scores1.items(), key=operator.itemgetter(1))
    max2 = max(scores2.items(), key=operator.itemgetter(1))
    max3 = max(scores3.items(), key=operator.itemgetter(1))
    tag_list = [max0, max1, max2, max3]
    final = {0: max0[1], 1: max1[1], 2: max2[1], 3: max3[1]}
    idx, score = max(final.items(), key=operator.itemgetter(1))
    if score >= threshold:
        return tag_list[idx][0]
    else:
        return "other"


def assign_tag_to_subject_body(
    df: pd.DataFrame,
    subject_col: str,
    body_col: str = None,
    category: str = "furniture",
    fuzzy: bool = False,
    fuzzy_refine_confidence: int = 70,
) -> str:
    """
    Assign tag to item using tag->keyword mapping

    :param df: pd.DataFrame containing the items
    :param subject_col: name of column holding the title of ads in df
    :param body_col: name of column holding the body of ads in df
    :param category: name of the category of the ad
    :param fuzzy: use fuzzy search for refining the result if regex doesn't find a match
    :param fuzzy_refine_confidence: confidence (0 to 100) to use for fuzzy matching
    :return: string, the tag found ('other' if no match is found)
    """
    tags = dict()
    for tag, pattern_list in tag_keyword_mapping_compiled[category].items():
        for pattern in pattern_list:
            match = pattern.search(df[subject_col].lower())
            if match:
                tags.update({tag: match.start()})

    if body_col:
        if len(tags) == 0:
            for tag, pattern_list in tag_keyword_mapping_compiled[category].items():
                for pattern in pattern_list:
                    match = pattern.search(df[body_col].lower())
                    if match:
                        tags.update({tag: match.start()})

    if len(tags) == 0:
        if fuzzy:
            if body_col:
                return assign_fuzzy_tag(df[subject_col] + df[body_col], category, fuzzy_refine_confidence)
            else:
                return assign_fuzzy_tag(df[subject_col], category, fuzzy_refine_confidence)
        else:
            return "other"
    else:
        return min(tags, key=tags.get)


def assign_tag_to_string(
    text: str, category: str = "furniture", fuzzy: bool = False, fuzzy_refine_confidence: int = 70
) -> dict:
    """
    Assign tag to item using tag->keyword mapping.

    :param text: string to parse
    :param category: name of the category of the ad
    :param fuzzy: use fuzzy search for refining the result if regex doesn't find a match
    :param fuzzy_refine_confidence: confidence (0 to 100) to use for fuzzy matching
    :return: dict {'tag': matched_tag} (to make it usable in REST APIs)
    """
    tags = dict()
    for tag, pattern_list in tag_keyword_mapping_compiled[category].items():
        for pattern in pattern_list:
            match = pattern.search(text.lower())
            if match:
                tags.update({tag: match.start()})

    if len(tags) == 0:
        if fuzzy:
            return {"tag": assign_fuzzy_tag(text, category, fuzzy_refine_confidence)}
        else:
            return {"tag": "other"}
    else:
        return {"tag": min(tags, key=tags.get)}
