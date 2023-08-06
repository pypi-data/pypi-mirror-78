from papersurfer.papersurfer import details_popup
from papersurfer.dtos import PaperDTO

def test_details_popup():
        paper = PaperDTO(
            "paper.author",
            "paper.authors",
            "paper.title",
            "paper.journal",
            2020,
            "paper.abstract",
            "paper.doi",
            "paper.slug",
        )
        close_dialog = lambda: None
        popup = details_popup(paper, close_dialog)
        print(popup)

def test_details_popup():
    close_dialog = lambda: None
    popup = details_popup(None, close_dialog)
    print(popup)