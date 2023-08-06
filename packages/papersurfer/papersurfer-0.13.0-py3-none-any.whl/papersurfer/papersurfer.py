"""Paper surfer - browse papers posted on the mattermost channel.

UI:

[____(filter)______]
1. paper (open discussion) (open paper)
2. paper (open discussion) (open paper)
3. paper (open discussion) (open paper)
4. paper (open discussion) (open paper)

"""
from functools import partial
import time
import os
import sys
import re
import logging
import pathlib
import webbrowser
import urwid
import configargparse
from tinydb import TinyDB, Query
from xdgappdirs import AppDirs
from .exceptions import ConfigError
from .ui_elements import PrettyButton
from .mattermost import Mattermost
from .doi import Doi
from .bibtex import Bibtex
from .dtos import PostDTO, PaperDTO
from . import config


class Papersurfer:
    """Organize and cache paper/post data.

    This handles interaction with mattermost, doi and a local database.

    Papers and posts are similar but distinct concepts. A post contains
    information on a single mattermost entry, containing a paper reference.
    A paper contains information on a single scientific paper and a reference
    back to the mattermost post.
    """
    def __init__(self, url, channelname, username, password):
        self._filters = {
            "needle": "",
            "fromdate": None,
            "untildate": None
        }

        self.mattermost = Mattermost(url, channelname, username, password)

        self.db_path = config.datadir

        self.db_posts = None
        self.db_papers = None
        self.db_files = {
            "posts": "papersurfer_posts_db.json",
            "papers": "papersurfer_papers_db.json",
        }

    def load(self):
        """Load data from mattermost and save to storage."""
        self._connect_db()
        latest = self.get_latest_post()
        posts = self.mattermost.retrieve(latest["create_at"]
                                         if latest else None)
        self._update_db(posts=posts)

    def _connect_db(self):
        """Establish db connection. Noop if already connected."""
        if not self.db_posts:
            dbfile = os.path.join(self.db_path, self.db_files['posts'])
            self.db_posts = TinyDB(dbfile)
        if not self.db_papers:
            dbfile = os.path.join(self.db_path, self.db_files['papers'])
            self.db_papers = TinyDB(dbfile)

    def get_latest_post(self):
        """Find the newest post and return."""
        posts = self.db_posts.all()
        if posts:
            posts.sort(reverse=True, key=lambda p: p["create_at"])

        return posts[0] if posts else None

    def _update_db(self, posts=None, papers=None):
        """Merge new data into database."""
        if posts:
            self._upsert_multiple(posts, self.db_posts)
        if papers:
            self._upsert_multiple(papers, self.db_papers)

    def _upsert_multiple(self, records, database):
        """Update record in db unless it exits, then insert.

        Would be trivial if we could just change the unique id in tinydb to the
        doi property, but we can't.
        """
        for record in records:
            database.upsert(record.__dict__, Query().doi == record.doi)

    def get_posts(self):
        """Get all posts in storage."""
        self._connect_db()
        return [PostDTO(p["id"], p["create_at"], p["message"],
                        p["reporter"], p["doi"])
                for p in self.db_posts.all()]

    def get_posts_filtered(self, needle=None):
        """Return a list of papers, filtered by filter."""
        self._filters['needle'] = needle = (needle
                                            if needle
                                            else self._filters['needle'])
        return [m for m in self.get_posts()
                if needle.lower() in m.message.lower()
                or needle.lower() in m.reporter.lower()]

    def get_papers(self):
        """Get all papers in storage."""
        return self.db_papers.all()


