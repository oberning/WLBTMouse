import re

class FileProcessing:

    def __init__(self, file_reader):
        self._reg_content = file_reader.reg_content
        self._config = file_reader.config

    def _find_element(self, search_string):
        result = None
        for element in self._reg_content:
            m = re.search(search_string, element)
            if m:
                break
        if m != None:
            result = m.group(1)
        return result
    
    def _get_proper_hex(self, search_string):
        element = self._find_element(search_string)
        if element:
            value = element.replace(',', '').upper()
        else:
            value = None
        return value

    def ediv(self):
        element = self._find_element("\"EDIV\"=dword:(.*)")
        result = None
        if element:
            result = str(int(element, 16))
        return result

    def long_term_key(self):
        return self._get_proper_hex("\"LTK\"=hex:(.*)")

    def identity_resolving_key(self):
        return self._get_proper_hex("\"IRK\"=hex:(.*)")

    def local_signature_key(self):
        return self._get_proper_hex("\"CSRK\"=hex:(.*)")

    def erand(self):
        element = self._find_element("\"ERand\"=hex\\(b\\):(.*)")
        result = None
        if element:
            list_hex = element.split(',')
            list_hex.reverse()
            result = str(int("".join(list_hex).upper(), 16))
        return result

    def replace_values(self):
        self._config['LongTermKey']['Key'] = self.long_term_key()
        self._config['LongTermKey']['Rand'] = self.erand()
        self._config['LongTermKey']['EDiv'] = self.ediv()
        self._config['IdentityResolvingKey']['Key'] = self.identity_resolving_key()
        self._config['LocalSignatureKey']['Key'] = self.local_signature_key()

    def _transform_dir(self, string):
        string = string.upper()
        if len(string) % 2 == 1:
            string = "0" + string
        return ":".join(string[i:i+2] for i in range(0, len(string), 2))

    def registry_path(self):
        result = self._find_element("BTHPORT\\\\Parameters\\\\Keys\\\\34f39a0209c6\\\\(.*)\\]")
        if result == None:
            print("The exported path of the registry is not expected.")
            print("Expected exported path is: HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services" + 
                    "\\BTHPORT0\\Parameters\\Keys\\<parent_key>\\<the key of bluetooth mouse>")
            return result
        return self._transform_dir(result)
