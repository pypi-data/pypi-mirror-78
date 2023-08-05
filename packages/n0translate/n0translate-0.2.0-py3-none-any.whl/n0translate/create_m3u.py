# -*- coding: utf-8 -*-
import os
import sys
import n0translate
import argparse
#import create_m3u as this # for using functions declared AFTER call
# UNIVERSAL: for using functions declared AFTER call
sys.path.insert(0, os.path.split(__file__)[0]);import importlib;this = importlib.import_module(os.path.splitext(os.path.basename(__file__))[0])

if __name__ == "__main__":
    ext_for_rename = [".mp3", ".ogg"]
    print("*"*70)
    print("Find %s (by default in current dir),\ntranslit their names and create .m3u list '!<current dir>.m3u'" % ext_for_rename)
    print("*"*70)
    # ##############################################################################
    len_sys_argv = len(sys.argv)

    parser = argparse.ArgumentParser(add_help = False)
    # parser.add_argument("start_path", metavar="<start path>",  action="store", default=os.path.abspath(os.getcwd()), help="start renaming from dir (default: current dir)")
    parser.add_argument("start_path", nargs="?", default=os.getcwd(), help="start renaming files %s from dir (default: current dir)" % ext_for_rename)
    parser.add_argument("-f", dest="rename_files", action="store_true", default=False, help="translit and rename files (default: False)")
    parser.add_argument("-d", dest="rename_dirs", action="store_true", default=False, help="translit and rename dirs (default: False)")
    parser.print_help()
    args = parser.parse_args()
    
    args.start_path = os.path.abspath(args.start_path)
    if not args.start_path.endswith(os.path.sep):  args.start_path += os.path.sep # \\ is required for correct trimming
    cur_dirs = list(filter(None, os.path.splitdrive(args.start_path)[1].split(os.path.sep)))
    # Disable to run at root \
    if  not len(cur_dirs)\
        or (
            cur_dirs[0] in ( # Disable in \%dir% an deeper
                "$GetCurrent",
                "$Recycle.Bin",
                "$WinREAgent",
                "Config.Msi",
                "eSupport",
                "Intel",
                "IntelOptaneData",
                "Program Files",
                "Program Files (x86)",
                "ProgramData",
                "Recovery",
                "System Volume Information",
                "Windows",
                "",
            )
        ) \
        or (
            len(cur_dirs) < 3 and
            cur_dirs[0] in (
                "Users",    # Disable in \Users\, \Users\UserName\, but enabled deeper for example C:\Users\UserName\Music\
                "Documents and Settings", # Disable in \Documents and Settings\, \Documents and Settings\UserName\, but enabled deeper for example \Documents and Settings\UserName\Music\
            )
        ) \
    :
        print("=-_-"*18)
        print("Running from '%s' is DISABLED!" % args.start_path)
        print("=-_-"*18)
        sys.exit()
    # ##############################################################################
    # ONLY if -r is set
    # Search all dirs from args.start_path (current dir)
    # and rename them into translited
    # ##############################################################################
    if args.rename_dirs:
        print("*"*70)
        print("Renaming dirs...")
        while True:
            renamed_once = False
            for cur_path, dirnames, filenames in os.walk(args.start_path):
                for dirname in dirnames:
                    translited_name = this.translit_fname(dirname)
                    if translited_name != dirname:
                        src = os.path.join(cur_path, dirname)
                        dst = this.unique_fname(os.path.join(cur_path, translited_name))
                        print("%s => %s" % (src, dst))
                        os.rename(src, dst)
                        renamed_once = True
                if renamed_once:
                    break # Reread all dirs structure again
            else:
                break # Exit from the iternal loop if no need to rename directories
        print("...completed")
    # ##############################################################################
    # Search all files from args.start_path (".\\" == current dir)
    # and rename them into translited
    # ##############################################################################
    if args.rename_files:
        print("*"*70)
        print("Renaming files...")
        for cur_path, dirnames, filenames in os.walk(args.start_path):
            for filename in filenames:
                filename_only, filename_ext = os.path.splitext(filename)
                translited_name = this.translit_fname(filename_only)
                if translited_name != filename_only:
                    filename_only, file_ext = os.path.splitext(filename)
                    if file_ext.lower() in ext_for_rename:
                        src = os.path.join(cur_path, filename)
                        dst = this.unique_fname(os.path.join(cur_path, translited_name+filename_ext))
                        print("%s -> %s" % (src, dst))
                        os.rename(src, dst)
        print("...completed")
        print("*"*70)
    # ##############################################################################
    # Search all files from args.start_path (".\\" == current dir)
    # and generate list for M3U
    # ##############################################################################
    print("*"*70)
    print("Searching for files...")
    files_for_m3u=[]
    for cur_path, dirnames, filenames in os.walk(args.start_path):
        for filename in filenames:
            filename_only, file_ext = os.path.splitext(filename)
            if file_ext.lower() in ext_for_rename:
                files_for_m3u.append(os.path.join(cur_path, filename)[len(args.start_path):])
    print("...completed")
    print("*"*70)
    # ##############################################################################
    # Generate '<current dir>.m3u' as transliterated dir
    # ##############################################################################
    if len(files_for_m3u):
        dst_m3u = this.unique_fname(args.start_path + "!" + this.translit_fname(os.path.basename(args.start_path[:-1])) + ".m3u")
        print("*"*70)
        print("*** Creating: " + dst_m3u)
        print("*"*70)
        with open(dst_m3u, "w") as dst:
            for file in sorted(files_for_m3u):
                # print(file)
                dst.write(file + "\n")
    else:
        print("*** No files %s found in '%s'" % (ext_for_rename, args.start_path))
# ##############################################################################
def translit_fname(original_fname: str):
    translited_fname = original_fname \
        .translate(n0translate.translit_dict) \
        .translate(str.maketrans(" .,'«»`","_______")) \
        .replace("__","_") \
        .replace("(_","(") \
        .replace("_)",")")
    if len(translited_fname) > 1 and  translited_fname.endswith("_"):
        translited_fname = translited_fname[:-1]
    return translited_fname
# ##############################################################################
def unique_fname(original_fname: str):
    postfix=0
    filename_only, filename_ext = os.path.splitext(original_fname)
    while os.path.exists(original_fname):
        original_fname = "%s.%02d%s" % (filename_only, postfix, filename_ext)
        postfix = postfix+1
    return original_fname