class PapersurferUi:
    """Provide UI and interface with mattermost class."""

    _palette = [
        ('button', 'default,bold', 'default'),
        ('I say', 'default,bold', 'default', 'bold'),
        ('needle', 'default, bold, underline', 'default', 'bold'),
        ('highlight', 'black', 'dark blue'),
        ('banner', 'black', 'light gray'),
        ('selectable', 'white', 'black'),
        ('focus', 'black', 'light gray'),
        ('papertitle', 'default,bold', 'default', 'bold')
    ]

    def __init__(self, url, channel, username, password):
        self.papersurfer = Papersurfer(url, channel, username, password)
        self._screen = urwid.raw_display.Screen()
        self.size = self._screen.get_cols_rows()

        ask = urwid.Edit(('I say', u"Filter?\n"))
        exitbutton = PrettyButton(u'Exit', on_press=self.on_exit_clicked)
        self.exportbutton = PrettyButton(u'Export filtered list as bibtex',
                                         on_press=self.on_export_clicked)
        submitbutton = PrettyButton('Submit paper',
                                    on_press=self.open_submit_paper)
        div = urwid.Divider(u'-')

        body = [urwid.Text("")]
        self.listcontent = urwid.SimpleFocusListWalker(body)

        paperlist = urwid.BoxAdapter(urwid.ListBox(self.listcontent),
                                     self.size[1] - 5)
        buttonrow = urwid.Columns([exitbutton, self.exportbutton,
                                   submitbutton])
        self.pile = urwid.Pile([ask,
                                div,
                                paperlist,
                                div,
                                buttonrow])
        self.top = urwid.Filler(self.pile, valign='middle')
        self._pile = urwid.Pile(
            [
                self.loading_indicator()
            ]
        )
        self._over = urwid.Overlay(
            self._pile,
            self.top,
            align='center',
            valign='middle',
            width=20,
            height=10
        )

        urwid.connect_signal(ask, 'change', self.onchange)
        self.mainloop = urwid.MainLoop(self._over, self._palette,
                                       unhandled_input=self._h_unhandled_input)
        self.mainloop.set_alarm_in(.1, self._h_load_list)
        self.mainloop.set_alarm_in(.2, self._h_update_data)
        self.mainloop.run()

    def _h_unhandled_input(self, key):
        """Handle keyboard input not otherwise handled."""
        if key == "esc":
            raise urwid.ExitMainLoop()

    def _h_load_list(self, _loop, _data):
        """Handle load list alarm."""
        self._load_list()

    def _load_list(self):
        """Load and display paper list."""
        body = [self.list_item(post) for post in self.papersurfer.get_posts()]
        if len(body) == 0:
            return
        self.listcontent.clear()
        self.listcontent.extend(body)
        self.mainloop.widget = self.top

    def _h_update_data(self, _loop, _data):
        """Handle update data alarm."""
        self._update_data()

    def _update_data(self):
        """Load and display paper list."""
        self.papersurfer.load()
        self._load_list()

    def loading_indicator(self):
        """Create loading indicator dialog."""
        body_text = urwid.Text("Loading...", align='center')
        body_filler = urwid.Filler(body_text, valign='middle')
        body_padding = urwid.Padding(
            body_filler,
            left=1,
            right=1
        )

        return urwid.Frame(body_padding)

    def list_item(self, paper, needle=""):
        """Create highlighted text entry."""
        text_items = []
        needle = needle or "ßß"
        msg = f"{paper.message} ({paper.reporter})"
        needles = re.findall(needle, msg, flags=re.IGNORECASE)
        hay = re.split(needle, msg, flags=re.IGNORECASE)
        for i, item in enumerate(hay):
            text_items.append(item)
            if i < len(needles):
                text_items.append(('needle', needles[i]))

        title = urwid.Text(text_items)
        discuss_button = PrettyButton("Open Discussion",
                                      on_press=partial(self.h_open_discussion,
                                                       paper))
        doi_button = PrettyButton("Open DOI",
                                  on_press=partial(self.h_open_doi, paper))
        details_button = PrettyButton("Show details",
                                      on_press=partial(self.h_show_details,
                                                       paper))

        button_bar = urwid.Columns([
            discuss_button, doi_button, details_button])
        pile = urwid.Pile([title, button_bar, urwid.Divider()])
        return pile

    def updscrn(self):
        """Update (redraw) screen."""
        self.mainloop.draw_screen()

    def onchange(self, _, needle):
        """Handle filter change."""
        self.listcontent.clear()
        self.listcontent.extend([
            self.list_item(paper, needle)
            for paper in self.papersurfer.get_posts_filtered(needle)])

    def running_export(self, state):
        """Set exporting state."""
        label = self.exportbutton.get_label()
        running_indicator = " (running...)"
        if state:
            self.exportbutton.set_label(label + running_indicator)
        else:
            self.exportbutton.set_label(label.replace(running_indicator, ""))
        self.updscrn()

    def on_exit_clicked(self, button):
        """Handle exitbutton click and exit."""
        raise urwid.ExitMainLoop()

    def on_export_clicked(self, _):
        """Handle exitbutton click and exit."""
        self.running_export(True)
        self.export_to_bibtex()
        self.running_export(False)

    def export_to_bibtex(self):
        """Export current filtered list to bibtex file."""
        papers = self.papersurfer.get_posts_filtered()
        dois = [paper.doi for paper in papers]
        string = Bibtex().bib_from_dois(dois)
        with open("export.bib", 'w') as file:
            file.write(string)

    def h_open_discussion(self, post, _):
        """Handle click/enter on discussion button."""
        self.open_discussion(post)

    def h_open_doi(self, post, _):
        """Handle click/enter on doi button."""
        self.open_doi(post)

    def h_show_details(self, post, _):
        """Handle click/enter on doi button."""
        self.show_details(post)

    def open_discussion(self, post):
        """Open Mattermost post in browser."""
        link = f"https://mattermost.cen.uni-hamburg.de/ifg/pl/{post.id}"
        webbrowser.open(link)

    def open_doi(self, post):
        """Open paper page in browser."""
        webbrowser.open(Doi().get_doi_link(post.doi))

    def show_details(self, post):
        """Open doi info in popup."""
        start = time.perf_counter()
        paper = Doi().get_info(post.doi)
        logging.debug("got doi info %s after %f s", paper,
                      time.perf_counter() - start)

        if paper is None:
            logging.error("Failed to load doi %s", post.doi)

        self.mainloop.widget = details_popup(paper, self.h_close_dialog)

    def h_close_dialog(self, _):
        """Handle close dialog button."""
        self.close_dialog()

    def close_dialog(self):
        """Close currently open dialog."""
        self.mainloop.widget = self.top

    def h_close_submit_paper(self, _):
        """Reload fresh data when closing submit paper dialog."""
        self._update_data()
        self.close_dialog()

    def open_submit_paper(self, _):
        """Open submit paper dialog."""
        self._pile = urwid.Pile(
            [
                PostDialog(self.papersurfer.mattermost,
                           self.h_close_submit_paper, self.mainloop)
            ]
        )
        self._over = urwid.Overlay(
            self._pile,
            self.top,
            align='center',
            valign='middle',
            width=100,
            height=200
        )

        self.mainloop.widget = self._over


