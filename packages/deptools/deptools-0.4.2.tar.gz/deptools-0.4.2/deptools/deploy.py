# -*- coding: utf-8 -*-
'''AlazarTech Package Deployment Script

This module can be used to deploy AlazarTech's software products to a network
directory, usually the public "P:" drive.

The main routine reads a deployment specification YAML file that determine what
files to deploy and specifies options.

Deployment consists in copying files or entire directories selected by glob
patterns to the destination, then optionnaly compressing these artifacts in an
encrypted zip file, and optionnaly signing the files with Windows' signtool
utility.

Note: The script must be run under Windows if any file should be signed.

Usage:
  deploy [[-e] -p <passfile>] <specfile> <package_name> <destination>
  deploy -h | --help
  deploy --version

Options:
  -h --help      Show this screen
  -p <passfile>  Reads the password from the file at the given path instead of
                 generating a password internally.
  -e             Deploys only the encrypted ZIP file, and no other file. This
                 must be used in conjunction with `-p`, otherwise the password
                 for the output file cannot be obtained.

Arguments:
  <specfile>      Path to the YAML deployment specification file to use for
                  this deployment. See below for more information about the
                  file's format.
  <package_name>  Name of the package to deploy. This is used to name the ZIP
                  file that gets created.
  <destination>   Destination directory where deployment should be made.
                  This can be either a regular file path, or an ftp path
                  formatted as follows:
                  "ftp://[<username>[:<password>]@]<host>/<path>"


Deployment Specification File
-----------------------------

The specs.yaml file contains a list of deployment specification elements. Here
is an example such file:

.. code-block:: yaml

    # This is an example YAML deployment specification file
    - pattern: deploy.py
    - pattern: conanfile.py
    - pattern: "*.md"
      many: yes
      entrypt: yes

Each element is a mapping with the following fields:

 - pattern: required field that takes a "glob" pattern to select the file(s) to
   deploy

 - many: optional boolean field. If this is true, the pattern is allowed to
   match more than one file. If pattern matches no files, an error is emitted.
   If pattern matches more than one file and `many` is false, an error is
   emitted. This option defaults to `False`

 - compress: optional boolean field. If this is true, the targets are
   compressed in a zip file at the destination. Defaults to `False`.

 - encrypt: optional boolean field. If this is `True`, `compress` must be
   `True`. If this is true, the compressed ZIP is password-protected, and a
   `password.txt` file containing the password is created at the destination.

 - sign: optional boolean field. If this is true, the target file(s) is(are)
   signed using Windows' signtool utility. Defaults to `False`

 - destdir: optional string. If this is set, the targets are deployed to this
   subdirectory. Note that the ZIP packages do not use `destdir`, and instead
   generate a "flat" package.

'''

import errno
import os
import secrets
import string
import subprocess
import sys
from collections import namedtuple
from ftplib import FTP, error_perm
from glob import glob
from shutil import (
    copy,
    copytree,
    rmtree,
)

from pyminizip import compress_multiple

import yaml


from docopt import docopt

from parsimonious.exceptions import ParseError
from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

if (sys.version_info > (3, 0)):
    from urllib.parse import urlparse
else:
    from urlparse import urlparse

NetLoc = namedtuple('NetLoc', [
    'username',  # type: str
    'password',  # type: str
    'host',      # type:  str
    ])

class NetLocRuleVisitor(NodeVisitor):
    '''Parser for net locations: [<username>[:<password>]@]<host>'''
    grammar = Grammar(r"""
        netloc = maybe_auth word
        word = ~"[\w.]+"
        maybe_auth = (auth)?
        auth = word maybe_password "@"
        maybe_password = (password)?
        password = ":" word
    """)

    def generic_visit(self, _, __):
        pass

    def visit_password(self, _, childs):
        return childs[1]

    def visit_maybe_password(self, node, childs):
        if node.text:
            return childs[0]
        return None

    def visit_auth(self, _, childs):
        return (childs[0], childs[1])

    def visit_maybe_auth(self, node, childs):
        if node.text:
            return childs[0]
        return (None, None)

    def visit_word(self, node, _):
        return node.text

    def visit_netloc(self, _, childs):
        return NetLoc(childs[0][0], childs[0][1], childs[1])


def copy_local_thing(source, destination):
    '''Copies a local file or a directory to the destination.'''
    try:
        os.makedirs(destination)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    if os.path.isfile(source):
        copy(source, destination)
    elif os.path.isdir(source):
        dirname = os.path.basename(source)
        destdir = "{}/{}".format(destination, dirname)
        if os.path.exists(destdir):
            rmtree(destdir, ignore_errors=True)
        copytree(source, destdir)
    else:
        raise ValueError(
            "Thing to copy is not a file nor a directory: {}".format(source))


def upload_thing(ftp, path):
    if not os.path.exists(path):
        raise ValueError("{} doesn't exist".format(path))

    basename = os.path.basename(path)

    if os.path.isfile(path):
        ftp.storbinary('STOR ' + basename, open(path, 'rb'))
    else:
        try:
            ftp.mkd(basename)
        except error_perm as e:
            # Ignore "already exists"
            if not e.args[0].startswith('550'):
                raise
        ftp.cwd(basename)
        for name in os.listdir(path):
            upload_thing(ftp, "{}/{}".format(path, name))
        ftp.cwd("..")


