#!/usr/bin/python
"""

> python findpkg.py --help
usage: findpkg.py [-h] [-p PACKAGE] [-b BINARY] image

positional arguments:
  image                 Linux distro (image:tag)

optional arguments:
  -h, --help            show this help message and exit
  -p PACKAGE, --package PACKAGE
                        Package to search for
  -b BINARY, --binary BINARY
                        Binary to search for

"""
import sys
import argparse
from docker import Client

def search(distro, package=None, binary=None):

    docker = Client(base_url='unix://var/run/docker.sock')
    search_pkgcmd = {'fedora':'yum search',
                     'centos':'yum search',
                     'ubuntu':'apt-cache search',
                     'debian':'apt-cache search',
                 }
    search_binarycmd = {'fedora':'yum whatprovides',
                        'centos':'yum whatprovides',
                        # XX: broken since apt-file is not
                        # installed
                        'ubuntu':'apt-file search',
                        'debian':'apt-file search',
    }

    if package:
        cmd = search_pkgcmd[distro.split(':')[0]]
        search_for = package
    if binary:
        cmd = search_binarycmd[distro.split(':')[0]]
        search_for = binary

    docker.pull(distro)
    contid = docker.create_container(image='{0}'.format(distro),
                                     command='{0} {1}'.format(cmd, search_for))
    docker.start(contid)
    docker.wait(contid)
    return str(docker.logs(contid))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image',
                        help='Linux distro (image:tag)'
                        )
    parser.add_argument('-p', '--package',
                        type=str,
                        help='Package to search for'
                        )
    parser.add_argument('-b', '--binary',
                        type=str,
                        help='Binary to search for'
                        )

    args = parser.parse_args()

    if len(args.image.split(':')) != 2:
        sys.exit('Specify image as image:tag')

    package = None
    binary = None
    if args.binary:
        binary = args.binary
    if args.package:
        package = args.package
    if (package and binary) or (not package and not binary):
        sys.exit('Specify either package or binary')
    result = search(args.image, package, binary)
    if result:
        print result
    else:
        print 'No package found'
