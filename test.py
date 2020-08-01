import unittest
from unittest.mock import MagicMock
import processing

class ProcessingTest(unittest.TestCase):

    def setUp(self):
        self._reg_content = ['Windows Registry Editor Version 5.00', '', 
                '[HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\BTHPORT\\Parameters\\Keys\\34f39a0209c6\\cfae3715888c]', 
                '"LTK"=hex:4c,ef,de,b2,09,c9,d3,fb,74,43,91,03,7f,06,23,89', '"KeyLength"=dword:00000010', 
                '"ERand"=hex(b):91,9a,b7,ec,52,c5,5c,39', '"EDIV"=dword:0000aadd', 
                '"IRK"=hex:8a,4b,56,40,c6,b1,bb,9a,00,02,10,fa,aa,6a,37,b6', 
                '"Address"=hex(b):8c,88,15,37,ae,cf,00,00', '"AddressType"=dword:00000001', 
                '"CSRK"=hex:d5,4c,b3,bd,15,aa,ac,bc,26,21,79,12,47,54,3a,21', '"OutboundSignCounter"=dword:00000000', 
                '"MasterIRKStatus"=dword:00000001', '"AuthReq"=dword:0000002d', '']
        self._info_content = []
    
    def test_long_term_key(self):
        mock = MagicMock()
        mock.reg_content = self._reg_content
        mock.info_content = self._info_content
        fp = processing.FileProcessing(mock)
        self.assertEqual(fp.long_term_key(), "4CEFDEB209C9D3FB744391037F062389")
    
    def test_identity_resolving_key(self):
        mock = MagicMock()
        mock.reg_content = self._reg_content
        mock.info_content = self._info_content
        fp = processing.FileProcessing(mock)
        self.assertEqual(fp.identity_resolving_key(), "8A4B5640C6B1BB9A000210FAAA6A37B6")

    def test_local_signature_key(self):
        mock = MagicMock()
        mock.reg_content = self._reg_content
        mock.info_content = self._info_content
        fp = processing.FileProcessing(mock)
        self.assertEqual(fp.local_signature_key(), "D54CB3BD15AAACBC2621791247543A21")

    def test_ediv(self):
        mock = MagicMock()
        mock.reg_content = self._reg_content
        mock.info_content = self._info_content
        fp = processing.FileProcessing(mock)
        self.assertEqual(fp.ediv(), 43741)

    def test_ediv_none(self):
        mock = MagicMock()
        mock.reg_content = self._reg_content
        mock.info_content = self._info_content
        mock.reg_content[6] = "Something completey different"
        fp_none = processing.FileProcessing(mock)
        self.assertEqual(fp_none.ediv(), None)

    def test_erand(self):
        mock = MagicMock()
        mock.reg_content = self._reg_content
        mock.info_content = self._info_content
        fp = processing.FileProcessing(mock)
        self.assertEqual(fp.erand(), 4133395517968718481)

    def test_erand_none(self):
        mock = MagicMock()
        mock.reg_content = self._reg_content
        mock.info_content = self._info_content
        mock.reg_content[5] = "Something completey different"
        fp_none = processing.FileProcessing(mock)
        self.assertEqual(fp_none.erand(), None)


if __name__ == '__main__':
    unittest.main()