def details_popup(paper, close_dialog):
    """Create Dialog with paper details."""
    if paper is None:
        paper = PaperDTO(
            title="Could not load or parse DOI data.",
            author="N/A",
            authors="N/A",
            journal="N/A",
            year=2020,
            abstract="N/A",
            doi="N/A",
            slug="N/A",
        )

    header_text = urwid.Text(('banner', 'Paper details'), align='center')
    header = urwid.AttrMap(header_text, 'banner')

    body_pile = urwid.Pile([
        urwid.Text(("papertitle", paper.title)),
        urwid.Text(paper.authors),
        urwid.Text(paper.journal),
        urwid.Text(paper.doi),
        urwid.Text(paper.abstract),
        urwid.Text(" "),
        urwid.Text(Bibtex().entry_from_doi(paper.doi)),
    ])
    body_filler = urwid.Filler(body_pile, valign='top')
    body_padding = urwid.Padding(
        body_filler,
        left=1,
        right=1
    )
    body = urwid.LineBox(body_padding)

    # Footer
    footer = PrettyButton('Okay', close_dialog)
    footer = urwid.GridFlow([footer], 8, 1, 1, 'center')

    # Layout
    layout = urwid.Frame(
        body,
        header=header,
        footer=footer,
        focus_part='footer'
    )

    return layout


