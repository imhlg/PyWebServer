import os
import tempfile
import unittest

import served


class AppFeatureTests(unittest.TestCase):
    def setUp(self):
        self.app = served.app.test_client()

    def test_jd_listing_endpoint_returns_uploaded_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            original_folder = served.JD_FOLDER
            served.JD_FOLDER = tmpdir
            try:
                with open(os.path.join(tmpdir, 'sample.txt'), 'w', encoding='utf-8') as handle:
                    handle.write('sample jd')

                response = self.app.get('/api/jd-files')

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.mimetype, 'application/json')
                self.assertIn('sample.txt', response.get_json()['files'])
            finally:
                served.JD_FOLDER = original_folder

    def test_projects_page_renders_successfully(self):
        response = self.app.get('/projects.html')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Python projects showcase', response.data)

    def test_forum_posts_endpoint_returns_saved_posts(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            original_forum_file = served.FORUM_FILE
            served.FORUM_FILE = os.path.join(tmpdir, 'forum-responses.txt')
            try:
                with open(served.FORUM_FILE, 'w', encoding='utf-8') as handle:
                    handle.write('Ada,\tHello world\n')

                response = self.app.get('/api/forum-posts')

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.mimetype, 'application/json')
                self.assertIn('Ada', response.get_json()['posts'][0]['author'])
                self.assertIn('Hello world', response.get_json()
                              ['posts'][0]['message'])
            finally:
                served.FORUM_FILE = original_forum_file


if __name__ == '__main__':
    unittest.main()
