"""Simplified DOI interface."""
import json
import re
import requests
from .dtos import PaperDTO


class Doi:
    """Interface w/ the doi.org api."""
    def get_doi_link(self, doi):
        """Assemble doi link."""
        return f"http://doi.org/{doi}"

    def load_doi_data(self, doi):
        """Load data for doi."""
        headers = {
            'Accept': 'application/json',
        }
        return requests.get(f'http://dx.doi.org/{doi}',
                            headers=headers).content

    def parse_doi_json(self, jsoncontent):
        """Tranform doi json to PaperDTO."""
        info = json.loads(jsoncontent)

        with open("debug.json", "w") as file:
            file.write(json.dumps(info))

        author = (f"{info['author'][0]['given']} {info['author'][0]['family']}"
                  if "author" in info
                  else "Author N/A")
        authors = (", ".join([f"{a['given']} {a['family']}"
                              for a in info['author']])
                   if "author" in info
                   else "Authors N/A")
        title = (info['title']
                 if "title" in info and isinstance(info['title'], str)
                 else "Title N/A")
        journal = (info['publisher']
                   if "publisher" in info
                   else "Journal N/A")
        year = info['created']['date-parts'][0][0]
        doi = info['DOI']
        abstract = (info['abstract']
                    if "abstract" in info
                    else "Abstract N/A")

        slug = f"{info['author'][0]['family']}{year}"

        return PaperDTO(author, authors, title, journal, year, abstract, doi,
                        slug)

    def get_bibtex(self, doi):
        """Get bibtex string for doi."""
        headers = {
            'Accept': 'text/bibliography; style=bibtex',
        }
        return requests.get(f'http://dx.doi.org/{doi}', headers=headers).text

    def get_info(self, doi):
        """Get information for doi."""
        try:
            jsoncontent = self.load_doi_data(doi)
            data = self.parse_doi_json(jsoncontent)
            return data
        except json.decoder.JSONDecodeError:
            return None

    def extract_doi(self, hay):
        """Parse doi from string, or None if not found.

        >>> Doi().extract_doi("https://doi.org/10.1093/petrology/egaa077")
        '10.1093/petrology/egaa077'
        """
        pattern = r'\b10\.\d{4,9}/[-._;()/:A-Z0-9]+'
        matches = re.compile(pattern, re.I).search(hay)
        return matches.group() if matches else None
