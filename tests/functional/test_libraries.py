# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2005-2015, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

# Library imports
# ---------------
import os
import pytest
import shutil

# Local imports
# -------------
from PyInstaller.utils.tests import importorskip, xfail_py2


@xfail_py2
@importorskip('django')
# Django test might sometimes hang.
@pytest.mark.timeout(timeout=7*60)
def test_django(pyi_builder, monkeypatch, data_dir):
    script_dir = os.path.join(data_dir, 'django_site')
    # Extend sys.path so PyInstaller could find modules from 'django_site' project.
    monkeypatch.syspath_prepend(script_dir)
    # Django uses manage.py as the main script.
    script = os.path.join(script_dir, 'manage.py')
    # Create the exe, run django command 'check' to do basic sanity checking of the
    # executable.
    pyi_builder.test_script(script, app_name='django_site', app_args=['check'])


@importorskip('enchant')
def test_enchant(pyi_builder):
    pyi_builder.test_script('pyi_lib_enchant.py')


def test_tkinter(pyi_builder):
    pyi_builder.test_script('pyi_lib_tkinter.py')


@importorskip('zmq')
def test_zmq(pyi_builder):
    pyi_builder.test_script('pyi_lib_zmq.py')


@importorskip('sphinx')
def test_sphinx(tmpdir, pyi_builder, data_dir):
    # Copy the data/sphix directory to the tempdir used by this test.
    shutil.copytree(os.path.join(data_dir, 'sphinx'),
                    os.path.join(tmpdir.strpath, 'data', 'sphinx'))
    pyi_builder.test_script('pyi_lib_sphinx.py')

@pytest.mark.xfail(reason='pkg_resources is not supported yet.')
@importorskip('pylint')
def test_pylint(pyi_builder):
    pyi_builder.test_script('pyi_lib_pylint.py')

@importorskip('pygments')
def test_pygments(pyi_builder):
    pyi_builder.test_script('pyi_lib_pygments.py')

@importorskip('markdown')
def test_markdown(pyi_builder):
    pyi_builder.test_script('pyi_lib_markdown.py')

@importorskip('PyQt4')
def test_PyQt4_QtWebKit(pyi_builder):
    pyi_builder.test_script('pyi_lib_PyQt4-QtWebKit.py')

@pytest.mark.xfail(reason='Reports "ImportError: No module named QtWebKit.QWebView".')
@importorskip('PyQt4')
def test_PyQt4_uic(tmpdir, pyi_builder, data_dir):
    # Copy the data/PyQt4-uic.ui file to the tempdir used by this test.
    os.mkdir(os.path.join(tmpdir.strpath, 'data'))
    shutil.copy(os.path.join(data_dir, 'PyQt4-uic.ui'),
                os.path.join(tmpdir.strpath, 'data'))

    pyi_builder.test_script('pyi_lib_PyQt4-uic.py')


@importorskip('zope.interface')
def test_zope_interface(pyi_builder):
    # Tests that modules without __init__.py file are bundled properly.
    pyi_builder.test_source(
        """
        # Package 'zope' does not contain __init__.py file.
        # Just importing 'zope.interface' is sufficient.
        import zope.interface
        """)


@importorskip('idlelib')
def test_idlelib(pyi_builder):
    pyi_builder.test_source(
        """
        # This file depends on loading some icons, located based on __file__.
        import idlelib.TreeWidget
        """)


@importorskip('keyring')
def test_keyring(pyi_builder):
    pyi_builder.test_script('pyi_lib_keyring.py')


@importorskip('numpy')
def test_numpy(pyi_builder):
    pyi_builder.test_source(
        """
        from __future__ import print_function
        import numpy
        from numpy.core.numeric import dot
        print('dot(3, 4):', dot(3, 4))
        """)


@importorskip('pyodbc')
def test_pyodbc(pyi_builder):
    pyi_builder.test_source(
        """
        # pyodbc is a binary Python module. On Windows when installed with easy_install
        # it is installed as zipped Python egg. This binary module is extracted
        # to PYTHON_EGG_CACHE directory. PyInstaller should find the binary there and
        # include it with frozen executable.
        import pyodbc
        """)


@importorskip('pytz')
def test_pytz(pyi_builder):
    pyi_builder.test_source(
        """
        import pytz
        pytz.timezone('US/Eastern')
        """)


@importorskip('pyttsx')
def test_pyttsx(pyi_builder):
    pyi_builder.test_source(
        """
        # Basic code example from pyttsx tutorial.
        # http://packages.python.org/pyttsx/engine.html#examples
        import pyttsx
        engine = pyttsx.init()
        engine.say('Sally sells seashells by the seashore.')
        engine.say('The quick brown fox jumped over the lazy dog.')
        engine.runAndWait()
        """)


@importorskip('pycparser')
def test_pycparser(pyi_builder):
    pyi_builder.test_script('pyi_lib_pycparser.py')


@importorskip('Crypto')
def test_pycrypto(pyi_builder):
    pyi_builder.test_source(
        """
        from __future__ import print_function
        import binascii
        from Crypto.Cipher import AES
        BLOCK_SIZE = 16
        print('AES null encryption, block size', BLOCK_SIZE)
        # Just for testing functionality after all
        print('HEX', binascii.hexlify(
            AES.new('\0' * BLOCK_SIZE).encrypt('\0' * BLOCK_SIZE)))
        """)


