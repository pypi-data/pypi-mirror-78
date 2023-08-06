import subprocess

__all__=["BashCall"]

def BashCall(cmdline,sourcefile=None):
    '''
    :param cmdline: cmd strings
    :param sourcefile: additional source file name
    :return: state code of that process
    '''
    if sourcefile==None:
        cmdline = ["bash", "-c", cmdline]
    else:
        cmdline = ["bash", "-c", "source "+sourcefile+";"+cmdline]
    return subprocess.call(cmdline)


