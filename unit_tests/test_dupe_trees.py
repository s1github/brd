#    brd - scans directories and files for damage due to decay of medium.
#    Copyright (C) 2013 Jeff Backus <jeff.backus@gmail.com>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

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

class TestDupeTrees(BrdUnitBase):
    """Unit tests for the dupe_trees subcommand.
    """

    def setUp(self):
        # Call superclass's setup routine.
        super(TestDupeTrees,self).setUp()
        
    def tearDown(self):
        # Call superclass's cleanup routine
        super(TestDupeTrees,self).tearDown()

    def test_identical_trees(self):
        """Tests dupe_trees subcommand with identical trees.
        """

        mod_time = datetime.datetime.fromtimestamp(int(float(time.time())))
        check_time = mod_time
        exp_out = \
            ['2 dirs with Fingerprint ' +
             '0xcab2b4fe2092da433a269238f82810b803c60917:',
             '    [rootB]', '    [rootA]', '']

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1
        self.populate_db_from_tree( 
            self.get_schema_1( mod_time, check_time ) )
        # Append another schema 1 with a new root name
        self.populate_db_from_tree( 
            self.get_schema_1( mod_time, check_time, 
                               root_name = 'rootB', first_file_id=6,
                               first_dir_id=6) )
        self.conn.close()

        # Check targets
        scr_out = subprocess.check_output([self.script_name, 'dupe_trees'], 
                                          stderr=subprocess.STDOUT,
                                          universal_newlines=True)

        scr_lines = scr_out.split('\n')

        # Verify results 
        self.assertEqual( len(scr_lines), len(exp_out) )
        for exp_line in exp_out:
            self.assertTrue( exp_line in scr_lines )
        
    def test_dissimilar_trees(self):
        """Tests dupe_trees subcommand with dissimilar trees.
        """

        mod_time = datetime.datetime.fromtimestamp(int(float(time.time())))
        check_time = mod_time
        exp_out = ['']

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1.
        self.populate_db_from_tree( 
            self.get_schema_1( mod_time, check_time ) )
        # Populate the database with schema 3.
        self.populate_db_from_tree( 
            self.get_schema_3( mod_time, check_time ) )
        self.conn.close()

        # Check targets
        scr_out = subprocess.check_output([self.script_name, 'dupe_trees'], 
                                          stderr=subprocess.STDOUT,
                                          universal_newlines=True)

        scr_lines = scr_out.split('\n')

        # Verify results 
        self.assertEqual( len(scr_lines), len(exp_out) )
        for exp_line in exp_out:
            self.assertTrue( exp_line in scr_lines )
        
    def test_output_option(self):
        """Tests dupe_trees subcommand with --output option.
        """

        mod_time = datetime.datetime.fromtimestamp(int(float(time.time())))
        check_time = mod_time
        out_file = 'test_output.txt'
        exp_out = \
            ['2 dirs with Fingerprint ' +
             '0xcab2b4fe2092da433a269238f82810b803c60917:\n',
             '    [rootB]\n', '    [rootA]\n']

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1
        self.populate_db_from_tree( 
            self.get_schema_1( mod_time, check_time ) )
        # Append another schema 1 with a new root name
        self.populate_db_from_tree( 
            self.get_schema_1( mod_time, check_time, 
                               root_name = 'rootB', first_file_id=6,
                               first_dir_id=6) )
        self.conn.close()

        # Check --output
        scr_out = subprocess.check_output([self.script_name,  'dupe_trees', 
                                           '--output', out_file], 
                                          stderr=subprocess.STDOUT,
                                          universal_newlines=True)

        with open(out_file, 'rt') as f:
            scr_lines = f.readlines()

        # Verify results
        self.assertEqual( scr_out, '' )

        self.assertEqual( len(scr_lines), len(exp_out) )
        for exp_line in exp_out:
            self.assertTrue( exp_line in scr_lines )

        # Remove output file and try again with -o option
        os.unlink( out_file )

        # Check -o
        scr_out = subprocess.check_output([self.script_name, 'dupe_trees', 
                                           '-o', out_file], 
                                          stderr=subprocess.STDOUT,
                                          universal_newlines=True)

        with open(out_file, 'rt') as f:
            scr_lines = f.readlines()

        # Verify results
        self.assertEqual( scr_out, '' )

        self.assertEqual( len(scr_lines), len(exp_out) )
        for exp_line in exp_out:
            self.assertTrue( exp_line in scr_lines )

        # Clean up
        os.unlink( out_file )
        
    def test_nofilefp_option(self):
        """Tests dupe_trees subcommand with --nofilefp option.
        """

        mod_time = datetime.datetime.fromtimestamp(int(float(time.time())))
        check_time = mod_time
        check_out = ['']
        exp_out = ['2 dirs with Fingerprint ' + 
                   '0x9ba569116eee959eae815d7c3d1f2bf81e518526:',
                   '    [rootA]/TreeA/DirA', '    [rootD]/TreeD/DirA', '']

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1.
        self.populate_db_from_tree( 
            self.get_schema_1( mod_time, check_time ) )
        # Populate the database with schema 3.
        self.populate_db_from_tree( 
            self.get_schema_3( mod_time, check_time ) )
        self.conn.close()

        # Check targets normally.
        scr_out = subprocess.check_output([self.script_name, 'dupe_trees'], 
                                          stderr=subprocess.STDOUT,
                                          universal_newlines=True)

        scr_lines = scr_out.split('\n')

        # Verify results
        self.assertEqual( len(scr_lines), len(check_out) )
        for exp_line in check_out:
            self.assertTrue( exp_line in scr_lines )

        # Check targets with --nofilefp
        scr_out = subprocess.check_output([self.script_name, 'dupe_trees',
                                           '--nofilefp'], 
                                          stderr=subprocess.STDOUT,
                                          universal_newlines=True)

        scr_lines = scr_out.split('\n')

        # Verify results 
        self.assertEqual( len(scr_lines), len(exp_out) )
        for exp_line in exp_out:
            self.assertTrue( exp_line in scr_lines )

    def test_nofilename_option(self):
        """Tests dupe_trees subcommand with --nofilename option.
        """

        mod_time = datetime.datetime.fromtimestamp(int(float(time.time())))
        check_time = mod_time
        check_out = ['']
        exp_out = ['2 dirs with Fingerprint ' + 
                   '0xe3405cd476f42e59b326abed4daa92f7dc220b42:',
                   '    [rootA]', '    [rootB]', '']

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1
        self.populate_db_from_tree( 
            self.get_schema_1( mod_time, check_time ) )
        # Populate the database with schema 4
        self.populate_db_from_tree( 
            self.get_schema_4( mod_time, check_time ) )
        self.conn.close()

        # Check targets normally.
        scr_out = subprocess.check_output([self.script_name, 'dupe_trees'], 
                                          stderr=subprocess.STDOUT,
                                          universal_newlines=True)

        scr_lines = scr_out.split('\n')

        # Verify results
        self.assertEqual( len(scr_lines), len(check_out) )
        for exp_line in check_out:
            self.assertTrue( exp_line in scr_lines )

        # Check targets with --nofilename
        scr_out = subprocess.check_output([self.script_name, 'dupe_trees',
                                           '--nofilename'], 
                                          stderr=subprocess.STDOUT,
                                          universal_newlines=True)

        scr_lines = scr_out.split('\n')

        # Verify results 
        self.assertEqual( len(scr_lines), len(exp_out) )
        for exp_line in exp_out:
            self.assertTrue( exp_line in scr_lines )

    def test_nosubdirfp_option(self):
        """Tests dupe_trees subcommand with --nosubdirfp option
        """

        mod_time = datetime.datetime.fromtimestamp(int(float(time.time())))
        check_time = mod_time
        check_out = ['']
        exp_out = ['2 dirs with Fingerprint ' +
                     '0xa937d97faf45931eeb5690804c2d26d519c06cf9:', 
                     '    [rootA]/TreeA/DirA', 
                     '    [rootD]/TreeD/DirA', '']

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1.
        self.populate_db_from_tree( 
            self.get_schema_1( mod_time, check_time ) )
        # Populate the database with schema 3.
        self.populate_db_from_tree( 
            self.get_schema_3( mod_time, check_time ) )
        self.conn.close()

        # Check targets normally.
        scr_out = subprocess.check_output([self.script_name, 'dupe_trees'], 
                                          stderr=subprocess.STDOUT,
                                          universal_newlines=True)

        scr_lines = scr_out.split('\n')

        # Verify results
        self.assertEqual( len(scr_lines), len(check_out) )
        for exp_line in check_out:
            self.assertTrue( exp_line in scr_lines )

        # Check targets with --nofilename
        scr_out = subprocess.check_output([self.script_name, 'dupe_trees',
                                           '--nosubdirfp'], 
                                          stderr=subprocess.STDOUT,
                                          universal_newlines=True)

        scr_lines = scr_out.split('\n')

        # Verify results 
        self.assertEqual( len(scr_lines), len(exp_out) )
        for exp_line in exp_out:
            self.assertTrue( exp_line in scr_lines )

    def test_nosubdirname_option(self):
        """Tests dupe_trees subcommand with --nosubdirname option
        """

        mod_time = datetime.datetime.fromtimestamp(int(float(time.time())))
        check_time = mod_time
        check_out = ['4 dirs with Fingerprint ' + 
                   '0x183831bb75375e5a0fdd885c3b4425472519b7e9:', 
                   '    [rootA]/LeafB', 
                   '    [rootB]/TreeD/DirD/LeafD', 
                   '    [rootA]/TreeA/DirA/LeafA', 
                   '    [rootB]/LeafE', '']
        exp_out = ['2 dirs with Fingerprint ' +
                   '0x1c2531f369ffdabf217641a9ffc4694bbe58b3e9:', 
                   '    [rootB]', 
                   '    [rootA]'] + check_out 

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1.
        self.populate_db_from_tree( 
            self.get_schema_1( mod_time, check_time ) )
        # Populate the database with schema 2.
        self.populate_db_from_tree( 
            self.get_schema_2( mod_time, check_time ) )
        self.conn.close()

        # Check targets with just --nodirname.
        scr_out = subprocess.check_output([self.script_name, 'dupe_trees',
                                           '--nodirname'], 
                                          stderr=subprocess.STDOUT,
                                          universal_newlines=True)

        scr_lines = scr_out.split('\n')

        # Verify results
        self.assertEqual( len(scr_lines), len(check_out) )
        for exp_line in check_out:
            self.assertTrue( exp_line in scr_lines )

        # Check targets with --nosubdirname and --nodirname
        scr_out = subprocess.check_output([self.script_name, 'dupe_trees',
                                           '--nosubdirname', '--nodirname'], 
                                          stderr=subprocess.STDOUT,
                                          universal_newlines=True)

        scr_lines = scr_out.split('\n')

        # Verify results 
        self.assertEqual( len(scr_lines), len(exp_out) )
        for exp_line in exp_out:
            self.assertTrue( exp_line in scr_lines )

    def test_nodirname_option(self):
        """Tests dupe_trees subcommand with --nodirname option.
        """

        mod_time = datetime.datetime.fromtimestamp(int(float(time.time())))
        check_time = mod_time
        check_out = ['2 dirs with Fingerprint '+
                     '0xcab2b4fe2092da433a269238f82810b803c60917:',
                     '    [rootB]', '    [rootA]', '']

        exp_out = ['2 dirs with Fingerprint ' +
                   '0x130563c2a00cfbb70e9abc1042b02e25a10b9c31:', 
                   '    [rootB]', '    [rootA]', 
                   '4 dirs with Fingerprint ' +
                   '0x183831bb75375e5a0fdd885c3b4425472519b7e9:', 
                   '    [rootA]/LeafB', '    [rootB]/TreeA/DirA/LeafA', 
                   '    [rootA]/TreeA/DirA/LeafA', 
                   '    [rootB]/LeafB', '']

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1
        self.populate_db_from_tree( 
            self.get_schema_1( mod_time, check_time ) )
        # Append another schema 1 with a new root name
        self.populate_db_from_tree( 
            self.get_schema_1( mod_time, check_time, 
                               root_name = 'rootB', first_file_id=6,
                               first_dir_id=6) )
        self.conn.close()

        # Check targets normally.
        scr_out = subprocess.check_output([self.script_name, 'dupe_trees'], 
                                          stderr=subprocess.STDOUT,
                                          universal_newlines=True)

        scr_lines = scr_out.split('\n')

        # Verify results
        self.assertEqual( len(scr_lines), len(check_out) )
        for exp_line in check_out:
            self.assertTrue( exp_line in scr_lines )

        # Check targets with --nodirname
        scr_out = subprocess.check_output([self.script_name, 'dupe_trees',
                                           '--nodirname'], 
                                          stderr=subprocess.STDOUT,
                                          universal_newlines=True)

        scr_lines = scr_out.split('\n')

        # Verify results 
        self.assertEqual( len(scr_lines), len(exp_out) )
        for exp_line in exp_out:
            self.assertTrue( exp_line in scr_lines )

# Allow unit test to run on its own
if __name__ == '__main__':
    unittest.main()
