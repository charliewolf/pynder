import datetime
from argparse import ArgumentParser
from codecs import open as copen
from unicodecsv import writer
import pynder
from pynder.session import Session


ID = FILL_THIS_IN
FB_TOKEN = FILL_THIS_IN


def get_match(matches, name):
    for m in matches:
        if m.name == name:
            return m
    raise LookupError("Match '{n}' could not be found".format(n=name))


if __name__ == "__main__":
    ap = ArgumentParser(description="Dump the conversation with a match into CSV format")
    ap.add_argument("name", help="Name of match")
    args = ap.parse_args()
        
    s = Session(ID, FB_TOKEN)
    match = get_match(s.matches(), args.name)
    output_filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_") + args.name + ".csv"

    with copen(output_filename, 'w') as fh:
        w = writer(fh)
        for m in match.messages:
            w.writerow([m._data['sent_date'], m.sender, m.body])

    print "Wrote:", output_filename
