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

class TestDelRoot(BrdUnitBase):
    """Unit tests for the delroot subcommand.
    """

    def setUp(self):
        # Call superclass's setup routine.
        super(TestDelRoot,self).setUp()
        
    def tearDown(self):
        # Call superclass's cleanup routine
        super(TestDelRoot,self).tearDown()

    def test_dir_target(self):
        """Tests delroot subcommand with one directory target.
        """

        mod_time = int(time.time())
        check_time = datetime.datetime.fromtimestamp(mod_time)

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1.
        exp_data = self.get_schema_1( str(mod_time), check_time )
        self.populate_db_from_tree( exp_data )
        self.conn.close()

        # Attempt to remove target subtree.
        scr_out = subprocess.check_output([self.script_name, 'delroot', 
                                           'rootA/TreeA'])

        # Remove target subtree from expected contents
        del(exp_data['roots']['rootA']['children']['TreeA'])

        # Reopen database
        self.open_db( self.default_db, False )
        cursor = self.conn.cursor()

        # Build a tree data structure from the current database contents.
        cur_data = self.build_tree_data_from_db( cursor )

        # Strip out contents field from all file entries and Name from the
        # top-level before comparing
        exp_data = self.strip_fields( exp_data, 'contents' )
        cur_data = self.strip_fields( cur_data, 'contents' )
        del(exp_data['Name'])
        del(cur_data['Name'])

        diff_results = self.diff_trees( exp_data, cur_data)
        
        # Verify results
        self.assertEqual( diff_results['left'], None)
        self.assertEqual( diff_results['right'], None)
        self.assertNotEqual( len( diff_results['common']['roots'] ), 0)
        
    def test_file_target(self):
        """Tests delroot subcommand with one file target.
        """

        mod_time = int(time.time())
        check_time = datetime.datetime.fromtimestamp(mod_time)

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1.
        exp_data = self.get_schema_1( str(mod_time), check_time )
        self.populate_db_from_tree( exp_data )
        self.conn.close()

        # Attempt to remove target file.
        scr_out = subprocess.check_output([self.script_name, 'delroot', 
                                           'rootA/LeafB/BunchOfAs.txt'])

        # Remove target file from expected contents
        del(exp_data['roots']['rootA']['children']['LeafB']['children']\
            ['BunchOfAs.txt'])

        # Reopen database
        self.open_db( self.default_db, False )
        cursor = self.conn.cursor()

        # Build a tree data structure from the current database contents.
        cur_data = self.build_tree_data_from_db( cursor )

        # Strip out contents field from all file entries and Name from the
        # top-level before comparing
        exp_data = self.strip_fields( exp_data, 'contents' )
        cur_data = self.strip_fields( cur_data, 'contents' )
        del(exp_data['Name'])
        del(cur_data['Name'])

        diff_results = self.diff_trees( exp_data, cur_data)
        
        # Verify results
        self.assertEqual( diff_results['left'], None)
        self.assertEqual( diff_results['right'], None)
        self.assertNotEqual( len( diff_results['common']['roots'] ), 0)

    def test_root_target(self):
        """Tests delroot subcommand with one root target.
        """

        mod_time = int(time.time())
        check_time = datetime.datetime.fromtimestamp(mod_time)

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1.
        exp_data = self.get_schema_2( str(mod_time), check_time )
        self.populate_db_from_tree( exp_data )
        self.conn.close()

        # Attempt to remove target subtree.
        scr_out = subprocess.check_output([self.script_name, 'delroot', 
                                           'rootA'])

        # Remove target subtree from expected contents
        del(exp_data['roots']['rootA'])

        # Reopen database
        self.open_db( self.default_db, False )
        cursor = self.conn.cursor()

        # Build a tree data structure from the current database contents.
        cur_data = self.build_tree_data_from_db( cursor )
 
        # Strip out contents field from all file entries and Name from the
        # top-level before comparing
        exp_data = self.strip_fields( exp_data, 'contents' )
        cur_data = self.strip_fields( cur_data, 'contents' )
        del(exp_data['Name'])
        del(cur_data['Name'])

        diff_results = self.diff_trees( exp_data, cur_data)

        # Verify results
        self.assertEqual( diff_results['left'], None)
        self.assertEqual( diff_results['right'], None)
        self.assertNotEqual( len( diff_results['common']['roots'] ), 0)
        
    def test_multiple_targets(self):
        """Tests delroot subcommand with multiple targets.
        """

        mod_time = int(time.time())
        check_time = datetime.datetime.fromtimestamp(mod_time)

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1.
        exp_data = self.get_schema_1( str(mod_time), check_time )
        self.populate_db_from_tree( exp_data )
        self.conn.close()

        # Attempt to remove targets.
        scr_out = subprocess.check_output([self.script_name, 'delroot', 
                                           'rootA/TreeA', 
                                           'rootA/LeafB/BunchOfAs.txt'])

        # Remove targets from expected contents
        del(exp_data['roots']['rootA']['children']['TreeA'])
        del(exp_data['roots']['rootA']['children']['LeafB']['children']\
            ['BunchOfAs.txt'])

        # Reopen database
        self.open_db( self.default_db, False )
        cursor = self.conn.cursor()

        # Build a tree data structure from the current database contents.
        cur_data = self.build_tree_data_from_db( cursor )

        # Strip out contents field from all file entries and Name from the
        # top-level before comparing
        exp_data = self.strip_fields( exp_data, 'contents' )
        cur_data = self.strip_fields( cur_data, 'contents' )
        del(exp_data['Name'])
        del(cur_data['Name'])

        diff_results = self.diff_trees( exp_data, cur_data)
        
        # Verify results
        self.assertEqual( diff_results['left'], None)
        self.assertEqual( diff_results['right'], None)
        self.assertNotEqual( len( diff_results['common']['roots'] ), 0)
        
    def test_use_root(self):
        """Tests delroot subcommand with one file target and the --use-root 
        option.
        """

        mod_time = int(time.time())
        check_time = datetime.datetime.fromtimestamp(mod_time)

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1.
        exp_data = self.get_schema_1( str(mod_time), check_time )
        self.populate_db_from_tree( exp_data )
        self.conn.close()

        # Attempt to remove target subtree.
        scr_out = subprocess.check_output([self.script_name, 'delroot', 
                                           '--use-root', 'rootA',
                                           'my_temp/TreeA'])

        # Remove target subtree from expected contents
        del(exp_data['roots']['rootA']['children']['TreeA'])

        # Reopen database
        self.open_db( self.default_db, False )
        cursor = self.conn.cursor()

        # Build a tree data structure from the current database contents.
        cur_data = self.build_tree_data_from_db( cursor )

        # Strip out contents field from all file entries and Name from the
        # top-level before comparing
        exp_data = self.strip_fields( exp_data, 'contents' )
        cur_data = self.strip_fields( cur_data, 'contents' )
        del(exp_data['Name'])
        del(cur_data['Name'])

        diff_results = self.diff_trees( exp_data, cur_data)
        
        # Verify results
        self.assertEqual( diff_results['left'], None)
        self.assertEqual( diff_results['right'], None)
        self.assertNotEqual( len( diff_results['common']['roots'] ), 0)
        
    def test_root_prefix(self):
        """Tests delroot subcommand with one file target and the --root-prefix 
        option.
        """

        mod_time = int(time.time())
        check_time = datetime.datetime.fromtimestamp(mod_time)

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1.
        exp_data = self.get_schema_1( str(mod_time), check_time )
        self.populate_db_from_tree( exp_data )
        self.conn.close()

        # Attempt to remove target subtree.
        scr_out = subprocess.check_output([self.script_name, 'delroot', 
                                           '--root-prefix', 'rootA',
                                           'TreeA'])

        # Remove target subtree from expected contents
        del(exp_data['roots']['rootA']['children']['TreeA'])

        # Reopen database
        self.open_db( self.default_db, False )
        cursor = self.conn.cursor()

        # Build a tree data structure from the current database contents.
        cur_data = self.build_tree_data_from_db( cursor )

        # Strip out contents field from all file entries and Name from the
        # top-level before comparing
        exp_data = self.strip_fields( exp_data, 'contents' )
        cur_data = self.strip_fields( cur_data, 'contents' )
        del(exp_data['Name'])
        del(cur_data['Name'])

        diff_results = self.diff_trees( exp_data, cur_data)
        
        # Verify results
        self.assertEqual( diff_results['left'], None)
        self.assertEqual( diff_results['right'], None)
        self.assertNotEqual( len( diff_results['common']['roots'] ), 0)
        
