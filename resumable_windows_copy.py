#!/usr/bin/env python
# resumable file copying for windows
# step 1: compare src/destiny directory
# step 2: based on result from step 1, copy all the files
#         that are different/missing in destiny directory

import os, sys, argparse, math, pprint, time
from os.path import join, getsize
from shutil import *

def gen_filelist(directory=None):
    filelist = {}
    sum0=0
    try:
        os.chdir('{0}'.format(directory))
        if args.verbose: print("Current working dir : %s" % os.getcwd())
        for dir_name, sub_dirs, files in os.walk(directory):
            for f in files:                
                file_full_name = os.path.join(dir_name,f)        
                fsize = getsize(file_full_name)
                shortened_dir = dir_name[len(directory):]
                shortened_filename = os.path.join(shortened_dir, f)
                filelist[shortened_filename] = fsize
                sum0 += fsize             
    except OSError as err:
        # handle error (see below)
        print(err)
    return filelist

def cpfile(f,source_dir,destiny_dir):
    src_file = os.sep.join([source_dir, f])
    dst_file = os.sep.join([destiny_dir, f])
    dst_dir = os.path.dirname(dst_file)

    #print('copying from {0} to {1} {2}'.format(src_file, dst_dir, dst_file))
    
    try:
        if not os.path.isdir(dst_dir):
            os.makedirs(dst_dir, mode=0o777, exist_ok=True)
    except OSError as err:
        print(err)

    try:
        copy2(src_file, dst_file)
    except OSError as err:
        # handle error (see below)
        print(err)

if __name__ == '__main__':
    if sys.version_info < (3, 3):
        raise "must use python 3.3 or greater"
    parser = argparse.ArgumentParser(description='Resumable file copying for windows.'
                                     ' If copying is terminated before completion,'
                                     ' you can rerun it to resume copying from where it'
                                     ' was last left off.')
    parser.add_argument('--source', help='Source directory of data', required=True)
    parser.add_argument('--destiny',
                        help='Destiny directory. '
                             'data will be backed up in the \'pukcab\' subdirectory '
                             '(** \'pukcab\' is the reverse of the word \'backup\' '
                             'to avoid possible naming collision)',
                        required=True)
    parser.add_argument('--check',
                        help='Only list what needs to be copied, not actual copying',
                        action='store_true')
    parser.add_argument('--verbose',
		action='store_true', help='Verbose mode, print more info')

    args = parser.parse_args()

    # step 1: compare source and desitny directory, generate a list
    # of files that have a different size from destiny folder or simply
    # missing there

    filelist_src = {}
    source_dir = args.source
    if args.destiny.find(os.sep) > 0:
        destiny_dir = os.path.join(args.destiny,'backup'[::-1])
    else:
        destiny_dir = os.path.join(args.destiny,os.sep,'backup'[::-1])
        
    if args.verbose: print('destiny: {0}'.format(destiny_dir))

    if not os.path.isdir(source_dir):
        print('source directory {0} does not exist !'.format(source_dir))
        sys.exit(0)

    if not os.path.isdir(destiny_dir):
        os.makedirs(destiny_dir, mode=0o777, exist_ok=True)
    
    filelist_src = gen_filelist(args.source)
    filelist_dest = gen_filelist(destiny_dir)

    diff_files = [ item for item in filelist_src if item not in filelist_dest
               or filelist_src[item] !=filelist_dest[item] ]

    if args.verbose or args.check:           
        pp = pprint.PrettyPrinter(indent=4)
        try:
            pp.pprint(diff_files)
            print('\nA total of {0} files shown above need to be copied'
                  ' from {1} to {2}'.format(len(diff_files),source_dir,destiny_dir))
                       
        except:
            #print('error printing some characters')
            pass
        
    if args.check: sys.exit(0)
    
    # step 2: copy over the files that are missing in destiny directory
    #for f in diff_files:

    os.chdir('{0}'.format(destiny_dir))
    #if args.verbose: print("Current working dir : %s" % os.getcwd())

    total_data = 0
    for f in diff_files:
        total_data += filelist_src[f]
    n = len(diff_files)
    marks = []
    for i in range(1,10):
        marks.append(int(math.floor(i*n/10)))

    if sys.platform[:3] == 'win':
        timefunc = time.clock
    else:
        timefunc = time.time
        
    start = timefunc()    
    try:
        sum0=0
        count=0
        for f in diff_files:
            # show we are copying a big file
            if filelist_src[f] > 524288000:
                print('copying {0}. Wow, this is a big file {1:.2f} megabytes, will take some time ...'.
                      format(f, filelist_src[f]/1024/1024)) 
            cpfile(f, source_dir, destiny_dir)
            if filelist_src[f] > 524288000:
                print('Whew, that is long! moving on to the next ...\n')
            sum0 += filelist_src[f]
            count += 1
            
            if count in marks:
                #print('{0}'.format(f))
                print('{0:.2f} out of {1:.2f} megabytes OR {2:.2f}% copied'.
                      format(sum0/1024/1024, total_data/1024/1024, sum0*100/total_data))
                print('{0} out of {1} files copied\n'.format(count, n))
    except KeyboardInterrupt: sys.exit(0)

    elapsed = timefunc() - start
    
    print('\n{0} out of {1} files copied in {2:.2f} seconds\n'.format(count, n, elapsed))
    print('\ndone! \ncheck your data backup in the directory {0}'.format(destiny_dir))
