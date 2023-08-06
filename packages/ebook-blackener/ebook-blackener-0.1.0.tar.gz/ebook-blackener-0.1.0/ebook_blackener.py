#!/usr/bin/env python3
"""Ebook blackener.

Usage:
  ebook_blackener.py <input-file> <output-base-name>
"""

import cssutils
import pathlib
import re
import shutil
import zipfile
from docopt import docopt

RE_RULE = re.compile(r'''(.*){(.*)}.*''')

def hack_css_file(css_filename):
    css_content = open(css_filename).read()
    modified_rules = list()

    sheet = cssutils.parseString(css_content)
    for rule in sheet.cssRules:
        rule_text = rule.cssText.replace('\n', '')
        m = RE_RULE.match(rule_text)
        if m:
            prefix = m.group(1)
            inside = m.group(2)
            items = dict()
            for item in [x.strip() for x in inside.split(';')]:
                keyval = item.split(':')
                items[keyval[0].strip()] = keyval[1].strip()
            items['color'] = 'white'
            items['background-color'] = 'black'
            modified_rule = prefix + ' {\n' + ';\n'.join([f'  {k}: {v}' for (k,v) in items.items()]) + '\n}\n'
            modified_rules.append(modified_rule)

    with open(css_filename, 'w') as f:
        f.write(''.join(modified_rules))

def hack_epub(epub_filename, output_base_name, tmp_dir='tmp-ebook-blk'):
    # clear and prepare temporary directory
    shutil.rmtree(tmp_dir, ignore_errors=True)
    pathlib.Path(tmp_dir).mkdir(parents=True, exist_ok=False)

    # unzip epub file
    with zipfile.ZipFile(epub_filename, 'r') as zip_ref:
        zip_ref.extractall(tmp_dir)

    # hack all css files
    for path in pathlib.Path(tmp_dir).rglob('*.css'):
        hack_css_file(path.absolute())

    # zip all files (clean and modified ones) together
    shutil.make_archive(output_base_name, 'zip', tmp_dir)
    # change file extension
    shutil.move(f'{output_base_name}.zip', f'{output_base_name}.epub')

    # remove temporary directory
    shutil.rmtree(tmp_dir, ignore_errors=True)

def main():
    args = docopt(__doc__, version='0.1.0')
    hack_epub(args['<input-file>'], args['<output-base-name>'])

if __name__ == '__main__':
    main()
