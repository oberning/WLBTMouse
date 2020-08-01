import re

class FileProcessing:

    def __init__(self, file_reader):
        self._reg_content = file_reader.reg_content
        self._info_content = file_reader.info_content

    def identity_resolving_key_target(self):
        return self._info_content.index("[IdentityResolvingKey]")

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
            result = int(element, 16)
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
            result = int("".join(list_hex).upper(), 16)
        return result
