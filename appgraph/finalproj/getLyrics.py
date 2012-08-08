#!/usr/bin/python
import sys
import signal
import PyQt4.QtCore as qtc
import PyQt4.QtGui as qtg
from PyQt4.QtWebKit import QWebPage as qwp

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

if __name__=="__main__":
    url = sys.argv[1]
    javascript_html = Render(url).html
    print unicode(javascript_html).encode("utf-8")
