"""Top-level package for procin."""
__author__ = """Powell Quiring"""
__email__ = 'powellquiring@gmail.com'
__version__ = '0.1.0'

import subprocess
import typing
import json
from pathlib import Path
import codecs

class Command:
    def __init__(self, print_output=False, print_error=True, cache=False, cache_dir="~/procin"):
        self.print_output = print_output
        self.print_error = print_error
        self.cache = cache
        self.cache_dir = cache_dir
        if self.cache:
            self.cache_path = Path(self.cache_dir)
            if self.cache_path.exists():
                if not self.cache_path.is_dir():
                    raise NotADirectoryError(self.cache_path)
            else:
                self.cache_path.mkdir()
        self.escape = {'^': '^', '$': 'd', ' ':'s', '\t': 't', '[':'l', ']':'r', '{':'L', '}': 'R', '/': 'f', '\\': 'b'}
        self.unescape = {value: key for (key, value) in self.escape.items()}
        self.unescape['n'] = 'n'

    
    def command_to_filename(self, command):
        """lossless conversion from a command to a file string"""
        filename = ""
        for word in command:
            for c in word:
                ch = c
                if c in self.escape:
                    ch = '^' + self.escape[c]
                filename += ch
            filename += "^n"
        return codecs.encode(filename, 'unicode-escape').decode('ascii')
    
    def filename_to_command(self, filename):
        lines = codecs.decode(filename, 'unicode-escape')
        escape = False
        command = []
        word = ""
        for c in lines:
            if escape:
                c = self.unescape[c]
                if c == 'n':
                    command.append(word)
                    word = ""
                else:
                    word += c
                escape = False
            else:
                if c == '^':
                    escape = True
                else:
                    word += c
        return command

    def file_cache_path(self, command):
        return Path(self.cache_dir) / self.command_to_filename(command)

    def in_cache(self, command):
        """text of the cache hit or None"""
        if self.cache:
            file_cache_path = self.file_cache_path(command)
            if file_cache_path.exists():
                return file_cache_path.read_text()
        return None

    def run_with_cache(self, command):
        stdout = self.in_cache(command)
        if stdout:
            return stdout
        out = subprocess.check_output(command)
        stdout = out.decode()
        if self.cache:
            self.file_cache_path(command).write_text(stdout)
        return stdout

    def run(self, command, catch:bool=False, print_command:bool=False, print_output:bool=False):
        if print_command:
            print(' '.join(command))
        if catch:
            try:
                stdout = self.run_with_cache(command)
            except subprocess.CalledProcessError:
                print('*** Command execution failed')
                stdout = ""
        else:
            stdout = self.run_with_cache(command)
        if print_output:
            print(stdout)
        return stdout

    def run_json(self, command):
        return json.loads(self.run(command))