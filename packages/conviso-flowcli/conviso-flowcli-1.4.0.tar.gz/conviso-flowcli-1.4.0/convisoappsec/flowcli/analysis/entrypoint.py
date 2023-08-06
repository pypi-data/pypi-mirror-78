import click

from convisoappsec.flowcli import help_option
from .sast import sast


@click.group(deprecated=True)
@help_option
def analysis():
    '''
    This command will be removed at 01/Aug/2020
    '''
    pass


analysis.add_command(sast, 'sast')

analysis.epilog = '''
  Run flow analysis COMMAND --help for more information on a command.
'''
