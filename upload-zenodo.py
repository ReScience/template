# -----------------------------------------------------------------------------
# Copyright 2018 ReScience - BSD two-clauses licence
#
# This script takes care of uploading a new ReScience article to Zenodo.
# 
# It requires the acticle (PDF) article and the metadata (YAML).
#
# It works in two passes:
#  - First pass reserves a DOI on Zenodo
#  - Second pass upload the paper and update the metadata
#
# Zenodo REST API at http://developers.zenodo.org
# -----------------------------------------------------------------------------
import json
import os
import os.path
import requests
from article import Article


def reserve_doi(server, token):
    """ Reserve a new DOI """
    
    headers = { "Content-Type": "application/json" }
    url = 'https://%s/api/deposit/depositions' % server
    response = requests.post(url, params={'access_token': token},
                             json={}, headers=headers)
    if response.status_code != 201:
        raise IOError("%s: " % response.status_code +
                      response.json()["message"])
    data = response.json() 
    return data["id"], data["metadata"]["prereserve_doi"]["doi"]


def upload_content(server, token, article_id, filename):
    """ Upload content to server """
        
    data = {'filename': filename}
    files = {'file': open(filename, 'rb')}
    url = 'https://%s/api/deposit/depositions/%s/files' % (server, article_id)
    response = requests.post(url, params={'access_token': token},
                              data=data, files=files)
    if response.status_code != 201:
        raise IOError("%s: " % response.status_code +
                      response.json()["message"])

    
def update_metadata(server, token, article_id, article):
    """ Upload content metadata to server """
        
    headers = {"Content-Type": "application/json"}
    url = 'https://%s/api/deposit/depositions/%s' % (server, article_id)

    data = {
        'metadata': {
            'title': article.title,
            'upload_type': 'publication',
            'publication_type': 'article',
            'description' : "A replication of"  + article.replication.bib,
            'creators': [ {'name': author.name,
                           'orcid': author.orcid} for author in article.authors],
            'access_right' : 'open',
            'license' : 'cc-by',
            'keywords' : article.keywords.split(),
            'contributors' : [
                {'name': article.editors[0].name, 'type': 'Editor' }
            ],
            'related_identifiers' : [
                {'relation': 'isSupplementedBy', 'identifier': article.code.doi},
                {'relation': 'cites',     'identifier': article.replication.doi}
            ],
            'journal_title' : "ReScience",
            'journal_volume' : article.journal_volume,
            'journal_issue' : article.journal_issue,
            'journal_pages' : "#%s" % article.article_number,
            'communities' : [
                {'identifier': 'rescience'}],
        }
    }

    response = requests.put(url, params={'access_token': token},
                            data=json.dumps(data),  headers=headers)
    if response.status_code != 200:
        raise IOError("%s: " % response.status_code +
                      response.json()["message"])

    
def publish(server, token, article_id):
    """ Publish entry """
    
    url = 'https://%s/api/deposit/depositions/%s/actions/publish' % (server, article_id)
    response = requests.post(url, params={'access_token': token})
    if response.status_code != 202:
        raise IOError("%s: " % response.status_code +
                      response.json()["message"])



     
# -----------------------------------------------------------------------------
if __name__ == '__main__':

    # Server
    # server = "zenodo.org"
    server = "sandbox.zenodo.org"

    # Server token (you'll need one)
    # -> Go to https://{server}/account/settings/applications/tokens/new/
    # -> Make sure to request a token for actions+write+email
    if server == "sandbox.zenodo.org":
        token = os.getenv("ZENODO_SANDBOX_TOKEN")
    else:
        token = os.getenv("ZENODO_TOKEN")

    # Article metadata
    article_data = "metadata.yaml"

    # Article PDF file
    article_pdf = "article.pdf"

    # Article 
    with open(article_data) as file:
        article = Article(file.read())

    # ---------------------------------------------------------------------
    # Article DOI (needs to be filled after the first connection to Zenodo)
    # ---------------------------------------------------------------------
    article_doi = None

    # ----------------------------------------------------------------------------
    # Article Zenodo id  (needs to be filled after the first connection to Zenodo)
    # ----------------------------------------------------------------------------
    article_id = None 


    # Get DOI if necessary
    if article_id is None:
        print("Request for a new DOI... ", end="")
        article_id, article_doi = reserve_doi(server, token)
        print("done!")

    print("Article ID: ", article_id)
    print("Article DOI:", article_doi)

    # Check if metadata DOI and Zenodo DOI are the same
    if article.article_doi != article_doi:
        raise ValueError("Article DOI in metadata needs to be updated")

    # Check if metadata file is newer than pdf
    if os.path.getmtime(article_data) > os.path.getmtime(article_pdf):
        raise ValueError("Article PDF needs to be rebuild")

    # Upload content
    print("Uploading content... ", end="")
    upload_content(server, token, article_id, article_pdf)
    print("done!")
        
    # Update metadata
    print("Updating metadata... ", end="")
    update_metadata(server, token, article_id, article)
    print("done!")

    # Publish entry
    print("Publishing... ", end="")
    publish(server, token, article_id)
    print("done!\n")

    print("Entry is online at ", end="")
    print("https://%s/record/%s" % (server, article_id))
