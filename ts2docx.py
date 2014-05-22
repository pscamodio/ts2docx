from os import path
import argparse

from docx import Document

from pyqtts import tsfile


parser = argparse.ArgumentParser(description='Create docx file from ts file')
parser.add_argument('input', type=str, help='input ts file')
parser.add_argument('-o', '--output', dest="output", type=str, help='output doc file')
parser.add_argument('--light', action="store_true", dest="light", default=False,
                    help='insert only unfinished  and not obsolete translations')


def append_text_to_cell(cell, text):
    cell.text = text


def my_strip(s):
    if s:
        return "".join(s.split())
    else:
        return ""


def main():
    args = parser.parse_args()
    if not args.output:
        args.output = path.splitext(args.input)[0] + ".docx"

    print("Opening ts file: " + args.input)
    f = tsfile.tsfile()
    try:
        f.load_file(args.input)
    except Exception as err:
        print("Unable to open " + args.input)
        exit(-1)

    print("Preparing translations")
    num_translations = 0
    num_conflicts = 0
    translations = {}
    keys = []
    for context in f.context_list:
        for message in context.message_list:
            if args.light and message.translation.status in ["finished", "obsolete"]:
                continue
            result = ""
            if message.translation:
                result = message.translation.text or ""
            key = my_strip(context.name) + my_strip(message.source)
            translations[key] = result
            if not message.source in keys:
                keys.append((context.name, message.source))
            message.translation.text = ""
    print("Identified " + str(len(keys)) + " translations")
    print("Generating docx")
    doc = Document("template.docx")
    table = doc.tables[0]
    for context, source in keys:
        row = table.add_row().cells
        append_text_to_cell(row[0], context or "")
        append_text_to_cell(row[1], source or "")
        key = my_strip(context) + my_strip(source)
        append_text_to_cell(row[2], translations[key] or "")
    print("Saving output: " + args.output)
    doc.save(args.output)


if __name__ == "__main__":
    main()