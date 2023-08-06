from convisoappsec.flowcli.sast.run import run, command

sast = run
sast.epilog = 'Use command \"{0}\" instead of this one'.format(command)