## TO DO ##
    def test_dry_run(self):
        """Tests delroot subcommand with --dry-run option.
        """

        mod_time = int(time.time())
        check_time = datetime.datetime.fromtimestamp(mod_time)

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1.
        exp_data = self.get_schema_1( str(mod_time), check_time )
        self.populate_db_from_tree( exp_data )
        self.conn.close()

        # Attempt to remove target subtree.
        scr_out = subprocess.check_output([self.script_name, 'delroot', 
                                           '--dry-run', 
                                           'rootA/TreeA'])
        # debug
        print(scr_out)
        # end debug

        # Reopen database
        self.open_db( self.default_db, False )
        cursor = self.conn.cursor()

        # Build a tree data structure from the current database contents.
        cur_data = self.build_tree_data_from_db( cursor )

        # Strip out contents field from all file entries and Name from the
        # top-level before comparing
        exp_data = self.strip_fields( exp_data, 'contents' )
        cur_data = self.strip_fields( cur_data, 'contents' )
        del(exp_data['Name'])
        del(cur_data['Name'])

        diff_results = self.diff_trees( exp_data, cur_data)
        
        # Verify results
        self.assertEqual( diff_results['left'], None)
        self.assertEqual( diff_results['right'], None)
        self.assertNotEqual( len( diff_results['common']['roots'] ), 0)
        
    def test_invalid_target(self):
        """Tests delroot subcommand with an invalid target.
        """

        mod_time = int(time.time())
        check_time = datetime.datetime.fromtimestamp(mod_time)
    #     exp_out = os.linesep.join( ( 'rootA/BunchOfDs.txt is not in database.',
    #                                  '', '' ) )

        # Call open_db, which should create db and its tables
        self.open_db( self.default_db, False )

        # Populate the database with schema 1.
        exp_data = self.get_schema_1( str(mod_time), check_time )
        self.populate_db_from_tree( exp_data )
        self.conn.close()

        # Attempt to remove target subtree.
        scr_out = subprocess.check_output([self.script_name, 'delroot', 
                                           'rootB/TreeA'])
        # Debug
        print(scr_out)
        # end debug

        # Reopen database
        self.open_db( self.default_db, False )
        cursor = self.conn.cursor()

        # Build a tree data structure from the current database contents.
        cur_data = self.build_tree_data_from_db( cursor )

        # Strip out contents field from all file entries and Name from the
        # top-level before comparing
        exp_data = self.strip_fields( exp_data, 'contents' )
        cur_data = self.strip_fields( cur_data, 'contents' )
        del(exp_data['Name'])
        del(cur_data['Name'])

        diff_results = self.diff_trees( exp_data, cur_data)
        
        # Verify results
        self.assertEqual( diff_results['left'], None)
        self.assertEqual( diff_results['right'], None)
        self.assertNotEqual( len( diff_results['common']['roots'] ), 0)
    #     self.assertEqual( scr_out, exp_out )
        
    # def test_file_target_wildcard(self):
    #     """Tests list subcommand with multiple file targets, using wildcards.
    #     """

    #     mod_time = int(time.time())
    #     check_time = datetime.datetime.fromtimestamp(mod_time)
    #     exp_out = os.linesep.join( ( "Files matching 'rootA/LeafB/*.txt':",
    #                                  '', 'BunchOfAs.txt:', '    ID: 4',
    #                                  '    Last Modified: ' + str(
    #                 datetime.datetime.fromtimestamp(mod_time) ),
    #                                  '    Fingerprint: 0x1a0372738bb5b4b8360b' +
    #                                  '47c4504a27e6f4811493',
    #                                  '    Size: 257 bytes', 
    #                                  'BunchOfBs.txt:', '    ID: 5',
    #                                  '    Last Modified: ' + str(
    #                 datetime.datetime.fromtimestamp(mod_time) ),
    #                                  '    Fingerprint: 0xfa75bf047f45891daee8' +
    #                                  'f1fa4cd2bf58876770a5',
    #                                  '    Size: 257 bytes', '',
    #                                  '2 entries listed.', '', '' ) )

    #     # Call open_db, which should create db and its tables
    #     self.open_db( self.default_db, False )

    #     # Populate the database with schema 1.
    #     self.populate_db_from_tree( self.get_schema_1( mod_time, check_time ) )
    #     self.conn.close()

    #     # Attempt to list contents
    #     scr_out = subprocess.check_output([self.script_name, 'list', 
    #                                        'rootA/LeafB/*.txt'])

    #     # Verify output
    #     self.assertEqual( scr_out, exp_out )


# Allow unit test to run on its own
if __name__ == '__main__':
    unittest.main()