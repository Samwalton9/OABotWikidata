import re
import requests

# Based on the top-level Crossref formula at
# https://www.crossref.org/blog/dois-and-matching-regular-expressions/
valid_doi_regex = r"^10.\d{4,9}/[-._;()/:A-Z0-9]+$"
valid_doi_match = re.compile(valid_doi_regex)


def validate_doi(doi):
    """Make sure that a DOI string is a valid DOI structure.
    Input: A DOI string
    Output: True or False for match against DOI regex
    """
    return bool(valid_doi_match.search(doi))


def check_if_link_works(url):
    """See if a link is valid (i.e., returns a '200' to the HTML request).
    Full list of potential status codes: https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
    :return: boolean if HTTP status code returned available or unavailable,
    "error" if a different status code is returned than 200 or 404
    """
    request = requests.get(url)
    if request.status_code == 200:
        return True
    elif request.status_code == 404:
        return False
    else:
        return 'error'


def check_if_doi_resolves(doi):
    """Whether a DOI resolves via dx.doi.org

    If the link works, make sure that it points to the same DOI
    Checks first if it's a valid DOI or see if it's a redirect.
    Difference in capitalization is ok.
    :return: True if works as expected, False if it doesn't resolve correctly,
    or if the metadata DOI doesn't match doi, return the metadata DOI
    """
    if validate_doi(doi) is False:
        return "Not valid DOI structure"
    url = "https://doi.org/" + doi
    if check_if_link_works(url):
        headers = {"accept": "application/vnd.citationstyles.csl+json"}
        r = requests.get(url, headers=headers)
        r_doi = r.json()['DOI']
        if r_doi.lower() == doi.lower():
            return True
        else:
            return r_doi
    else:
        return False


def sensible_url(url):
    """Input: A URL string
    Output: True or False for match against URL sanity checks (regex?)
    """
    if len(url) <= 2000 and url.startswith("http") and "://" in url:
        return True
    else:
        return False
    
