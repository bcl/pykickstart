import unittest, shlex
import warnings
import tempfile
from tests.baseclass import *

from pykickstart.version import *
from pykickstart.errors import *
from pykickstart.commands.vnc import *
#from pykickstart.base import *
#from pykickstart.options import *

def getClassName(cls):
    return cls().__class__.__name__

class StringToVersion_TestCase(CommandTest):
    def runTest(self):

        # fail - no version specified
        self.assertRaises(KickstartVersionError, stringToVersion, "RHEL")
        self.assertRaises(KickstartVersionError, stringToVersion, "Red Hat Enterprise Linux")
        self.assertRaises(KickstartVersionError, stringToVersion, "Fedora")
        self.assertRaises(KickstartVersionError, stringToVersion, "F")
        self.assertRaises(KickstartVersionError, stringToVersion, "FC")

        # fail - too old
        self.assertRaises(KickstartVersionError, stringToVersion, "Fedora Core 1")
        self.assertRaises(KickstartVersionError, stringToVersion, "Fedora Core 2")

        # fail - incorrect syntax
        self.assertRaises(KickstartVersionError, stringToVersion, "FC7")
        self.assertRaises(KickstartVersionError, stringToVersion, "FC8")
        self.assertRaises(KickstartVersionError, stringToVersion, "FC9")
        self.assertRaises(KickstartVersionError, stringToVersion, "FC10")
        self.assertRaises(KickstartVersionError, stringToVersion, "FC11")
        self.assertRaises(KickstartVersionError, stringToVersion, "F1111")
        self.assertRaises(KickstartVersionError, stringToVersion, "F 11")

        # pass - FC3
        self.assertEqual(stringToVersion("Fedora Core 3"), FC3)
        self.assertEqual(stringToVersion("FC3"), FC3)
        # pass - FC4
        self.assertEqual(stringToVersion("Fedora Core 4"), FC4)
        self.assertEqual(stringToVersion("FC4"), FC4)
        # pass - FC5
        self.assertEqual(stringToVersion("Fedora Core 5"), FC5)
        self.assertEqual(stringToVersion("FC5"), FC5)
        # pass - FC6
        self.assertEqual(stringToVersion("Fedora Core 6"), FC6)
        self.assertEqual(stringToVersion("FC6"), FC6)
        # pass - F7
        self.assertEqual(stringToVersion("Fedora Core 7"), F7)
        self.assertEqual(stringToVersion("Fedora 7"), F7)
        self.assertEqual(stringToVersion("F7"), F7)
        # pass - F8
        self.assertEqual(stringToVersion("Fedora Core 8"), F8)
        self.assertEqual(stringToVersion("Fedora 8"), F8)
        self.assertEqual(stringToVersion("F8"), F8)
        # pass - F9
        self.assertEqual(stringToVersion("Fedora Core 9"), F9)
        self.assertEqual(stringToVersion("Fedora 9"), F9)
        self.assertEqual(stringToVersion("F9"), F9)
        # pass - F10
        self.assertEqual(stringToVersion("Fedora Core 10"), F10)
        self.assertEqual(stringToVersion("Fedora 10"), F10)
        self.assertEqual(stringToVersion("F10"), F10)
        # pass - F11
        self.assertEqual(stringToVersion("Fedora 11"), F11)
        self.assertEqual(stringToVersion("F11"), F11)
        # pass - F12
        self.assertEqual(stringToVersion("Fedora 12"), F12)
        self.assertEqual(stringToVersion("F12"), F12)
        # pass - F13
        self.assertEqual(stringToVersion("Fedora 13"), F13)
        self.assertEqual(stringToVersion("F13"), F13)

        # pass - RHEL3
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux 3"), RHEL3)
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux AS 3"), RHEL3)
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux ES 3"), RHEL3)
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux WS 3"), RHEL3)
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux Desktop 3"), RHEL3)
        self.assertEqual(stringToVersion("RHEL3"), RHEL3)

        # pass - RHEL4
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux 4"), RHEL4)
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux AS 4"), RHEL4)
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux ES 4"), RHEL4)
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux WS 4"), RHEL4)
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux Desktop 4"), RHEL4)
        self.assertEqual(stringToVersion("RHEL4"), RHEL4)

        # pass - RHEL5
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux 5"), RHEL5)
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux Client 5"), RHEL5)
        self.assertEqual(stringToVersion("Red Hat Enterprise Linux Server 5"), RHEL5)
        for MINOR in range(1,10):
            self.assertEqual(stringToVersion("Red Hat Enterprise Linux 5.%s" % MINOR), RHEL5)
            self.assertEqual(stringToVersion("Red Hat Enterprise Linux Client 5.%s" % MINOR), RHEL5)
            self.assertEqual(stringToVersion("Red Hat Enterprise Linux Server 5.%s" % MINOR), RHEL5)
        self.assertEqual(stringToVersion("RHEL5"), RHEL5)

