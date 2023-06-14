import os
import json
import base64
from glob import glob

class FileInterface:
    def __init__(self):
        os.chdir('files/')

    def list(self, params=None):
        try:
            filelist = glob('*.*')
            return dict(status='OK', data=filelist)
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def get(self, params=None):
        try:
            if not params:
                return dict(status='ERROR', data='Missing filename')

            filename = params[0]
            if filename == '':
                return dict(status='ERROR', data='Invalid filename')

            with open(filename, 'rb') as fp:
                isifile = base64.b64encode(fp.read()).decode()

            return dict(status='OK', data=dict(data_namafile=filename, data_file=isifile))
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def post(self, params=None):
        try:
            if not params or len(params) < 2:
                return dict(status='ERROR', data='Missing filename or file content')

            filename = params[0]
            if filename == '':
                return dict(status='ERROR', data='Invalid filename')

            isifile = params[1]
            with open(filename, 'wb') as fp:
                decoded_file_content = base64.b64decode(isifile)
                fp.write(decoded_file_content)

            return dict(status='OK', data_namafile=filename, data_file=isifile)
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def delete(self, params=None):
        try:
            if not params:
                return dict(status='ERROR', data='Missing filename')

            filename = params[0]
            if filename == '':
                return dict(status='ERROR', data='Invalid filename')

            os.remove(filename)
            return dict(status='OK', data='File berhasil dihapus')
        except Exception as e:
            return dict(status='ERROR', data=str(e))


if __name__ == '__main__':
    f = FileInterface()
    print(f.list())
    print(f.get(['pokijan.jpg']))
