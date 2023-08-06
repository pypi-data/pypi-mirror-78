from unittest import mock
import unittest
import sys
import os
import shutil
import io
import zipfile
from flask import current_app
import webscrapbook
from webscrapbook import WSB_DIR, WSB_LOCAL_CONFIG
from webscrapbook import app as wsbapp

root_dir = os.path.abspath(os.path.dirname(__file__))
server_root = os.path.join(root_dir, 'test_app_helpers')

mocking = None

def setUpModule():
    # mock out WSB_USER_CONFIG
    global mocking
    mocking = mock.patch('webscrapbook.WSB_USER_CONFIG', server_root)
    mocking.start()

def tearDownModule():
    # stop mock
    mocking.stop()

class TestFunctions(unittest.TestCase):
    def test_is_local_access(self):
        root = os.path.join(root_dir, 'test_app_helpers', 'general')
        app = wsbapp.make_app(root)

        # host is localhost
        with app.test_request_context('/',
                base_url='http://127.0.0.1',
                environ_base={'REMOTE_ADDR': '192.168.0.100'}):
            self.assertTrue(wsbapp.is_local_access())

        # host (with port) is localhost
        with app.test_request_context('/',
                base_url='http://127.0.0.1:8000',
                environ_base={'REMOTE_ADDR': '192.168.0.100'}):
            self.assertTrue(wsbapp.is_local_access())

        # remote is localhost
        with app.test_request_context('/',
                base_url='http://192.168.0.1',
                environ_base={'REMOTE_ADDR': '127.0.0.1'}):
            self.assertTrue(wsbapp.is_local_access())

        # host = remote
        with app.test_request_context('/',
                base_url='http://example.com',
                environ_base={'REMOTE_ADDR': 'example.com'}):
            self.assertTrue(wsbapp.is_local_access())

        # host (with port) = remote
        with app.test_request_context('/',
                base_url='http://example.com:8000',
                environ_base={'REMOTE_ADDR': 'example.com'}):
            self.assertTrue(wsbapp.is_local_access())

        # otherwise non-local
        with app.test_request_context('/',
                base_url='http://example.com',
                environ_base={'REMOTE_ADDR': '192.168.0.100'}):
            self.assertFalse(wsbapp.is_local_access())

    def test_get_archive_path1(self):
        """Basic logit for a sub-archive path."""
        root = os.path.join(root_dir, 'test_app_helpers', 'general')
        app = wsbapp.make_app(root)
        with app.app_context():
            tempfile = os.path.join(root, 'entry.zip')
            try:
                with zipfile.ZipFile(tempfile, 'w') as zip:
                    pass

                self.assertEqual(wsbapp.get_archive_path('entry.zip'), (None, None))
                self.assertEqual(wsbapp.get_archive_path('entry.zip!'), (None, None))
                self.assertEqual(wsbapp.get_archive_path('entry.zip!/'), (tempfile, ''))
                self.assertEqual(wsbapp.get_archive_path('entry.zip!/subdir'), (tempfile, 'subdir'))
                self.assertEqual(wsbapp.get_archive_path('entry.zip!/subdir/'), (tempfile, 'subdir'))
                self.assertEqual(wsbapp.get_archive_path('entry.zip!/index.html'), (tempfile, 'index.html'))
            finally:
                try:
                    os.remove(tempfile)
                except FileNotFoundError:
                    pass

    def test_get_archive_path2(self):
        """Handle conflicting file or directory."""
        # entry.zip!/entry1.zip!/ = entry.zip!/entry1.zip! >
        # entry.zip!/entry1.zip >
        # entry.zip!/ = entry.zip! >
        # entry.zip
        root = os.path.join(root_dir, 'test_app_helpers', 'general')
        app = wsbapp.make_app(root)
        with app.app_context():
            # entry.zip!/entry1.zip!/ > entry.zip!/entry1.zip
            try:
                os.makedirs(os.path.join(root, 'entry.zip!', 'entry1.zip!'), exist_ok=True)
                with zipfile.ZipFile(os.path.join(root, 'entry.zip!', 'entry1.zip'), 'w') as zip:
                    pass
                with zipfile.ZipFile(os.path.join(root, 'entry.zip'), 'w') as zip:
                    pass

                self.assertEqual(
                    wsbapp.get_archive_path('entry.zip!/entry1.zip!/'),
                    (None, None))
            finally:
                try:
                    shutil.rmtree(os.path.join(root, 'entry.zip!'))
                except NotADirectoryError:
                    os.remove(os.path.join(root, 'entry.zip!'))
                except FileNotFoundError:
                    pass
                try:
                    os.remove(os.path.join(root, 'entry.zip'))
                except FileNotFoundError:
                    pass

            # entry.zip!/entry1.zip! > entry.zip!/entry1.zip
            try:
                os.makedirs(os.path.join(root, 'entry.zip!'), exist_ok=True)
                with open(os.path.join(root, 'entry.zip!', 'entry1.zip!'), 'w') as f:
                    pass
                with zipfile.ZipFile(os.path.join(root, 'entry.zip!', 'entry1.zip'), 'w') as zip:
                    pass
                with zipfile.ZipFile(os.path.join(root, 'entry.zip'), 'w') as zip:
                    pass

                self.assertEqual(
                    wsbapp.get_archive_path('entry.zip!/entry1.zip!/'),
                    (None, None))
            finally:
                try:
                    shutil.rmtree(os.path.join(root, 'entry.zip!'))
                except NotADirectoryError:
                    os.remove(os.path.join(root, 'entry.zip!'))
                except FileNotFoundError:
                    pass
                try:
                    os.remove(os.path.join(root, 'entry.zip'))
                except FileNotFoundError:
                    pass

            # entry.zip!/entry1.zip > entry.zip!/
            try:
                os.makedirs(os.path.join(root, 'entry.zip!'), exist_ok=True)
                with zipfile.ZipFile(os.path.join(root, 'entry.zip!', 'entry1.zip'), 'w') as zip:
                    pass
                with zipfile.ZipFile(os.path.join(root, 'entry.zip'), 'w') as zip:
                    pass

                self.assertEqual(
                    wsbapp.get_archive_path('entry.zip!/entry1.zip!/'),
                    (os.path.join(root, 'entry.zip!', 'entry1.zip'), ''))
            finally:
                try:
                    shutil.rmtree(os.path.join(root, 'entry.zip!'))
                except NotADirectoryError:
                    os.remove(os.path.join(root, 'entry.zip!'))
                except FileNotFoundError:
                    pass
                try:
                    os.remove(os.path.join(root, 'entry.zip'))
                except FileNotFoundError:
                    pass

            # entry.zip!/ > entry.zip
            try:
                os.makedirs(os.path.join(root, 'entry.zip!'), exist_ok=True)
                with zipfile.ZipFile(os.path.join(root, 'entry.zip'), 'w') as zip:
                    pass

                self.assertEqual(
                    wsbapp.get_archive_path('entry.zip!/entry1.zip!/'),
                    (None, None))
            finally:
                try:
                    shutil.rmtree(os.path.join(root, 'entry.zip!'))
                except NotADirectoryError:
                    os.remove(os.path.join(root, 'entry.zip!'))
                except FileNotFoundError:
                    pass
                try:
                    os.remove(os.path.join(root, 'entry.zip'))
                except FileNotFoundError:
                    pass

            # entry.zip! > entry.zip
            try:
                with open(os.path.join(root, 'entry.zip!'), 'w') as f:
                    pass
                with zipfile.ZipFile(os.path.join(root, 'entry.zip'), 'w') as zip:
                    pass

                self.assertEqual(
                    wsbapp.get_archive_path('entry.zip!/entry1.zip!/'),
                    (None, None))
            finally:
                try:
                    shutil.rmtree(os.path.join(root, 'entry.zip!'))
                except NotADirectoryError:
                    os.remove(os.path.join(root, 'entry.zip!'))
                except FileNotFoundError:
                    pass
                try:
                    os.remove(os.path.join(root, 'entry.zip'))
                except FileNotFoundError:
                    pass

            # entry.zip
            try:
                with zipfile.ZipFile(os.path.join(root, 'entry.zip'), 'w') as zip:
                    pass

                self.assertEqual(
                    wsbapp.get_archive_path('entry.zip!/entry1.zip!/'),
                    (os.path.join(root, 'entry.zip'), 'entry1.zip!'))
            finally:
                try:
                    shutil.rmtree(os.path.join(root, 'entry.zip!'))
                except NotADirectoryError:
                    os.remove(os.path.join(root, 'entry.zip!'))
                except FileNotFoundError:
                    pass
                try:
                    os.remove(os.path.join(root, 'entry.zip'))
                except FileNotFoundError:
                    pass

            # other
            try:
                with open(os.path.join(root, 'entry.zip'), 'w') as f:
                    pass

                self.assertEqual(
                    wsbapp.get_archive_path('entry.zip!/entry1.zip!/'),
                    (None, None))
            finally:
                try:
                    shutil.rmtree(os.path.join(root, 'entry.zip!'))
                except NotADirectoryError:
                    os.remove(os.path.join(root, 'entry.zip!'))
                except FileNotFoundError:
                    pass
                try:
                    os.remove(os.path.join(root, 'entry.zip'))
                except FileNotFoundError:
                    pass

    @mock.patch('webscrapbook.util.encrypt', side_effect=webscrapbook.util.encrypt)
    def test_get_permission1(self, mock_encrypt):
        """Return 'all' anyway if no auth section."""
        root = os.path.join(root_dir, 'test_app_helpers', 'get_permission1')
        app = wsbapp.make_app(root)
        with app.app_context():
            # util.encrypt should NOT be called
            self.assertEqual(wsbapp.get_permission(None), 'all')
            mock_encrypt.assert_not_called()

            self.assertEqual(wsbapp.get_permission({'username': '', 'password': ''}), 'all')
            mock_encrypt.assert_not_called()

            self.assertEqual(wsbapp.get_permission({'username': '', 'password': 'pass'}), 'all')
            mock_encrypt.assert_not_called()

            self.assertEqual(wsbapp.get_permission({'username': 'user', 'password': ''}), 'all')
            mock_encrypt.assert_not_called()

            self.assertEqual(wsbapp.get_permission({'username': 'user', 'password': 'pass'}), 'all')
            mock_encrypt.assert_not_called()

    @mock.patch('webscrapbook.util.encrypt', side_effect=webscrapbook.util.encrypt)
    def test_get_permission2(self, mock_encrypt):
        """Return corresponding permission for the matched user and '' for unmatched."""
        root = os.path.join(root_dir, 'test_app_helpers', 'get_permission2')
        app = wsbapp.make_app(root)
        with app.app_context():
            # util.encrypt should be called with the inputting password
            # and the salt and method for the matched user
            mock_encrypt.reset_mock()

            self.assertEqual(wsbapp.get_permission({'username': 'user1', 'password': 'pass1'}), '')
            mock_encrypt.assert_called_with('pass1', '', 'plain')

            self.assertEqual(wsbapp.get_permission({'username': 'user2', 'password': 'pass2'}), 'view')
            mock_encrypt.assert_called_with('pass2', 'salt', 'plain')

            self.assertEqual(wsbapp.get_permission({'username': 'user3', 'password': 'pass3'}), 'read')
            mock_encrypt.assert_called_with('pass3', '', 'sha1')

            self.assertEqual(wsbapp.get_permission({'username': 'user4', 'password': 'pass4'}), 'all')
            mock_encrypt.assert_called_with('pass4', 'salt4', 'sha256')

            # Password check should be handled by util.encrypt properly.
            # Here are just some quick fail tests for certain cases:
            # - empty input should not work
            # - inputting password + salt should not work
            # - inputting hashed value should not work
            mock_encrypt.reset_mock()

            self.assertEqual(wsbapp.get_permission({'username': 'user4', 'password': ''}), '')
            mock_encrypt.assert_called_with('', 'salt4', 'sha256')

            self.assertEqual(wsbapp.get_permission({'username': 'user4', 'password': 'salt4'}), '')
            mock_encrypt.assert_called_with('salt4', 'salt4', 'sha256')

            self.assertEqual(wsbapp.get_permission({'username': 'user4', 'password': '49d1445a2989c509c5b5b1f78e092e3f30f05b1d219fd975ac77ff645ea68d53'}), '')
            mock_encrypt.assert_called_with('49d1445a2989c509c5b5b1f78e092e3f30f05b1d219fd975ac77ff645ea68d53', 'salt4', 'sha256')

            # util.encrypt should NOT be called for an unmatched user
            mock_encrypt.reset_mock()

            self.assertEqual(wsbapp.get_permission(None), '')
            mock_encrypt.assert_not_called()

            self.assertEqual(wsbapp.get_permission({'username': '', 'password': ''}), '')
            mock_encrypt.assert_not_called()

            self.assertEqual(wsbapp.get_permission({'username': '', 'password': 'pass'}), '')
            mock_encrypt.assert_not_called()

            self.assertEqual(wsbapp.get_permission({'username': 'userx', 'password': ''}), '')
            mock_encrypt.assert_not_called()

            self.assertEqual(wsbapp.get_permission({'username': 'userx', 'password': 'pass'}), '')
            mock_encrypt.assert_not_called()

    @mock.patch('webscrapbook.util.encrypt', side_effect=webscrapbook.util.encrypt)
    def test_get_permission3(self, mock_encrypt):
        """Use empty user and password if not provided."""
        root = os.path.join(root_dir, 'test_app_helpers', 'get_permission3')
        app = wsbapp.make_app(root)
        with app.app_context():
            self.assertEqual(wsbapp.get_permission(None), 'view')
            mock_encrypt.assert_called_with('', 'salt', 'plain')

            self.assertEqual(wsbapp.get_permission({'username': '', 'password': ''}), 'view')
            mock_encrypt.assert_called_with('', 'salt', 'plain')

    @mock.patch('webscrapbook.util.encrypt', side_effect=webscrapbook.util.encrypt)
    def test_get_permission4(self, mock_encrypt):
        """Use permission for the first matched user and password."""
        root = os.path.join(root_dir, 'test_app_helpers', 'get_permission4')
        app = wsbapp.make_app(root)
        with app.app_context():
            mock_encrypt.reset_mock()
            self.assertEqual(wsbapp.get_permission({'username': '', 'password': ''}), 'view')
            mock_encrypt.assert_called_once_with('', 'salt', 'plain')

            mock_encrypt.reset_mock()
            self.assertEqual(wsbapp.get_permission({'username': 'user1', 'password': 'pass1'}), 'read')
            self.assertEqual(mock_encrypt.call_args_list[0][0], ('pass1', 'salt', 'plain'))
            self.assertEqual(mock_encrypt.call_args_list[1][0], ('pass1', 'salt', 'plain'))

    def test_verify_authorization(self):
        for action in {'view', 'source', 'static'}:
            with self.subTest(action=action):
                self.assertFalse(wsbapp.verify_authorization('', action))
                self.assertTrue(wsbapp.verify_authorization('view', action))
                self.assertTrue(wsbapp.verify_authorization('read', action))
                self.assertTrue(wsbapp.verify_authorization('all', action))

        for action in {'list', 'edit', 'editx', 'exec', 'browse', 'config', 'unknown'}:
            with self.subTest(action=action):
                self.assertFalse(wsbapp.verify_authorization('', action))
                self.assertFalse(wsbapp.verify_authorization('view', action))
                self.assertTrue(wsbapp.verify_authorization('read', action))
                self.assertTrue(wsbapp.verify_authorization('all', action))

        for action in {'token', 'lock', 'unlock', 'mkdir', 'save', 'delete', 'move', 'copy'}:
            with self.subTest(action=action):
                self.assertFalse(wsbapp.verify_authorization('', action))
                self.assertFalse(wsbapp.verify_authorization('view', action))
                self.assertFalse(wsbapp.verify_authorization('read', action))
                self.assertTrue(wsbapp.verify_authorization('all', action))

    def test_make_app1(self):
        # pass root
        root = os.path.join(root_dir, 'test_app_helpers', 'make_app1')

        app = wsbapp.make_app(root)
        with app.app_context():
            self.assertEqual(current_app.config['WEBSCRAPBOOK_RUNTIME']['config']['app']['name'], 'mywsb1')

    def test_make_app2(self):
        # pass root, config
        root = os.path.join(root_dir, 'test_app_helpers', 'make_app1')
        config_dir = os.path.join(root_dir, 'test_app_helpers', 'make_app2')
        config = webscrapbook.Config()
        config.load(config_dir)

        app = wsbapp.make_app(root, config)
        with app.app_context():
            self.assertEqual(current_app.config['WEBSCRAPBOOK_RUNTIME']['config']['app']['name'], 'mywsb2')

if __name__ == '__main__':
    unittest.main()