def get_config_file_paths():
    """Find config file paths.

    The first config file that is found is used, it is searched for (in
    this order), at:
     - config, if set (e.g. from the cli)
     - from the default source path (./papersurfer.conf)
     - home config path (system-dependent,
        see https://pypi.org/project/xdgappdirs/ for details)
     - system path (system-dependent,
        see https://pypi.org/project/xdgappdirs/ for details)

    >>> type(get_config_file_paths())
    <class 'list'>
    """
    appdir = AppDirs("papersurfer")
    paths = [appdir.site_config_dir, appdir.user_config_dir, "./"]
    default_filename = "papersurfer.conf"

    return [os.path.join(p, default_filename) for p in paths]


def get_log_file_path():
    """Get log file path."""
    path = AppDirs("papersurfer").user_log_dir
    default_filename = "papersurfer.log"

    return os.path.join(path, default_filename)


def interactive_configuration():
    """Query user for credentials."""
    url = input("Mattermost URL (eg. mattermost.example.net): ")
    channel = input("Channel (eg. Paper Club): ")
    username = input("Username (same as mattermost login, "
                     "eg. JohnDoe@example.net): ")
    password = input("Password (same as mattermost login, eg. SuperSecret1): ")
    return url, channel, username, password


class PostDialog(urwid.WidgetWrap):
    """Dialog to submit a new paper to mattermost thread.

    UI:
        DOI: [ _________________]
        Generated Message:
            "# # # #  # # # #"

        [Submit]       [Close]
    """
    def __init__(self, mattermost, close, loop):
        self._loop = loop
        self.alarm_handle = None

        self.doi = None
        self.msg = None
        self.mattermost = mattermost
        self.close = close
        self.doi_input = urwid.Edit("Doi: ")
        urwid.connect_signal(self.doi_input, 'change', self.h_input)
        self.doi_result = urwid.Text("")

        body_pile = urwid.Pile([
            self.doi_input,
            urwid.Divider(" "),
            self.doi_result,
            urwid.Divider(" "),
            urwid.Columns([
                PrettyButton("Close", self.close),
                PrettyButton("Submit", self.submit)
            ]),
        ])
        body_filler = urwid.Filler(body_pile, valign='top')
        body_padding = urwid.Padding(
            body_filler,
            left=1,
            right=1
        )
        body = urwid.LineBox(body_padding)
        frame = urwid.Frame(body,
                            header=urwid.Text("Submit new paper to list"))

        self.widget = frame

        super().__init__(self.widget)

    def submit(self, _):
        """Submit post to thread."""
        if not self.mattermost.check_doi_exits(self.doi):
            self.mattermost.post(self.msg)
        self.close(_)

    def create_mgs(self, paper):
        """Format post message."""
        msg = f"""\
{paper.title}
{paper.authors}
{paper.journal} [{paper.slug}]
{Doi().get_doi_link(paper.doi)}"""
        return msg

    def h_input(self, _, doi):
        """Handle doi input field and debounce."""
        self.doi_result.set_text("")
        self.doi = None
        self.msg = None

        self._loop.remove_alarm(self.alarm_handle)
        self.alarm_handle = self._loop.set_alarm_in(.5, self.search_doi, doi)

    def search_doi(self, _loop, doi):
        """Trigger search for paper ref by doi and update ui."""
        self.doi_result.set_text("... loading ...")
        self._loop.draw_screen()
        if Doi().extract_doi(doi):
            paper = Doi().get_info(doi)
            if paper:
                if self.mattermost.check_doi_exits(doi):
                    self.doi_result.set_text(f"{self.create_mgs(paper)} \n"
                                             "-> Paper already posted! <-")
                else:
                    self.doi_result.set_text(self.create_mgs(paper))
                    self.doi = doi
                    self.msg = self.create_mgs(paper)
            else:
                self.doi_result.set_text("Doi not found.")
            return

        self.doi_result.set_text("invalid doi")


