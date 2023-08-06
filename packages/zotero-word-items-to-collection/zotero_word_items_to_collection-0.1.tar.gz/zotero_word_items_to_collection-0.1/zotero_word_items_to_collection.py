#!/usr/bin/env python3

import zipfile
import re

from pyzotero import zotero


def items_from_docx(file):
    document = zipfile.ZipFile(file)
    xmldoc = document.read('word/document.xml')
    r = re.compile(r"zotero.org/(?P<type>[a-z]+)/(?P<library_id>[0-9]+)/items/(?P<id>[A-Za-z0-9]+)")
    nu_items = [m.groupdict() for m in r.finditer(xmldoc.decode())]
    items = list({v['id']: v for v in nu_items}.values())
    print("Found %s items." % len(items))
    return items


def zotero_collection_from_items(items, collection_name, **connection):
    zot = zotero.Zotero(**connection)
    collection = zot.create_collections([{'name': collection_name}])["success"]["0"]
    print("Adding to collection %s..." % collection_name)
    li = len(items)
    for i, it in enumerate(items):
        zot.addto_collection(collection, zot.item(it))
        print("%i/%i" % (i+1, li))
    return


def main():
    import argparse
    import os
    parser = argparse.ArgumentParser(
        description="Create a collection from items added to a Word .docx file"
        " via the Word Zotero Integration")
    parser.add_argument('file', help="The .docx file path.")
    parser.add_argument("collection", help="Name of new collection to create.")
    parser.add_argument("--api-key", help="A Zotero API key with write permissions. "
                        "Create here (after login): https://www.zotero.org/settings/keys/new")
    parser.add_argument("--library-id", default="infer", help="The library ID if different to "
                        "the one used to add the items (See top of table here 'Your userID "
                        "for use in API calls': https://www.zotero.org/settings/keys).")
    parser.add_argument("--library-type", default="user")
    parser.add_argument("-n", "--dry-run", action="store_true", default=False,
                        help="Only retrieve items from file and try opening Zotero API connection.")
    args = parser.parse_args()

    apikeyfile = os.path.expanduser("~/.zotero_api_key")
    if os.path.exists(apikeyfile):
        with open(apikeyfile) as f:
            args.api_key = f.read().strip()
        print('Using Zotero API key in %s' % apikeyfile) 
    elif not args.api_key:
        print("You need to either parse --api-key or put one into %s" % apikeyfile)
        return

    items = items_from_docx(args.file)
    connection = {d: getattr(args, d) for d in ['library_id', 'library_type', 'api_key']}
    if len(items) > 0:
        if connection['library_id'] == "infer":
            lid = [i['library_id'] for i in items][0]
            connection['library_id'] = lid
        if args.dry_run:
            zot = zotero.Zotero(**connection)
        else:
            zotero_collection_from_items([i['id'] for i in items],
                                         args.collection, **connection)

if __name__ == "__main__":
    main()