@importorskip('sqlite3')
def test_sqlite3(pyi_builder):
    pyi_builder.test_source(
        """
        # PyInstaller did not included module 'sqlite3.dump'.
        import sqlite3
        conn = sqlite3.connect(':memory:')
        csr = conn.cursor()
        csr.execute('CREATE TABLE Example (id)')
        for line in conn.iterdump():
             print(line)
        """)


@importorskip('scapy')
def test_scapy(pyi_builder):
    pyi_builder.test_source(
        """
        # Test-cases taken from issue #834
        import scapy.all
        scapy.all.IP

        from scapy.all import IP

        # Test-case taken from issue #202.
        from scapy.all import *
        DHCP # scapy.layers.dhcp.DHCP
        BOOTP # scapy.layers.dhcp.BOOTP
        DNS # scapy.layers.dns.DNS
        ICMP # scapy.layers.inet.ICMP
        """)


@importorskip('scapy')
def test_scapy2(pyi_builder):
    pyi_builder.test_source(
        """
        # Test the hook to scapy.layers.all
        from scapy.layers.all import DHCP
        """)


@importorskip('scapy')
def test_scapy3(pyi_builder):
    pyi_builder.test_source(
        """
        # Test whether
        # a) scapy packet layers are not included if neither scapy.all nor
        #    scapy.layers.all are imported.
        # b) packages are included if imported explicitly

        # This test-case assumes, that layer modules are imported only if
        NAME = 'hook-scapy.layers.all'
        layer_inet = 'scapy.layers.inet'

        def testit():
            try:
                __import__(layer_inet)
                raise SystemExit('Self-test of hook %s failed: package module found'
                                 % NAME)
            except ImportError, e:
                if not e.args[0].endswith(' inet'):
                    raise SystemExit('Self-test of hook %s failed: package module found'
                                    ' and has import errors: %r' % (NAME, e))

        import scapy
        testit()
        import scapy.layers
        testit()
        # Explicitly import a single layer module. Note: This module MUST NOT
        # import inet (neither directly nor indirectly), otherwise the test
        # above fails.
        import scapy.layers.ir
        """)


@importorskip('scipy')
def test_scipy(pyi_builder):
    pyi_builder.test_source(
        """
        # General SciPy import.
        from scipy import *
        # Test import hooks for the following modules.
        import scipy.io.matlab
        import scipy.sparse.csgraph
        # Some other "problematic" scipy submodules.
        import scipy.lib
        import scipy.linalg
        import scipy.signal
        """)


@importorskip('sqlalchemy')
def test_sqlalchemy(pyi_builder):
    pyi_builder.test_source(
        """
        # The hook behaviour is to include with sqlalchemy all installed database
        # backends.
        import sqlalchemy
        # This import was known to fail with sqlalchemy 0.9.1
        import sqlalchemy.ext.declarative
        """)


@importorskip('twisted')
def test_twisted(pyi_builder):
    pyi_builder.test_source(
        """
        # Twisted is an event-driven networking engine.
        #
        # The 'reactor' is object that starts the eventloop.
        # There are different types of platform specific reactors.
        # Platform specific reactor is wrapped into twisted.internet.reactor module.
        from twisted.internet import reactor
        # Applications importing module twisted.internet.reactor might fail
        # with error like:
        #
        #     AttributeError: 'module' object has no attribute 'listenTCP'
        #
        # Ensure default reactor was loaded - it has method 'listenTCP' to start server.
        if not hasattr(reactor, 'listenTCP'):
            raise SystemExit('Twisted reactor not properly initialized.')
        """)


@importorskip('matplotlib')
def test_matplotlib(pyi_builder):
    pyi_builder.test_source(
        """
        import os
        import matplotlib
        import sys
        import tempfile
        # In frozen state rthook should force matplotlib to create config directory
        # in temp directory and not $HOME/.matplotlib.
        configdir = os.environ['MPLCONFIGDIR']
        print(('MPLCONFIGDIR: %s' % configdir))
        if not configdir.startswith(tempfile.gettempdir()):
            raise SystemExit('MPLCONFIGDIR not pointing to temp directory.')
        # matplotlib data directory should point to sys._MEIPASS.
        datadir = os.environ['MATPLOTLIBDATA']
        print(('MATPLOTLIBDATA: %s' % datadir))
        if not datadir.startswith(sys._MEIPASS):
            raise SystemExit('MATPLOTLIBDATA not pointing to sys._MEIPASS.')
        """)


@importorskip('pyexcelerate')
def test_pyexcelerate(pyi_builder):
    pyi_builder.test_source(
        """
        # Requires PyExcelerate 0.6.1 or higher
        # Tested on Windows 7 x64 SP1 with CPython 2.7.6
        import pyexcelerate
        """)


@importorskip('usb')
def test_usb(pyi_builder):
    pyi_builder.test_source(
        """
        import usb.core
        # Detect usb devices.
        devices = usb.core.find(find_all = True)
        if not devices:
            raise SystemExit('No USB device found.')
        """)
