resumable_windows_copy
======================

Resumable file copying for windows. If copying is interrupted before completion, 
you can rerun it to resume copying from where it was left off.

Motivation:
I was getting a new laptop. To move the old files onto the new laptop I had to babysit it: 
just to click buttons to confirm this and that. At one time, I had to interrupt my copy, 
then I had to start all over again - since I don't know which files have been copied.

With this script, you run it at command prompt.
* It compares source with desitiny, copy only files not copied yet.
* Optionally run in 'check' mode before doing the real copy.
* You will see the progress of your copying.

Warning:
----------------------
The backup will be copied to a new directory called 'pukcab' under the specified desitiny
directory.

Requirements:
----------------------
* only tested on windows
* for 32 bit machine [python 3.3 x86] (http://www.python.org/ftp/python/3.3.2/python-3.3.2.msi)
* for 64 bit machine [python 3.3 x86-64] (http://www.python.org/ftp/python/3.3.2/python-3.3.2.amd64.msi)

Usage:
----------------------
      C:\Python3.3\python d:\scripts\resumable_windows_copy -h
      usage: resumable_windows_copy.py [-h] --source SOURCE --destiny DESTINY
                                       [--check] [--verbose]

      Resume file copying for windows. If copying is terminated before
      completion, you can rerun it to resume copying from where it was last left off.

      optional arguments:
        -h, --help         show this help message and exit
        --source SOURCE    Source directory of data
        --destiny DESTINY  Destiny directory. data will be backed up in the 'pukcab'
                           subdirectory (** 'pukcab' is the reverse of the word
                           'backup' to avoid possible naming collision)
        --check            Only list what needs to be copied, not actual copying
        --verbose          Verbose mode, print more info

Example:
---------------------
After you downloaded the windows python msi file, run it and get the path to it. After that run:
C:\Python33\python D:\tmp\resumable_windows_copy.py --source D:\Ubuntu11 --destiny C:

#
