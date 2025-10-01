import os

def list_tree(startpath,
              show_files=True,
              use_unicode=True,
              sort=True,
              max_depth=None):
    """
    Print a tree view of startpath.

    Parameters:
      startpath (str): root directory to print
      show_files (bool): include files if True
      use_unicode (bool): use box-drawing characters; set False to use ASCII
      sort (bool): sort entries alphabetically
      max_depth (int|None): maximum depth (0 = only the root). None = unlimited.
    """
    if use_unicode:
        VERT = '│   '
        BRANCH = '├── '
        LAST = '└── '
        SPACE = '    '
    else:
        VERT = '|   '
        BRANCH = '|-- '
        LAST = '`-- '
        SPACE = '    '

    def inner(path, prefix='', depth=0):
        if max_depth is not None and depth > max_depth:
            return

        try:
            entries = os.listdir(path)
        except PermissionError:
            print(prefix + LAST + "[Permission Denied]")
            return

        if sort:
            entries.sort()

        if not show_files:
            entries = [e for e in entries if os.path.isdir(os.path.join(path, e))]

        for i, name in enumerate(entries):
            full = os.path.join(path, name)
            is_last = (i == len(entries) - 1)
            connector = LAST if is_last else BRANCH
            display_name = name + ('/' if os.path.isdir(full) else '')
            print(prefix + connector + display_name)
            if os.path.isdir(full):
                extension = SPACE if is_last else VERT
                inner(full, prefix + extension, depth + 1)

    # nice root name
    root_name = os.path.basename(startpath.rstrip(os.sep)) or startpath
    print(f"{root_name}/")
    inner(startpath, prefix='', depth=0)
