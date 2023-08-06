""" 
File for formatting htmlphrase strings. 
Usage:
    > phrase = "<ul><li>cat</li><ul><li>smelly cat</li><li>Happy cat!</li></ul><li>dog</li></ul>"
    > htmlformat.format_phrase(phrase)
    <ul>
      <li>cat</li>
      <ul>
        <li>smelly cat</li>
        <li>Happy cat!</li>
      </ul>
      <li>dog</li>
    </ul>
"""
import textwrap

from html.parser import HTMLParser

class HTMLPhraseFormater(HTMLParser): 
    def __init__(self, tab_num_spaces=2):
        super().__init__()
        self.open_tags = []
        self.out_str = f''
        self.complete = False
        self.just_closed = False
        self.tabs_string = " " * tab_num_spaces

    def handle_starttag(self, tag, attrs):
        self.check_complete()
        self.just_closed = False
        n_tags = len(self.open_tags)
        
        new_line = "" if n_tags == 0 else "\n"
        tabs = self.tabs_string * n_tags
        self.open_tags.append(tag)

        new_str = f'{new_line}{tabs}{self.get_starttag_text()}'

        self.out_str += new_str

    def handle_endtag(self, tag):
        self.check_complete()
        self.open_tags = self.open_tags[:-1]
        n_tags = len(self.open_tags)

        white_space = f''
        if self.just_closed:
            tabs = self.tabs_string * n_tags
            white_space += f'\n{tabs}'
        new_str = f'{white_space}</{tag}>'
        
        if len(self.open_tags) == 0:
            self.complete = True

        self.out_str += new_str

        self.just_closed = True

    def handle_data(self, data):
        self.check_complete()
        self.out_str += data

    def check_complete(self):
        if self.complete == True:
            raise Exception("Input needs to have a single outer tag!")

    def close(self):
        if self.complete == False:
            raise Exception("Incomplete tagging! Check for missing or extra start/end tags!")
        return self.out_str


def format_phrase(phrase):
    parser = HTMLPhraseFormater()
    parser.feed(phrase)
    return parser.close()