class VersionToString_TestCase(CommandTest):
    def runTest(self):

        # Make sure DEVEL is the highest version
        highest = 0
        for (ver_str,ver_num) in versionMap.items():
            highest = max(ver_num, highest)
        self.assertEqual(highest, DEVEL)

        # FC series
        self.assertEqual(versionToString(FC3), "FC3")
        self.assertEqual(versionToString(FC4), "FC4")
        self.assertEqual(versionToString(FC5), "FC5")
        self.assertEqual(versionToString(FC6), "FC6")
        # F series
        self.assertEqual(versionToString(F7), "F7")
        self.assertEqual(versionToString(F8), "F8")
        self.assertEqual(versionToString(F9), "F9")
        self.assertEqual(versionToString(F10), "F10")
        self.assertEqual(versionToString(F10, skipDevel=True), "F10")
        self.assertEqual(versionToString(F10, skipDevel=False), "F10")
        self.assertEqual(versionToString(F11, skipDevel=True), "F11")
        self.assertEqual(versionToString(F11, skipDevel=False), "F11")
        self.assertEqual(versionToString(F12, skipDevel=True), "F12")
        self.assertEqual(versionToString(F13, skipDevel=True), "F13")
        self.assertEqual(versionToString(F13, skipDevel=False), "DEVEL")
        # RHEL series
        self.assertEqual(versionToString(RHEL3), "RHEL3")
        self.assertEqual(versionToString(RHEL4), "RHEL4")
        self.assertEqual(versionToString(RHEL5), "RHEL5")

class returnClassForVersion_TestCase(CommandTest):
    def runTest(self):

        # Load the handlers
        import pykickstart.handlers
        for module in loadModules(pykickstart.handlers.__path__[0], cls_pattern="Handler", skip_list=["control"]):
            if module.__name__.endswith("Handler") and module.__name__ not in ["BaseHandler"]:
                # What is the version of the handler?
                vers = module.__name__.replace("Handler","")
                self.assertTrue(versionMap.has_key(vers))
                # Ensure that returnClassForVersion returns what we expect
                self.assertEqual(getClassName(returnClassForVersion(versionMap[vers])), getClassName(module))

# TODO - versionFromFile

class versionFromFile_TestCase(CommandTest):
    def runTest(self):

        def write_ks_cfg(buf):
            (fd, name) = tempfile.mkstemp(prefix="ks-", suffix=".cfg", dir="/tmp")
            os.write(fd, buf)
            os.close(fd)
            return name

        # no version specified
        ks_cfg = '''
# This is a sample kickstart file
rootpw testing123
cdrom
'''
        ks_cfg = write_ks_cfg(ks_cfg)
        self.assertEqual(versionFromFile(ks_cfg), DEVEL)
        os.unlink(ks_cfg)

        # proper format ... DEVEL
        ks_cfg = '''
# This is a sample kickstart file
#version=DEVEL
rootpw testing123
cdrom
'''
        ks_cfg = write_ks_cfg(ks_cfg)
        self.assertEqual(versionFromFile(ks_cfg), DEVEL)
        os.unlink(ks_cfg)

        # proper format ... RHEL3
        ks_cfg = '''
# This is a sample kickstart file
#version=RHEL3
rootpw testing123
cdrom
'''
        ks_cfg = write_ks_cfg(ks_cfg)
        self.assertEqual(versionFromFile(ks_cfg), RHEL3)
        os.unlink(ks_cfg)

        # improper format ... fallback to DEVEL
        ks_cfg = '''
# This is a sample kickstart file
# version: FC3
rootpw testing123
cdrom
'''
        ks_cfg = write_ks_cfg(ks_cfg)
        self.assertEqual(versionFromFile(ks_cfg), DEVEL)
        os.unlink(ks_cfg)

        # unknown version specified ... raise exception
        ks_cfg = '''
# This is a sample kickstart file
#version=RHEL5000
rootpw testing123
cdrom
'''
        ks_cfg = write_ks_cfg(ks_cfg)
        self.assertRaises(KickstartVersionError, versionFromFile, ks_cfg)
        os.unlink(ks_cfg)

if __name__ == "__main__":
    unittest.main()