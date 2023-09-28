import unittest
from flask import Flask
from main import app

class TestUploadNewRequestsFlow(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_upload_new_requests_page(self):
        response = self.app.get('/upload-new-requests')
        self.assertEqual(response.status_code, 200)

    def test_upload_valid_csv_file(self):
        with open(r'./testfiles/valid_csv.csv', 'rb') as file:
            data = {'new-requests': file}
            response = self.app.post('/upload-new-requests', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.content_type)

    def test_upload_valid_excel_file(self):
        with open(r'./testfiles/sample_new_cases.xlsx', 'rb') as file:
            data = {'new-requests': file}
            response = self.app.post('/upload-new-requests', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.content_type)

    def test_upload_invalid_file_format(self):
        with open(r'./testfiles/CrisisInSoftware.pdf', 'rb') as file:
            data = {'new-requests': file}
            response = self.app.post('/upload-new-requests', data=data, content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 501)
   
if __name__ == '__main__':
    unittest.main()
