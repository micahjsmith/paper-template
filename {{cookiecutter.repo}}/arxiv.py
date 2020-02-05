#!/usr/bin/env python3

import pathlib
import re
import shutil
import sys
from textwrap import dedent

import ply.lex

def get_deps_file():
    # TODO recover actual builddir
    with open('./latexmkrc', 'r') as f:
        lines = f.readlines()
    for line in lines:
        if 'deps_file' in line:
            pass

    return pathlib.Path('.', 'build', 'deps')


def remove_trailing_backslash(s):
    if s[-1] == '\\':
        return s[:-1]
    else:
        return s


def strip_comments(source):
    """Strip comments from LaTeX source files

    Adapated from:
    <https://tex.stackexchange.com/a/214637> by Adam Merberg
    """

    tokens = (
        'PERCENT',
        'BEGINCOMMENT', 'ENDCOMMENT',
        'BACKSLASH',
        'CHAR',
        'BEGINVERBATIM', 'ENDVERBATIM',
        'BEGINLISTING', 'ENDLISTING',
        'NEWLINE',
        'ESCPCT',
    )
    states = (
        ('linecomment', 'exclusive'),
        ('commentenv', 'exclusive'),
        ('verbatim', 'exclusive'),
        ('listing', 'exclusive'),
    )

    #Deal with escaped backslashes, so we don't think they're escaping %.
    def t_BACKSLASH(t):
        r"\\\\"
        return t

    #One-line comments
    def t_PERCENT(t):
        r"\%"
        t.lexer.begin("linecomment")
        return None

    #Escaped percent signs
    def t_ESCPCT(t):
        r"\\\%"
        return t

    #Comment environment, as defined by verbatim package
    def t_BEGINCOMMENT(t):
        r"\\begin\s*{\s*comment\s*}"
        t.lexer.begin("commentenv")
        return None

    #Verbatim environment (different treatment of comments within)
    def t_BEGINVERBATIM(t):
        r"\\begin\s*{\s*verbatim\s*}"
        t.lexer.begin("verbatim")
        return t

    #Listings environment (different treatment of comments within)
    def t_BEGINLISTING(t):
        r"\\begin\s*{\s*lstlisting\s*}"
        t.lexer.begin("listing")
        return t

    #Any other character in initial state we leave alone
    def t_CHAR(t):
        r"."
        return t

    def t_NEWLINE(t):
        r"\n"
        return t

    #End comment environment
    def t_commentenv_ENDCOMMENT(t):
        r"\\end\s*{\s*comment\s*}"
        #Anything after \end{comment} on a line is ignored!
        t.lexer.begin('linecomment')
        return None

    #Ignore comments of comment environment
    def t_commentenv_CHAR(t):
        r"."
        return None

    def t_commentenv_NEWLINE(t):
        r"\n"
        return None

    #End of verbatim environment
    def t_verbatim_ENDVERBATIM(t):
        r"\\end\s*{\s*verbatim\s*}"
        t.lexer.begin('INITIAL')
        return t

    #End of listing environment
    def t_listing_ENDLISTING(t):
        r"\\end\s*{\s*lstlisting\s*}"
        t.lexer.begin('INITIAL')
        return t

    #Leave contents of verbatim/listing environment alone
    def t_verbatim_listing_CHAR(t):
        r"."
        return t

    def t_verbatim_listing_NEWLINE(t):
        r"\n"
        return t


    #End a % comment when we get to a new line
    def t_linecomment_ENDCOMMENT(t):
        r"\n"
        t.lexer.begin("INITIAL")
        #Newline at the end of a line comment is stripped.
        return None

    #Ignore anything after a % on a line
    def t_linecomment_CHAR(t):
        r"."
        return None

    #Print errors
    def t_ANY_error(t):
        print(t.value, file=sys.stderr)

    lexer = ply.lex.lex()
    lexer.input(source)
    return u"".join([tok.value for tok in lexer])


def main():

    # make arxiv dir
    arxivdir = pathlib.Path('.', 'arxiv')

    # open deps file and find matches
    depsfile = get_deps_file()
    with depsfile.open('r') as f:
        # skip two lines
        for _ in range(2):
            f.readline()

        # now skip until path doesn't start with leading /
        while True:
            line = f.readline()
            line = line.strip()
            if line[0] != '/':
                break

        deps = [remove_trailing_backslash(line)]

        # now read until #===End
        while True:
            line = f.readline()
            line = line.strip()
            if line.startswith('#===End'):
                break
            else:
                deps.append(remove_trailing_backslash(line))


    assert deps


    # copy matches to new subdirectory
    for dep in deps:
        src = pathlib.Path(dep)
        dst = arxivdir.joinpath(dep)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)

    # create makefile
    with arxivdir.joinpath('Makefile').open('w') as f:
        f.write(dedent('''\
            .PHONY: main
            main:
            \tlatexmk -shell-escape -bibtex -pdf main

            .PHONY: clean
            clean:
            \tlatexmk -C main
        '''))

    # remove comments from all files
    for dep in deps:
        p = arxivdir.joinpath(dep)
        if p.suffix != '.tex':
            print(f'Skipping {p}')
            continue

        print(f'Stripping comments from {p}...')
        with p.open('r') as f:
            content = f.read()
        content = strip_comments(content)
        with p.open('w') as f:
            f.write(content)


if __name__ == '__main__':
    main()
