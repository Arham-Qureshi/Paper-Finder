import logging
import requests
import urllib.parse
from datetime import datetime

logger = logging.getLogger(__name__)

class SemanticScholarService:
    BASE_URL = 'https://api.semanticscholar.org/graph/v1/paper/search'

    def search_papers(self, query, max_results=5):
        try:
            params = {
                'query': query,
                'limit': max_results,
                'fields': 'paperId,title,abstract,authors,year,openAccessPdf,url,publicationDate'
            }
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            papers = []
            for entry in data.get('data', []):
                try:
                    # Normalize data
                    authors = [author.get('name') for author in entry.get('authors', [])]
                    
                    # Handle date
                    pub_date = None
                    if entry.get('publicationDate'):
                        try:
                            pub_date = datetime.strptime(entry.get('publicationDate'), '%Y-%m-%d')
                        except ValueError:
                            pass
                    if not pub_date and entry.get('year'):
                         pub_date = datetime(entry.get('year'), 1, 1)

                    pdf_link = None
                    if entry.get('openAccessPdf'):
                        pdf_link = entry.get('openAccessPdf').get('url')

                    paper = {
                        'id': entry.get('paperId'),
                        'title': entry.get('title'),
                        'summary': entry.get('abstract') or "No abstract available.",
                        'authors': authors,
                        'published': pub_date,
                        'pdf_link': pdf_link,
                        'arxiv_url': entry.get('url'),
                        'source': 'Semantic Scholar'
                    }
                    papers.append(paper)
                except Exception as entry_e:
                    logger.warning(f"Error parsing Semantic Scholar entry: {entry_e}")
                    continue
            
            return papers
        except Exception as e:
            logger.error(f"Error fetching from Semantic Scholar: {e}")
            return []
