# ReScience yaml to latex converter
# Released under the BSD two-clauses licence


def generate_latex_metadata(article):

    content = (
        "% DO NOT EDIT - automatically generated from metadata.yaml\n\n"
        "\\def \\codeURL{{{_.code.url}}}\n"
        "\\def \\codeDOI{{{_.code.doi}}}\n"
        "\\def \\dataURL{{{_.data.url}}}\n"
        "\\def \\dataDOI{{{_.data.doi}}}\n"
        "\\def \\editorNAME{{{_.editors[0].name}}}\n"
        "\\def \\editorORCID{{{_.editors[0].orcid}}}\n"
        "\\def \\reviewerINAME{{{_.reviewers[0].name}}}\n"
        "\\def \\reviewerIORCID{{{_.reviewers[0].orcid}}}\n"
        "\\def \\reviewerIINAME{{{_.reviewers[1].name}}}\n"
        "\\def \\reviewerIIORCID{{{_.reviewers[1].orcid}}}\n"
        "\\def \\dateRECEIVED{{{_.date_received}}}\n"
        "\\def \\dateACCEPTED{{{_.date_accepted}}}\n"
        "\\def \\datePUBLISHED{{{_.date_published}}}\n"
        "\\def \\articleTITLE{{{_.title}}}\n"
        "\\def \\articleYEAR{{{_.date_published.year}}}\n"
        "\\def \\reviewURL{{{_.review.url}}}\n"
        "\\def \\articleABSTRACT{{{_.abstract}}}\n"
        "\\def \\replicationBIB{{{_.replication.bib}}}\n"
        "\\def \\replicationDOI{{{_.replication.doi}}}\n"
        "\\def \\contactNAME{{{_.contact.name}}}\n"
        "\\def \\contactEMAIL{{{_.contact.email}}}\n"
        "\\def \\articleKEYWORDS{{{_.keywords}}}\n"
        "\\def \\journalVOLUME{{{_.journal_volume}}}\n"
        "\\def \\journalISSUE{{{_.journal_issue}}}\n"
        "\\def \\articleNUMBER{{{_.article_number}}}\n"
        "\\def \\articleDOI{{{_.article_doi}}}\n"
        "\\def \\authorsFULL{{{_.authors_full}}}\n"
        "\\def \\authorsABBRV{{{_.authors_abbrv}}}\n"
        "\\def \\authorsSHORT{{{_.authors_short}}}\n"
        "".format(_=article))

    for author in article.authors:
        affiliations = ",".join(author.affiliations)
        affiliations += ",\\orcid{%s}" % author.orcid
        content += "\\author[%s]{%s}\n" % (affiliations, author.name)

    for a in article.affiliations:
        if len(a.address) > 0:
            content += "\\affil[{_.code}]{{{_.name}, {_.address}}}\n".format(_=a)
        else:
            content += "\\affil[{_.code}]{{{_.name}}}\n".format(_=a)
                
    return content



# -----------------------------------------------------------------------------
if __name__ == '__main__':
    from article import Article

    filename_in = "metadata.yaml"
    filename_out = "article-metadata.tex"
    
    with open(filename_in, "r") as file:
        article = Article(file.read())

    with open(filename_out, "w") as file:
        content = generate_latex_metadata(article)
        file.write(content)
