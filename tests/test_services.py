import unittest
from unittest.mock import patch, MagicMock
from services.arxiv_service import ArxivService
from services.summarizer_service import SummarizerService
from services.export_service import ExportService
from models import Paper
import datetime

class TestServices(unittest.TestCase):
    def setUp(self):
        self.arxiv = ArxivService()
        self.export = ExportService()
        # Mocking Summarizer to avoid loading large models during test
        with patch('services.summarizer_service.pipeline') as mock_pipeline:
             self.summarizer = SummarizerService()
             self.summarizer.summarizer = MagicMock(return_value=[{'summary_text': 'Summary'}])

    @patch('urllib.request.urlopen')
    def test_arxiv_search(self, mock_urlopen):
        # Mock response
        mock_response = MagicMock()
        mock_response.read.return_value = b'''
        <feed xmlns="http://www.w3.org/2005/Atom">
            <entry>
                <id>http://arxiv.org/abs/1234.5678</id>
                <title>Test Paper</title>
                <summary>Abstract</summary>
                <author><name>Author One</name></author>
                <published>2023-01-01T00:00:00Z</published>
                <link href="http://arxiv.org/abs/1234.5678" rel="alternate" type="text/html"/>
                <link href="http://arxiv.org/pdf/1234.5678" rel="related" type="application/pdf"/>
            </entry>
        </feed>
        '''
        mock_urlopen.return_value = mock_response
        
        results = self.arxiv.search_papers('quantum')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Test Paper')
        self.assertEqual(results[0]['id'], '1234.5678')

    def test_summarizer(self):
        # Since we mocked the pipeline in setUp, we just digest the mock return
        summary = self.summarizer.summarize("Long text")
        self.assertEqual(summary, "Summary")
        
        bullets = self.summarizer.generate_bullets("Long text")
        self.assertTrue(len(bullets) > 0)

    def test_export_csv(self):
        paper = Paper(
            title="Test", 
            authors="Me", 
            published_date=datetime.date(2023, 1, 1), 
            summary="Sum", 
            pdf_link="http://pdf"
        )
        csv_data = self.export.export_to_csv([paper])
        self.assertTrue(b"Test" in csv_data)
        self.assertTrue(b"Me" in csv_data)

    def test_export_pdf(self):
        paper = Paper(
            title="Test", 
            authors="Me", 
            published_date=datetime.date(2023, 1, 1), 
            summary="Sum", 
            pdf_link="http://pdf"
        )
        pdf_data = self.export.export_to_pdf([paper])
        self.assertTrue(pdf_data.startswith(b'%PDF'))

if __name__ == '__main__':
    unittest.main()
