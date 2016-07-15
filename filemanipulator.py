#!/usr/bin/python2
import tempfile
import sys
import datetime

mit_license = ("""\
/*
MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
""")

class FileModifierError(Exception):
    pass

class FileModifier(object):

    def __init__(self, fname):
        self.__write_dict = {}
        self.__filename = fname
        self.__tempfile = tempfile.TemporaryFile()
        with open(fname, 'rb') as fp:
            for line in fp:
                self.__tempfile.write(line)
        self.__tempfile.seek(0)

    def write(self, s, line_number = 'END'):
        if line_number != 'END' and not isinstance(line_number, (int, float)):
            raise FileModifierError("Line number %s is not a valid number" % line_number)
        try:
            self.__write_dict[line_number].append(s)
        except KeyError:
            self.__write_dict[line_number] = [s]

    def writeline(self, s, line_number = 'END'):
        self.write('%s\n' % s, line_number)

    def writelines(self, s, line_number = 'END'):
        for ln in s:
            self.writeline(s, line_number)

    def __popline(self, index, fp):
        try:
            ilines = self.__write_dict.pop(index)
            for line in ilines:
                fp.write(line)
        except KeyError:
            pass

    def close(self):
        self.__exit__(None, None, None)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        with open(self.__filename,'w') as fp:
            for index, line in enumerate(self.__tempfile.readlines()):
                self.__popline(index, fp)
                fp.write(line)
            for index in sorted(self.__write_dict):
                for line in self.__write_dict[index]:
                    fp.write(line)
        self.__tempfile.close()

filename = sys.argv[1]
#license = sys.argv[1]
print "Licenseadder by Paul Kramme"
with FileModifier(filename) as fp:
	fp.writeline(mit_license, 0)
