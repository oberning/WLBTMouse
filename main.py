import argparse
import tempfile
from fileaccess import *
from processing import *

def main():
    parser = argparse.ArgumentParser(prog='WLBTMouse',
        description='Converts a Windows Registry File into Linux Bluetooth Info File')
    parser.add_argument('-i', '--reg_file', required=True, help='The windows registry file')
    parser.add_argument('-o', '--out_path', required=True, help='The path to the info file, often under /var/lib/bluetooth')
    args = parser.parse_args()
    with tempfile.NamedTemporaryFile() as tmpfile:
        tmpfile.write(b'Test')
        tmpfile.seek(0)
        print(str(tmpfile.read()))
        print('Dir %s' % tmpfile.name)
    file_reader = FileReader(args.reg_file, args.out_path)
    file_processing = FileProcessing(file_reader)

    print(file_reader.reg_content)
    print(file_reader.info_content)
    print(file_processing.identity_resolving_key())

if __name__ == "__main__":
    main()
