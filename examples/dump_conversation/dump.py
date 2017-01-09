import datetime
from argparse import ArgumentParser
from codecs import open as copen
from unicodecsv import writer
import pynder
from pynder.session import Session


ID = FILL_THIS_IN
FB_TOKEN = FILL_THIS_IN


def select_interactively(matches, name):
    print "Found {n} matches with name: '{n}'".format(n=name)
    N = len(matches)
    if N == 0:
        raise SystemExit("Please try with a different name")
    elif N == 1:
        return matches[0]
    selected = None
    while selected not in range(N):
        for i, m in enumerate(matches):
            print "[{i}]\t{n}\t(ID #{id})".format(i=i, n=m.user.name, id=m.user.id)
        print "Select one of the above listed matches"
        try:
            return matches[int(raw_input("> "))]
        except Exception as e:
            print e


if __name__ == "__main__":
    ap = ArgumentParser(description="Dump the conversation with a match into CSV format")
    ap.add_argument("name", help="Name of match")
    args = ap.parse_args()

    s = Session(facebook_id=ID, facebook_token=FB_TOKEN)

    matches = [m for m in s.matches() if m.user is not None and m.user.name == args.name]
    match =  select_interactively(matches, args.name)

    output_filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_") + args.name + ".csv"

    with copen(output_filename, 'w') as fh:
        w = writer(fh)
        for m in match.messages:
            w.writerow([m._data['sent_date'], m.sender, m.body])

    print "Wrote:", output_filename
