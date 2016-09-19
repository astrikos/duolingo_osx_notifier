#!/usr/bin/env python
import sys
import time
import signal
import argparse
import subprocess
from Foundation import NSUserNotification, NSUserNotificationCenter, NSObject


class Notification(NSObject):
    def notify(self, title, subtitle, text):
        notification = NSUserNotification.alloc().init()
        notification.setTitle_(title)
        notification.setSubtitle_(subtitle)
        notification.setInformativeText_(text)
        NSUserNotificationCenter.defaultUserNotificationCenter().\
            setDelegate_(self)
        NSUserNotificationCenter.defaultUserNotificationCenter().\
            scheduleNotification_(notification)


class DictFile(object):
    """Class responsble for file that holds our dictionary."""
    def __init__(self, filename, separator="="):
        self.filename = filename
        self.separator = separator
        self.total_lines = None
        self.already_selected = []
        self.selected_line_index = 0
        self.word = ""
        self.meaning = ""
        self.blank_lines = []
        self.comments = []
        self.malformed = []
        self._init()

    def _init(self):
        self.total_lines = self.get_total_lines()

    def calculate_word_and_meaning(self):
        sline = ""
        with open(self.filename) as fp:
            for i, line in enumerate(fp):
                if (
                    i in self.blank_lines or
                    i in self.comments or
                    i in self.malformed
                ):
                    continue
                if line.startswith("#"):
                    self.comments.append(i)
                    continue
                line = line.strip()
                if not line:
                    self.blank_lines.append(i)
                    continue
                if i > self.selected_line_index:
                    sline = line
                    self.already_selected.append(i)
                if i == self.selected_line_index:
                    sline = line
                    self.already_selected.append(i)

                if sline:
                    if not self.extract_word_and_meaning(line):
                        self.malformed.append(i)
                    else:
                        break

    def extract_word_and_meaning(self, line):
        line = line.split(self.separator, 2)
        try:
            self.word = line[0].strip()
            self.meaning = line[1].strip()
        except IndexError:
            return False

        return True

    def get_total_lines(self):
        if self.total_lines is None:
            out = subprocess.Popen(
                ['wc', '-l', self.filename],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            ).communicate()[0]
            self.total_lines = int(out.split()[0])
        return self.total_lines

    def select_line_by_index(self):
        t = int(time.time())
        selected_line_index = t % self.total_lines
        self.already_selected.append(selected_line_index)
        self.selected_line_index = selected_line_index


def notify(title="Word Of The Day", text=""):
    notify_obj = Notification.alloc().init()
    notify_obj.notify(title, "", text)


def cancel(signum, frame):
    print 'Got signal {}: shutdown requested'.format(signum)
    sys.exit(0)


def main():

    parser = argparse.ArgumentParser(
        description="",
        prog="repeat.py {}"
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=int,
        action="store",
        default=3600,
        help="The interval between notifications, e.g. 3600 # an hour"
    )

    parser.add_argument(
        "-f",
        "--filename",
        type=str,
        required=True,
        action="store",
        help="The filename where words/definitions are located."
    )
    arguments = parser.parse_args(sys.argv[1:])
    my_file = arguments.filename
    interval = arguments.interval

    signal.signal(signal.SIGINT, cancel)
    signal.signal(signal.SIGTERM, cancel)

    df = DictFile(my_file)

    while True:
        df.select_line_by_index()
        df.calculate_word_and_meaning()
        text = "{} : {}".format(df.word, df.meaning)
        notify(text=text)
        time.sleep(interval)

if __name__ == "__main__":
    sys.exit(main())
