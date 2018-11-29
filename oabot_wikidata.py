from wikidataintegrator import wdi_core

from sanity_checks import validate_doi, sensible_url


def load_qids(): # TODO: Load the QID data file
    return [['Q4115189', '10.1372/JOURNAL.PONE.002974421421845848484']]


def get_fatcat_data(doi): # TODO: Add API call(s)
    return 'http://test.com'


def get_wd_item(qid):
    wd_item = wdi_core.WDItemEngine(
        wd_item_id=qid
    )
    wd_json = wd_item.get_wd_entity()
    return wd_json


def edit_wd_item(qid):
    # Return None if we didn't find an item at this QID
    doi_id = wdi_core.WDExternalID(value=doi, prop_nr='P356')

    data = [doi_id]

    wd_item = wdi_core.WDItemEngine(
        domain='citation',
        search_only=True,
        item_name='citation',
        data=data,
        append_value=['P356']
    )
    wd_json = wd_item.get_wd_entity()
    #print(wd_json)

    return wd_json


def run_bot():
    input_list = load_qids()
    for input_data in input_list:
        qid = input_data[0]
        doi = input_data[1]
        fc_url = get_fatcat_data(doi)

        # Sanity check that the DOI and URL look sensible
        if not validate_doi(doi):
            continue
        if not sensible_url(fc_url):
            continue

        wd_item = get_wd_item(qid)
        if not wd_item:
            print("Error: Couldn't find a Wikidata item at {QID}".format(
                QID = qid
            ))
            continue

        # Check that existing Wikidata DOI matches the Fatcat DOI
        wd_item_doi = wd_item['claims']['P356'][0]['mainsnak']['datavalue']['value']
        if wd_item_doi != doi:
            print("Error: Mismatch between fatcat DOI {fc_doi} and Wikidata"
            "DOI {wd_doi}".format(fc_doi=doi, wd_doi=wd_item_doi))
            continue

        try:
            num_fulltext_statements = len(wd_item['claims']['P953'])
        except KeyError:
            print("Info: {qid} has no P953, adding.".format(
                qid=qid
            )) # TODO: Implement
            continue

        if num_fulltext_statements > 3:
            print("Info: Skipped {qid} which already has more than 3 full"
            "text URLs".format(qid=qid))
            continue

        print("Adding open access URL {oa_url} for {doi} to {qid}.".format(
            oa_url=fc_url,
            doi=doi,
            qid=qid
        ))


if __name__ == '__main__':
    run_bot()
