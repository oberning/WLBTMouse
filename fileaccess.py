import configparser
import os
import shutil
import pathlib

class FileAccess:

    def __init__(self, reg_file = None, info_file = None):
        self.config = configparser.RawConfigParser()
        self.config.optionxform = lambda option: option
        self.reg_content = ""
        self.info_path = []
        if reg_file != None and info_file != None:
            self._info_file = info_file
            self._reg_file = reg_file
            self._info_last_dir_part()
            self.load(reg_file)        

    def load(self, reg_file):
        self._load_info_file()
        self.reg_content = self._load_reg_file()
        if not self._is_valid_reg():
            print('Not a supported Windows Registry file! Aborting.')
            exit(1)
    
    def save(self, new_config):
        self.backup()
        self.config = new_config
        with open(self._info_file, 'w') as f:
            self.config.write(f)

    def backup(self):
        path = os.path.join(os.sep, *self.info_path[:-2])
        shutil.make_archive(os.path.join(pathlib.Path.home(), "WLBTMouse_backup.zip"), 'zip', path)
    
    def _info_last_dir_part(self):
        info_path = os.path.normpath(self._info_file)
        self.info_path = info_path.split(os.sep)

    def _load_info_file(self):
        try:
            self.config.read(self._info_file)
        except FileNotFoundError:
            print("Path to the bluetooth info file '%s' not found" % self._info_file)
            exit(1)

    def _load_reg_file(self):
        try:
            with open(self._reg_file, encoding='utf-16') as f:
                return f.read().splitlines()
        except FileNotFoundError:
            print("Path to registry file '%s' not found." % self._reg_file)
            exit(1)
    
    def _is_valid_reg(self):
        if self.reg_content[0] == 'Windows Registry Editor Version 5.00':
            return True
        return False
