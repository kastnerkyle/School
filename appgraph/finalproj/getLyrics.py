#!/usr/bin/python
import sys
import signal
import PyQt4.QtCore as qtc
import PyQt4.QtGui as qtg
from PyQt4.QtWebKit import QWebPage as qwp
import HTMLParser
import re

class Render(qwp):
    def __init__(self, url):
        self.app = qtg.QApplication(sys.argv)
        qwp.__init__(self)
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.connect(self,
                     qtc.SIGNAL('loadFinished(bool)'),
                     self._finished_loading)
        self.mainFrame().load(qtc.QUrl(url))
        self.app.exec_()

    def _finished_loading(self, result):
        self.html = self.mainFrame().toHtml()
        self.app.quit()

class ParseLyrics(HTMLParser.HTMLParser):
    def __init__(self):
       HTMLParser.HTMLParser.__init__(self)
       self.recording = 0
       self.data = []

    def handle_starttag(self, tag, attributes):
        if tag != "div":
            return
        if self.recording:
           self.recording += 1
        for name, value in attributes:
            if name == "class" and value == "lyricbox":
                break
            else:
                return
        self.recording = 1
    
    def handle_endtag(self, tag):
        if tag == "div" and self.recording:
            self.recording -= 1

    def handle_data(self, data):
        if self.recording:
            self.data.append(data)

if __name__=="__main__":
    url = sys.argv[1]
    javascript_html = Render(url).html
    final_html = unicode(javascript_html).encode("utf-8")
    #Get approximate lyrics (all html inside lyricbox tag)
    p = ParseLyrics()
    p.feed(final_html)
    #Remove unwanted newlines and tabs, and join as a giant string
    unfiltered_lyrics = " ".join(filter(lambda x: x != "\t" and x != "\n", p.data))
    #Split based on the ringtone tag using non-greedy matching
    filtered_lyrics = re.split("Send.*?Cell", unfiltered_lyrics)
    #Center of array should hold lyrics
    print filtered_lyrics[1]
