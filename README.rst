===============================
vim2vim
===============================

.. .. image:: https://badge.fury.io/py/vim2vim.png
..    :target: http://badge.fury.io/py/vim2vim
..     
.. .. image:: https://travis-ci.org/westurner/vim2vim.png?branch=master
..        :target: https://travis-ci.org/westurner/vim2vim
..
.. .. image:: https://pypip.in/d/vim2vim/badge.png
..        :target: https://crate.io/packages/vim2vim?version=latest


Utility for working with vim colorschemes.

* Free software: BSD license
* Documentation: https://github.com/westurner/vim2vim/blob/master/vim2vim/vim2vim.py

``vim2vim`` transforms output from ``:highlight``,
to a flat, plain ViM colorscheme.

Many ViM colorschemes and extensions utilize various functions for
configuring syntax highlighting. This utility works with ViM's
final, configured state.

Usage
------
1. (ViM) Write ``:highlight`` output to a file::

    :redir > vim_highlight_output.txt
    :highlight
    :redir END

2. (vim2vim) Transform vim ``:highlight`` colors to vim color syntax::

    python ./vim2vim/vim2vim.py | sort > my_colorscheme.vim

    vim2vim ./vim_highlight_output.txt | sort > my_colorscheme.vim
    

.. note:: Does not correctly tokenize multi-word font settings,
   requiring manual removal of `font=multi word font` settings
   from <vim_highlight_output.txt>
   for the time being. #TODO
