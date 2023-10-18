import unittest
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
    
    def test_upload_missing_file(self):
        data = {}  # Empty data to simulate missing file
        response = self.app.post('/upload-new-requests', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 404)

    def helper_open_file(self):
        with open(r'./testfiles/invalid_csv.csv', 'rb') as file:
            data = {'new-requests': file}
            response = self.app.post('/upload-new-requests', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.content_type)
        return response

    def test_upload_file_with_invalid_customer_id(self):
        response = self.helper_open_file()
        self.assertIn('Invalid value in customer_id. Must contain digits only and not start from 0.', response.data.decode('utf-8'))
    
    def test_upload_file_with_invalid_outreach_date_future(self):
        response = self.helper_open_file()
        self.assertIn('Invalid date in Outreach_Date. Cannot be in the future.', response.data.decode('utf-8'))
    
    def test_upload_file_with_invalid_outreach_date_format(self):
        response = self.helper_open_file()
        self.assertIn('Invalid date format in Outreach_Date.', response.data.decode('utf-8'))
   
if __name__ == '__main__':
    unittest.main()