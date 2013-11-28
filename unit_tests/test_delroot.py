from __future__ import unicode_literals

import os
import subprocess
import unittest
import datetime
import time

from brd_unit_base import BrdUnitBase

# Import brd in order to use some of its functions
# Note: we're expecting brd_unit_base to take care of path stuff
import brd

class TestList(BrdUnitBase):
    """Unit tests for the list subcommand.
    """

    def setUp(self):
        # Call superclass's setup routine.
        super(TestList,self).setUp()
        
    def tearDown(self):
        # Call superclass's cleanup routine
        super(TestList,self).tearDown()

    def test_dir_target(self):
        """Tests list subcommand with one directory target.
        """

        mod_time = int(time.time())
        check_time = datetime.datetime.fromtimestamp(mod_time)
        exp_out = os.linesep.join( ( 'rootA:', '    LeafB/', '    TreeA/',
                                     '    BunchOfCs.txt', '',
                                     '3 entries listed.', '', '' ) )

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1.
        self.populate_db_from_tree( self.get_schema_1( mod_time, check_time ) )
        self.conn.close()

        # Attempt to list contents
        scr_out = subprocess.check_output([self.script_name, 'list', 
                                           'rootA'])

        # Verify output
        self.assertEqual( scr_out, exp_out )

    def test_file_target(self):
        """Tests list subcommand with one file target.
        """

        mod_time = int(time.time())
        check_time = datetime.datetime.fromtimestamp(mod_time)
        exp_out = os.linesep.join( ( "Files matching 'rootA/BunchOfCs.txt':",
                                     '', 'BunchOfCs.txt:', '    ID: 1',
                                     '    Last Modified: ' + str(
                    datetime.datetime.fromtimestamp(mod_time) ),
                                     '    Fingerprint: 0xff3785f53b503b7adb7e' +
                                     '7a3b9eeef255eac0e276',
                                     '    Size: 257 bytes', '',
                                     '1 entries listed.', '', '' ) )

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1.
        self.populate_db_from_tree( self.get_schema_1( mod_time, check_time ) )
        self.conn.close()

        # Attempt to list contents
        scr_out = subprocess.check_output([self.script_name, 'list', 
                                           'rootA/BunchOfCs.txt'])
        # Verify output
        self.assertEqual( scr_out, exp_out )

    def test_multiple_targets(self):
        """Tests list subcommand with multiple targets.
        """

        mod_time = int(time.time())
        check_time = datetime.datetime.fromtimestamp(mod_time)
        exp_out = os.linesep.join( ( "Files matching 'rootA/BunchOfCs.txt':",
                                     '', 'BunchOfCs.txt:', '    ID: 1',
                                     '    Last Modified: ' + str(
                    datetime.datetime.fromtimestamp(mod_time) ),
                                     '    Fingerprint: 0xff3785f53b503b7adb7e' +
                                     '7a3b9eeef255eac0e276',
                                     '    Size: 257 bytes', '',
                                     '1 entries listed.', '', 
                                     'rootA/LeafB:', '    BunchOfAs.txt', 
                                     '    BunchOfBs.txt', '', 
                                     '2 entries listed.', '', '' ) )

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1.
        self.populate_db_from_tree( self.get_schema_1( mod_time, check_time ) )
        self.conn.close()

        # Attempt to list contents
        scr_out = subprocess.check_output([self.script_name, 'list', 
                                           'rootA/BunchOfCs.txt', 
                                           'rootA/LeafB'])
        # Verify output
        self.assertEqual( scr_out, exp_out )

    def test_invalid_target(self):
        """Tests list subcommand with an invalid target.
        """

        mod_time = int(time.time())
        check_time = datetime.datetime.fromtimestamp(mod_time)
        exp_out = os.linesep.join( ( 'rootA/BunchOfDs.txt is not in database.',
                                     '', '' ) )

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1.
        self.populate_db_from_tree( self.get_schema_1( mod_time, check_time ) )
        self.conn.close()

        # Attempt to list contents
        scr_out = subprocess.check_output([self.script_name, 'list', 
                                           'rootA/BunchOfDs.txt'])
        # Verify output
        self.assertEqual( scr_out, exp_out )

    def test_file_target_wildcard(self):
        """Tests list subcommand with multiple file targets, using wildcards.
        """

        mod_time = int(time.time())
        check_time = datetime.datetime.fromtimestamp(mod_time)
        exp_out = os.linesep.join( ( "Files matching 'rootA/LeafB/*.txt':",
                                     '', 'BunchOfAs.txt:', '    ID: 4',
                                     '    Last Modified: ' + str(
                    datetime.datetime.fromtimestamp(mod_time) ),
                                     '    Fingerprint: 0x1a0372738bb5b4b8360b' +
                                     '47c4504a27e6f4811493',
                                     '    Size: 257 bytes', 
                                     'BunchOfBs.txt:', '    ID: 5',
                                     '    Last Modified: ' + str(
                    datetime.datetime.fromtimestamp(mod_time) ),
                                     '    Fingerprint: 0xfa75bf047f45891daee8' +
                                     'f1fa4cd2bf58876770a5',
                                     '    Size: 257 bytes', '',
                                     '2 entries listed.', '', '' ) )

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1.
        self.populate_db_from_tree( self.get_schema_1( mod_time, check_time ) )
        self.conn.close()

        # Attempt to list contents
        scr_out = subprocess.check_output([self.script_name, 'list', 
                                           'rootA/LeafB/*.txt'])

        # Verify output
        self.assertEqual( scr_out, exp_out )

    def test_use_root(self):
        """Tests list subcommand with one file target and the --use-root option.
        """

        mod_time = int(time.time())
        check_time = datetime.datetime.fromtimestamp(mod_time)
        exp_out = os.linesep.join( ( "Files matching 'my_temp/BunchOfCs.txt':", 
                                     '', 'BunchOfCs.txt:', '    ID: 1',
                                     '    Last Modified: ' + str(
                    datetime.datetime.fromtimestamp(mod_time) ),
                                     '    Fingerprint: 0xff3785f53b503b7adb7e' +
                                     '7a3b9eeef255eac0e276',
                                     '    Size: 257 bytes', '',
                                     '1 entries listed.', '', '' ) )

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1.
        self.populate_db_from_tree( self.get_schema_1( mod_time, check_time ) )
        self.conn.close()

        # Attempt to list contents
        scr_out = subprocess.check_output([self.script_name, 'list', 
                                           '--use-root', 'rootA', 
                                           'my_temp/BunchOfCs.txt'])
        # Verify output
        self.assertEqual( scr_out, exp_out )

    def test_root_prefix(self):
        """Tests list subcommand with one file target and the --root-prefix 
        option.
        """

        mod_time = int(time.time())
        check_time = datetime.datetime.fromtimestamp(mod_time)
        exp_out = os.linesep.join( ( "Files matching 'BunchOfCs.txt':", 
                                     '', 'BunchOfCs.txt:', '    ID: 1',
                                     '    Last Modified: ' + str(
                    datetime.datetime.fromtimestamp(mod_time) ),
                                     '    Fingerprint: 0xff3785f53b503b7adb7e' +
                                     '7a3b9eeef255eac0e276',
                                     '    Size: 257 bytes', '',
                                     '1 entries listed.', '', '' ) )

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1.
        self.populate_db_from_tree( self.get_schema_1( mod_time, check_time ) )
        self.conn.close()

        # Attempt to list contents
        scr_out = subprocess.check_output([self.script_name, 'list', 
                                           '--root-prefix', 'rootA', 
                                           'BunchOfCs.txt'])
        # Verify output
        self.assertEqual( scr_out, exp_out )

    def test_minimal(self):
        """Tests list subcommand --minimal option
        """

        mod_time = int(time.time())
        check_time = datetime.datetime.fromtimestamp(mod_time)
        exp_out = os.linesep.join( ( 'LeafB/', 'TreeA/', 'BunchOfCs.txt', '' ) )

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1.
        self.populate_db_from_tree( self.get_schema_1( mod_time, check_time ) )
        self.conn.close()

        # Attempt to list contents with --minimal
        scr_out = subprocess.check_output([self.script_name, 'list', 
                                           '--minimal', 'rootA'])
        # Verify output
        self.assertEqual( scr_out, exp_out )

        # Attempt to list contents with -m
        scr_out = subprocess.check_output([self.script_name, 'list', 
                                           '-m', 'rootA'])
        # Verify output
        self.assertEqual( scr_out, exp_out )

    def test_expanded(self):
        """Tests list subcommand --expanded option
        """

        mod_time = int(time.time())
        check_time = datetime.datetime.fromtimestamp(mod_time)
        exp_out = os.linesep.join( ( 'rootA:', '    [INFO]', '        ID: 1',
                                     '        Parent ID: -1', 
                                     '        Last Checked: ' + str(
                    datetime.datetime.fromtimestamp(mod_time) ),
                                     '    [Subdirectories]',
                                     '        LeafB/ (2)',
                                     '        TreeA/ (3)',
                                     '    [Files]', '        BunchOfCs.txt (1)',
                                     '', '3 entries listed.', '', '' ) )

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1.
        self.populate_db_from_tree( self.get_schema_1( mod_time, check_time ) )
        self.conn.close()

        # Attempt to list contents with --expanded
        scr_out = subprocess.check_output([self.script_name, 'list', 
                                           '--expanded', 'rootA'])
        # Verify output
        self.assertEqual( scr_out, exp_out )

        # Attempt to list contents with -e
        scr_out = subprocess.check_output([self.script_name, 'list', 
                                           '-e', 'rootA'])
        # Verify output
        self.assertEqual( scr_out, exp_out )


# Allow unit test to run on its own
if __name__ == '__main__':
    unittest.main()
