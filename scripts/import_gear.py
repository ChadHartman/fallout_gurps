#!/usr/bin/env python3

import json
import os
# python 3 only
from table_parser import TableParser


def jsonify(rows):
    array = []
    keys = rows[0]
    row_index = 1

    for row in rows[1:]:
        item = {}
        array.append(item)
        if len(keys) != len(row):
            raise Exception("Row #{0}: ({1}) {2} keys for ({3}) {4} items".format(
                row_index,
                len(keys),
                json.dumps(keys),
                len(row),
                json.dumps(row)))
        for i in range(len(keys)):
            item[keys[i]] = row[i]
        row_index += 1

    return array


def parse(outdir, filename):

    if not filename.endswith('.html'):
        return
        
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    parser = TableParser()
    with open(filename, 'r') as f:
        parser.feed("".join(f.readlines()))

    outfile = filename.split("/")[-1]
    # Remove file extension
    outfile = ".".join(outfile.split(".")[:-1])
    outfile = os.path.join(outdir, outfile + ".json")

    try:
        with open(outfile, 'w') as f:
            json.dump(jsonify(parser.rows), f, indent=4, sort_keys=True)
    except Exception as e:
        print("Error prosessing rows of " + outfile)
        print(json.dumps(parser.rows))
        raise e


def main():

    for filename in os.listdir("../assets/armor"):
        parse(
            "../out/armor",
            os.path.join("../assets/armor", filename))

    for filename in os.listdir("../assets/weapons"):
        parse(
            "../out/weapons",
            os.path.join("../assets/weapons", filename))


if __name__ == "__main__":
    main()
