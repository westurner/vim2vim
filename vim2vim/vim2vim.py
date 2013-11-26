#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function
__doc__ = """
vim2vim
=========
`vim2vim` transforms output from `:highlight`,
to a flat, plain ViM colorscheme.

Many ViM colorschemes and extensions utilize various functions for
configuring syntax highlighting. This utility works with ViM's
final, configured state.

Usage
------
1. (ViM) Write `:highlight` output to a file::

    :redir > vim_highlight_output.txt
    :highlight
    :redir END

2. (vim2vim) Transform vim colors to vim color syntax::

    vim2vim ./vim_highlight_output.txt | sort > my_colorscheme.vim

.. note:: Does not correctly tokenize multi-word font settings,
   requiring manual removal of `font=multi word font` settings
   from <vim_highlight_output.txt>
   for the time being. #TODO
"""

from collections import namedtuple
import logging
log = logging.getLogger()

ATTRS = (
    'name',
    'term',
    'cterm',
    'ctermfg',
    'ctermbg',
    'gui',
    'guifg',
    'guibg',
    'guisp', # ?
    'font',
    'link',
    'cleared')
ColorGroup = namedtuple('ColorGroup', ATTRS)

def cg_str(self):
    def _cg_str(self):
        if self.link:
            yield '" '
        yield 'hi '
        if self.cleared:
            yield 'clear '
        yield self.name
        yield ' '
        if self.link:
            yield 'links to %s' % self.link
        else:
            for k,v in self._asdict().iteritems():
                if k in ('name', 'cleared', 'link'):
                    continue
                if v is not None:
                    yield ' %s=%s' % (k,v)
    return str.join('', _cg_str(self))

ColorGroup.__str__ = cg_str


def vim2vim(filename):
    """Transform output from `:highlight` to a flat, plain vim colorscheme.

    """
    with open(filename, 'r') as f:
        for line in f:
            log.debug(line.rstrip())
            l = line.strip()
            if not l or 'xxx' not in l:
                continue
            name, attrs = l.split('xxx')
            name = name.strip()
            attrs = attrs.strip()
            attrdict = dict.fromkeys(ATTRS, None)
            attrdict['name'] = name

            if attrs.startswith('links to'):
                attrdict['link'] = attrs.split('links to ')[-1]
            elif attrs.startswith('cleared'):
                attrdict['cleared'] = True
            else:
                _attrs = [x.split('=',1) for x in attrs.split(' ')]
                try:
                    attrdict.update(_attrs)
                except ValueError:
                    log.error(_attrs)
                    raise

            yield ColorGroup(**attrdict)


def sort_by_name_clear_inline(iterable):
    return sorted(iterable, key=lambda x: (x.name, not x.cleared, not x.link))


def sort_by_name_clear_to_top(iterable):
    return sorted(iterable, key=lambda x: (not x.cleared, x.name, x.link))


import unittest
class Test_vim2vim(unittest.TestCase):
    def test_vim2vim(self):
        import os.path
        filename = os.path.join(
            os.path.dirname(__file__),
            '..',
            'tests',
            'vim_highlight_output.txt')
        print(filename)
        log.info(filename)
        color_groups = vim2vim(filename)
        for group in color_groups:
            log.debug(group)


def main(*args):
    import logging
    import optparse
    import sys

    prs = optparse.OptionParser(
        usage="%prog [-s|-S] <vim_highlight_output.txt>",
        description=vim2vim.__doc__
    )


    prs.add_option('-s', '--sort-by-name-clear-inline',
                    dest='sort_by_name_clear_inline',
                    help='Sort by name w/ "hi clear <name>" lines inline',
                    action='store_true',)

    prs.add_option('-S', '--sort-by-name-clear-to-top',
                    dest='sort_by_name_clear_to_top',
                    help='sort by name w/ "hi clear <name>" lines at the top',
                    action='store_true',)

    prs.add_option('-v', '--verbose',
                    dest='verbose',
                    action='store_true',)
    prs.add_option('-q', '--quiet',
                    dest='quiet',
                    action='store_true',)
    prs.add_option('-t', '--test',
                    dest='run_tests',
                    action='store_true',)

    args = args and list(args) or sys.argv[1:]
    (opts, args) = prs.parse_args(args)

    if not opts.quiet:
        logging.basicConfig()

        if opts.verbose:
            logging.getLogger().setLevel(logging.DEBUG)

    if opts.run_tests:
        import sys
        sys.argv = [sys.argv[0]] + args
        import unittest
        sys.exit(unittest.main())

    if len(args):
        filename = args[0]
        color_groups = vim2vim(filename)
        if opts.sort_by_name_clear_inline:
            color_groups = sort_by_name_clear_inline(color_groups)
        elif opts.sort_by_name_clear_to_top:
            color_groups = sort_by_name_clear_to_top(color_groups)
        for group in color_groups:
            print(group)
    else:
        print(__doc__)
        prs.print_help()


if __name__ == "__main__":
    main()