def get_version():
    """Get version number from static version text file."""
    pkgbase = pathlib.Path(__file__).parent
    with open(f"{pkgbase}/_version.txt", "r") as versionfile:
        return versionfile.read()


def print_paths():
    """Get paths of config, log and data files."""
    paths = get_config_file_paths()
    paths.append(get_log_file_path())
    paths.append(config.datadir)
    paths = [p for p in paths if os.path.exists(p)]
    print("\n".join(paths))


def parse_args():
    """Parse command line arguments and config file."""
    parser = configargparse.ArgParser(
        default_config_files=get_config_file_paths())
    parser.add("-w", "--write-out-config-file",
               help="takes the current command line args and writes them out "
                    "to a config file at the given path",
               is_write_out_config_file_arg=True)
    parser.add('-c', '--my-config', required=False, is_config_file=True,
               help='config file path')
    parser.add('--url', required=False, help='Mattermost url')
    parser.add('--channel', required=False, help='Mattermost channel')
    parser.add('-u', '--username', required=False, help='Mattermost username')
    parser.add('-p', '--password', required=False, help='Mattermost password')
    parser.add('--dump-posts', action='store_true',
               help="Dump mattermost paper posts to stdout and exit")
    parser.add('--dump-bibtex', action='store_true',
               help="Dump bibtex collection to stdout and exit")
    parser.add('--version', action='version', version=get_version())
    parser.add("--debug", action="store_true",
               help="Print debug messages and dump debug data files")
    parser.add('--paths', action="store_true",
               help="Print config and data paths and exit")
    parser.add('--datadir', default=AppDirs("papersurfer").user_data_dir,
               help='Path to datafiles.')

    options = parser.parse_args()

    config.debug = options.debug

    pathlib.Path(options.datadir).mkdir(parents=True, exist_ok=True)
    config.datadir = options.datadir

    if options.paths:
        print_paths()
        sys.exit(0)

    if not options.url:
        start_interactive = input(
            "Could not load config file or read command line arguments, do you"
            " wish to start the interactive configuration assistant? (y/n) ")
        if start_interactive == "y":
            url, channel, username, password = interactive_configuration()
            try:
                Mattermost(url, channel, username, password)
            except ConfigError:
                print("Failed to validate configuration, exiting.")
                sys.exit(1)

            options.url = url
            options.channel = channel
            options.username = username
            options.password = password
            configpath = AppDirs("papersurfer").user_config_dir

            pathlib.Path(configpath).mkdir(parents=True, exist_ok=True)

            configfile = os.path.join(configpath, "papersurfer.conf")
            with open(configfile, "w") as file:
                file.write(f"url = {url}\n")
                file.write(f"channel = {channel}\n")
                file.write(f"username = {username}\n")
                file.write(f"password = {password}\n")
                print(f"Configfile {configfile} written.")

            time.sleep(2)
        else:
            parser.print_help()
            sys.exit(0)

    return options


def just_posts(url, channel, username, password):
    """Fuck off with all this interactive shit."""
    posts = Papersurfer(url, channel, username, password).get_posts()
    for post in posts:
        print(post.message)


def just_bibtex(url, channel, username, password):
    """Retrieve and dump bibtext formated data, unfiltered."""
    posts = Papersurfer(url, channel, username, password).get_posts()
    dois = [post.doi for post in posts]
    print(Bibtex().bib_from_dois(dois))


def main():
    """Run main program."""
    opt = parse_args()

    logfile = get_log_file_path()
    pathlib.Path(os.path.dirname(logfile)).mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename=logfile, level=logging.DEBUG)

    if opt.dump_posts:
        just_posts(opt.url, opt.channel, opt.username, opt.password)
    elif opt.dump_bibtex:
        just_bibtex(opt.url, opt.channel, opt.username, opt.password)
    else:
        PapersurferUi(opt.url, opt.channel, opt.username, opt.password)


if __name__ == "__main__":
    main()
