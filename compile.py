#!/usr/bin/python
"""
"""
import os
import shutil
import markdown


SOURCE_DIR = 'src/'
TARGET_DIR = 'out/'
with open('html-template.html') as fd:
    HTML_TEMPLATE = fd.read()


def to_target(path: str, ext=None) -> str:
    assert os.path.exists(path), path
    assert path.startswith(SOURCE_DIR), path
    subpath = path[len(SOURCE_DIR):]
    if ext is not None:  # extension must be modified
        subpath, _ = os.path.splitext(subpath)
        subpath += '.' + ext.lstrip('.')
    return os.path.join(TARGET_DIR, subpath)


def move_files(*, dir_=SOURCE_DIR):
    for entry in os.scandir(dir_):
        if entry.is_dir():
            os.mkdir(to_target(entry.path))
            yield from move_files(dir_=entry.path)
        elif entry.is_file():
            ext = os.path.splitext(entry.path)[1]
            if ext in {'.html', '.css', '.js'}:
                trg = to_target(entry.path)
                shutil.copy(entry.path, trg)
                yield entry.path, trg
            elif ext in {'.md', '.mkd'}:
                trg = to_target(entry.path, ext='html')
                with open(entry.path) as fd:
                    html = HTML_TEMPLATE.format(body=markdown.markdown(fd.read()), title='aspyrine')
                with open(trg, 'w') as fd:
                    fd.write(html)
                yield entry.path, trg
            else:
                raise NotImplementedError(f"Can't handle file {repr(entry.path)} of extension {ext}.")


if __name__ == "__main__":
    for src, trg in move_files():
        print(f'{src} -> {trg}')
    print('compilation done.')
