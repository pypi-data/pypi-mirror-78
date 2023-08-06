import traceback

def exceptionHandler(got_exception_type, got_exception, got_traceback):
    listing  = traceback.format_exception(got_exception_type, got_exception, got_traceback)
    del listing[-2]
    filelist = ["org.python.pydev"]
    listing = [ item for item in listing if len([f for f in filelist if f in item]) == 0 ]
    files = [line for line in listing if line.startswith("  File")]
    if len(files) == 1:
        del listing[0]
    print("".join(listing))