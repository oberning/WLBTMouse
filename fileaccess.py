import configparser

class FileReader:

    def __init__(self, reg_file, info_file):
        self.config = configparser.ConfigParser()
        self._info_file(info_file)
        self.reg_content = self._reg_file(reg_file)
        if not self._is_valid_reg():
            print('Not a supported Windows Registry file! Aborting.')
            exit(1)

    def _info_file(self, file_path):
        try:
            self.config.read(file_path)
        except FileNotFoundError:
            print("Path to the bluetooth info file '%s' not found" % file_path)

    def _reg_file(self, file_path):
        try:
            with open(file_path, encoding='utf-16') as f:
                return f.read().splitlines()
        except FileNotFoundError:
            print("Path to registry file '%s' not found." % file_path)
    
    def _is_valid_reg(self):
        if self.reg_content[0] == 'Windows Registry Editor Version 5.00':
            return True
        return False
