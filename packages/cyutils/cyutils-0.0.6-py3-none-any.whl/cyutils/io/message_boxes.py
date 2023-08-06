import subprocess, os, sys
from tempfile import TemporaryDirectory
from cyutils import exception_handler as eh

def message_box(title, content, args=''):
    if os.name == 'nt':
        with TemporaryDirectory() as temp_dir:
            with open(temp_dir + '\\data.vbs', 'w') as f:
                f.write('x=MsgBox("' + content + '", ' + args + ', "' + title + '")')
            subprocess.call('cscript ' + temp_dir + '\\data.vbs', stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
    else:
        sys.excepthook = eh.exceptionHandler
        raise EnvironmentError("message_box is only available for Windows Users.")

