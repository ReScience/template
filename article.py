# ReScience yaml parser
# Released under the BSD two-clauses licence

import yaml
import dateutil.parser

class Contributor:
    def __init__(self, role, name, orcid="", email="", affiliations=[]):
        self.role = role
        self.name = name
        self.fullname = name
        self.lastname = self.get_lastname(name)
        self.abbrvname = self.get_abbrvname(name)
        self.orcid = orcid
        self.email = email
        self.affiliations = affiliations

    def get_abbrvname(self, name):
        if ',' in name:
            lastname = name.split(",")[0]
            firstnames = name.split(",")[1].strip().split(" ")
        else:
            lastname = name.split(" ")[-1]
            firstnames = name.split(" ")[:-1]
        abbrvname = ""
        for firstname in firstnames:
            if "-" in firstname:
                for name in firstname.split("-"):
                    abbrvname += name[0].strip().upper() + '.-'
                abbrvname = abbrvname[:-1]
            else:
                abbrvname += firstname[0].strip().upper() + '.'
        return abbrvname + " " + lastname


    def get_lastname(self, name):
        # Rougier, Nicolas P.
        if ',' in name:
            lastname = name.split(",")[0].strip()
            firstname = name.split(",")[1].strip()
        # Nicolas P. Rougier
        else:
            lastname = name.split(" ")[-1]
            firstname = name.split(" ")[:-1]
        return lastname
    

class Affiliation:
    def __init__(self, code, name, address=""):
        self.code = code
        self.name = name
        self.address = address

class Repository:
    def __init__(self, name, url, doi):
        self.name = name
        self.url = url
        self.doi = doi

class Replication:
    def __init__(self, bib, doi):
        self.bib = bib
        self.doi = doi

class Review:
    def __init__(self, url, doi):
        self.url = url
        self.doi = doi

class Date:
    def __init__(self, date):
        date = dateutil.parser.parse(date)
        self.date = date
        self.year = date.year
        self.month = date.month
        self.day = date.day

    def __str__(self):
        return self.date.strftime("%d %B %Y")

    def __repr__(self):
        return self.date.strftime("%d %B %Y")
        

class Article:
    def __init__(self, data):
        self.title = None
        self.absract = None
        self.keywords = []
        self.authors = []
        self.editors = []
        self.reviewers = []
        self.affiliations = []
        self.code = None
        self.data = None
        self.number = None
        self.contact = None

        self.review = None
        self.replication = None
        
        self.date_received = None
        self.date_accepted = None
        self.date_published = None

        self.journal_name = "ReScience"
        self.journal_issn = "2430-3658"
        self.journal_volume = None
        self.journal_issue = None
        self.article_number = None
        self.article_doi = None

        self.parse(data)

        # Build authors list
        self.authors_short = "" # Family names only
        self.authors_abbrv = "" # Abbreviated firsnames + Family names
        self.authors_full = ""  # Full names
        
        n = len(self.authors)
        if n > 3:
            self.authors_short = self.authors[0].lastname + " et al."
            self.authors_abbrv = self.authors[0].abbrvname + " et al."
            self.authors_full = self.authors[0].fullname + " et al."
        else:
            for i in range(n-2):
                self.authors_short += self.authors[i].lastname + ", "
                self.authors_abbrv += self.authors[i].abbrvname + ", "
                self.authors_full += self.authors[i].fullname + ", "
                
            self.authors_short += self.authors[n-2].lastname + " and "
            self.authors_short += self.authors[n-1].lastname

            self.authors_abbrv += self.authors[n-2].abbrvname + " and "
            self.authors_abbrv += self.authors[n-1].abbrvname

            self.authors_full += self.authors[n-2].fullname + " and "
            self.authors_full += self.authors[n-1].fullname

            
        
    def parse(self, data):
        document = yaml.load(data)

        self.title = document["title"]
        self.abstract = document["abstract"]
        self.keywords = ", ".join(document["keywords"])

        # Miscellaneous dates
        dates = {key:value for data in document["dates"]
                           for key, value in data.items()}
        self.date_received = Date(dates["received"])
        self.date_accepted = Date(dates["accepted"])
        self.date_published = Date(dates["published"])
        
        # Add authors
        for item in document["authors"]:
            role = "author"
            name = item["name"]
            orcid = item.get("orcid","")
            email = item.get("email","")
            affiliations = item["affiliations"].split(",")
            if "*" in affiliations:
                affiliations.remove("*")
                author = Contributor(role, name, orcid, email, affiliations)
                self.add_contributor(author)
                self.contact = author
            else:
                author = Contributor(role, name, orcid, email, affiliations)
                self.add_contributor(author)
                

        # Add author affiliations
        for item in document["affiliations"]:
            self.affiliations.append(
                Affiliation(item["code"],
                            item["name"],
                            item.get("address", "")))

    
        # Add editor & reviewers
        for item in document["contributors"]:
            role = item["role"]
            name = item["name"]
            orcid = item.get("orcid","")
            contributor = Contributor(role, name, orcid)
            self.add_contributor(contributor)

            
        # Code repository (mandatory)
        if "code" in document.keys():
            code = {key:value for data in document["code"]
                              for key, value in data.items()}
            self.code = Repository("code",
                                   code.get("url","") or "",
                                   code.get("doi","") or "")
        else:
            raise IndexError("Code repository not found")
        
        # Data repository (optional)
        if "data" in document.keys():
            data = {key:value for data in document["data"]
                              for key, value in data.items()}
            self.data = Repository("data",
                                   data.get("url","") or "",
                                   data.get("doi","") or "")
        else:
            self.data = Repository("data", "", "")
            
        # Review
        review = {key:value for review in document["review"]
                            for key, value in review.items()}
        self.review = Review(review["url"], review["doi"])

        # Replication
        replication = {key:value for replication in document["replication"]
                                 for key, value in replication.items()}
        self.replication = Replication(replication["bib"], replication["doi"])

        # Article number & DOI
        article = {key:value for article in document["article"]
                             for key, value in article.items()}
        self.article_number = str(article["number"])
        self.article_doi = article.get("doi","") or ""

        # Journal volume and issue
        journal = {key:value for journal in document["journal"]
                             for key, value in journal.items()}
        self.journal_volume = str(journal["volume"])
        self.journal_issue = str(journal["issue"])
        
                    
    def add_contributor(self, contributor):
        if contributor.role == "author":
            self.authors.append(contributor)
        elif contributor.role == "editor":
            self.editors.append(contributor)
        elif contributor.role == "reviewer":
            self.reviewers.append(contributor)
        else:
            raise(IndexError)



# -----------------------------------------------------------------------------
if __name__ == '__main__':

    with open("metadata.yaml") as file:
        article = Article(file.read())
        print(article.authors_full)
        print(article.authors_abbrv)
        print(article.authors_short)
