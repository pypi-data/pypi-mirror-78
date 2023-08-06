"""
build function to use for setup.py
"""
import os
import sys
import subprocess

from distutils.command.build_py import build_py_2to3 as _build_py
from distutils.command.clean import clean as _clean

from distutils.spawn import find_executable

def find_protoc():
    """Locates protoc executable"""
    if 'PROTOC' in os.environ and os.path.exists(os.environ['PROTOC']):
        protoc = os.environ['PROTOC']
    else:
        protoc = find_executable('protoc')

    if protoc is None:
        sys.stderr.write(
            'protoc not found. Is protobuf-compiler installed? \n'
            'Alternatively, you can point the PROTOC environment' + \
            ' variable at a local version.')
        sys.exit(1)

    return protoc

class BuildProtoBuf(_build_py):
    """ find and execute protobuf related work """
    def run(self):
        """ run the proto_builder """
        for package in self.packages:
            packagedir = self.get_package_dir(package)

            for protofile in filter(lambda x: x.endswith('.proto'),
                                    os.listdir(packagedir)):
                source = os.path.join(packagedir, protofile)
                output = source.replace('.proto', '_pb2.py')
                print(f"Generating {output}...")

                if (not os.path.exists(output) or \
                    (os.path.getmtime(source) > os.path.getmtime(output))):
                    protoc_command = [find_protoc(), \
                                      "--python_out=.", source]
                    if subprocess.call(protoc_command) != 0:
                        sys.exit(-1)
        _build_py.run(self)

class CleanProtoBuf(_clean):
    """ clean protobuf info """
    def run(self):
        """ Delete generated files in the code tree. """
        for (dirpath, _, filenames) in os.walk("."):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if filepath.endswith("_pb2.py"):
                    os.remove(filepath)
        # _clean is an old-style class, so super() doesn't work.
        _clean.run(self)
