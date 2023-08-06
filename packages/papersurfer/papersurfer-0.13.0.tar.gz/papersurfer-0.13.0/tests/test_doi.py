from papersurfer.doi import Doi
from papersurfer.dtos import PaperDTO


def test_parse_doi_json_wo_author(shared_datadir):
    data_wo_author = (shared_datadir / 'data_wo_author.json').read_text()
    doi = Doi()
    data = doi.parse_doi_json(data_wo_author)
    assert data.slug == "N/A"


def test_parse_doi_json(shared_datadir):
    datafiles = ['data_wo_author.json', 'doi-10.10292011jb008747.json']
    for datafile in datafiles:
        data_wo_author = (shared_datadir / datafile).read_text()
        doi = Doi()
        paper = doi.parse_doi_json(data_wo_author)
        assert isinstance(paper, PaperDTO)
        assert paper.author
        assert paper.authors
        assert paper.title
        assert paper.journal
        assert paper.year
        assert paper.abstract
        assert paper.doi
        assert paper.slug


def test_get_info():
    Doi.load_doi_data = lambda _self, _doi: ""
    info = Doi().get_info("dummy-doi")
    assert info is None
