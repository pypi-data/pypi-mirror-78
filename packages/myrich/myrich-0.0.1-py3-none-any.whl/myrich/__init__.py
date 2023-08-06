#!/usr/bin/env python
# coding: utf-8

import os
import sys

from .vendor.delegator import run

from rich.console import Console
from rich.markdown import Markdown


def main(argv=None):
    
    console = Console()
    cwd = os.getcwd()
    
    while(True):
        try:
            prompt = '(rich) ' + cwd + '%s' % '>' if os.name == 'nt' else '$'
            command_line = input(prompt)
            
            if(command_line and command_line.strip() == 'exit'):
                break
            
            if (command_line[:2] == 'cd' and
                len(command_line.split(' ', 1)) == 2):
                try:
                    os.chdir(command_line[3:])
                    cwd = os.getcwd()
                    continue
                except FileNotFoundError as err:
                    pass
            elif (command_line[:8] == 'markdown' and
                len(command_line.split(' ', 1)) == 2 and
                os.path.isfile(command_line[9:])):
                with open(command_line[9:]) as md:
                    markdown = Markdown(md.read())
                console.print(markdown)
                continue
            elif  command_line[:6] == 'myrich':
                console.print('No action taken to avoid nested environments',
                              style='bold yellow')
                continue
            
            c = run(command_line, cwd=cwd)
            console.print(c.out)
            
            if c.err:
                console.print(c.err, style='bold red')
        except KeyboardInterrupt:
            sys.exit(
                console.print('\nERROR: Interrupted by user', style='bold red')
            )
    
    console.print('Bye :waving_hand:')


__all__ = ['main']