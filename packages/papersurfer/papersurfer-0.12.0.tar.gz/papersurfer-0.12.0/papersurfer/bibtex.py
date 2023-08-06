"""Simplified DOI interface."""
from .doi import Doi


class Bibtex:
    """Interface for bibtex string."""
    def entry_from_doi(self, doi):
        """Get bibtex string for doi."""
        return Doi().get_bibtex(doi)

    def bib_from_dois(self, dois):
        """Get bibtex string for mulitple dois."""
        return "\n".join([Doi().get_bibtex(doi) for doi in dois])