def ftp_mkd_and_cd(ftp, path):
    '''CD into path, creating directories recursively if needed'''
    dirs = [x for x in path.split('/') if x]
    for name in dirs:
        try:
            ftp.mkd(name)
        except error_perm as e:
            # Ignore "already exists"
            if not e.args[0].startswith('550'):
                raise
        ftp.cwd(name)


def copy_thing(source, destination):
    '''Copies a local source file to a potentially remote location'''
    parseresult = urlparse(destination)
    if parseresult.scheme == "ftp":
        netloc = NetLocRuleVisitor().parse(parseresult.netloc)
        ftp = FTP(netloc.host)
        if netloc.username:
            ftp.login(netloc.username, netloc.password)
        ftp_mkd_and_cd(ftp, parseresult.path)
        upload_thing(ftp, source)
    else:
        copy_local_thing(source, destination)


def create_password():
    '''Create a reasonnably secure 8-character password'''
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(8))



# Describe a (set of) files that should be deployed with an AlazarTech
# product. See module documentation for details.
DeploymentSpecification = namedtuple('DeploymentSpecification', [
    'pattern',   # type: str
    'compress',  # type: bool
    'encrypt',   # type: bool
    'many',      # type: bool
    'sign',      # type: bool
    'destdir',   # type: str
    ])

def sign_file(filepath):
    '''Ditially signs a file'''
    status = subprocess.call(
        "signtool sign /SHA1 c48498d54a5107064fe898b89c3377d18aed6cfa {}".format(filepath)
    )
    assert status == 0, "{} returned while signing file {}".format(status, filepath)


def get_things(spec):
    '''Returns the list of files/directories to copy based on a spec'''
    thinglist = glob(spec.pattern)
    if not thinglist:
        raise ValueError("Pattern {} matched no element".format(spec.pattern))
    if not spec.many and len(thinglist) > 1:
        raise ValueError(
            "Pattern {} matched more than one element: {}".format(spec.pattern, thinglist)
        )
    return thinglist


def get_specs_from_file(specspath):
    output = []
    with open(specspath, 'r') as sfile:
        specslist = yaml.load(sfile, Loader=yaml.FullLoader)
        for specsdict in specslist:
            if 'many' not in specsdict:
                specsdict['many'] = False
            if 'compress' not in specsdict:
                specsdict['compress'] = False
            if 'encrypt' not in specsdict:
                specsdict['encrypt'] = False
            if 'sign' not in specsdict:
                specsdict['sign'] = False
            if 'destdir' not in specsdict:
                specsdict['destdir'] = '/'
            output.append(DeploymentSpecification(**specsdict))
    return output


def deploy(specsfile, name, destination, passfile,
           encrypted_only):
    '''Deploys a set of files according to given specifications.

    Parameters
    ----------
    specsfile: str
        Path to a YAML file that contains the details of details the files that
        should be exported
    name: str
        Name of the package to deploy. This is used to name the
        password-protected ZIP file if any.
    destination: str
        Destination directory of the package. Directory gets created if it does
        not exist. If the directory already exists and it is non-empty, files it
        contains will get overwritten.
    '''
    specs = get_specs_from_file(specsfile)

    # Sign files that need it
    specs_to_sign = [spec for spec in specs if spec.sign]
    for spec in specs_to_sign:
        for thing in get_things(spec):
            # Check that thing is a file, and not a directory
            if not os.path.isfile(thing):
                raise ValueError("Thing to sign is not a file {}".format(thing))

            sign_file(thing)


    specs_to_compress = [spec for spec in specs if spec.compress]
    specs_to_encrypt = [spec for spec in specs if spec.encrypt]

    if specs_to_encrypt:
        # Confirm that the specs that need encryption are the same as the
        # ones that need compression
        if specs_to_compress != specs_to_encrypt:
            raise ValueError(
                "non-null encrypt but things to compress don't match")

    if specs_to_compress:
        password = None
        if specs_to_encrypt:
            password = create_password()
            if passfile:
                with open(passfile, 'r') as passf:
                    password = passf.readline().strip()
            with open('password.txt', 'w') as passf:
                passf.write(password)
            if not encrypted_only:
                copy_thing('password.txt', destination)

        things_to_compress = []
        for spec in specs_to_compress:
            things = get_things(spec)
            things_to_compress.extend(things)
        compress_multiple(things_to_compress, [], "{}.zip".format(name), password, 9)

        copy_thing("{}.zip".format(name), destination)


    # Copy regular things
    if not encrypted_only:
        for spec in specs:
            for thing in get_things(spec):
                copy_thing(thing, "{}/{}".format(destination, spec.destdir))


def main():
    '''Main function'''
    arguments = docopt(__doc__, version='Deloy Utility')
    deploy(
        specsfile=arguments['<specfile>'],
        name=arguments['<package_name>'],
        destination=arguments['<destination>'],
        passfile=arguments['-p'],
        encrypted_only=arguments['-e'])


if __name__ == "__main__":
    main()
