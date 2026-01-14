import logging
import urllib.parse
import urllib.request
import feedparser
from datetime import datetime

logger = logging.getLogger(__name__)

class ArxivService:
    BASE_URL = 'http://export.arxiv.org/api/query?'

    def search_papers(self, query, max_results=10, start=0, sort_by='relevance', sort_order='descending'):
        # Construct the query
        search_query = f'search_query=all:{query}&start={start}&max_results={max_results}&sortBy={sort_by}&sortOrder={sort_order}'
        url = self.BASE_URL + search_query
        
        try:
            response = urllib.request.urlopen(url).read()
            feed = feedparser.parse(response)
            
            papers = []
            for entry in feed.entries:
                try:
                    paper = {
                        'id': entry.id.split('/abs/')[-1],
                        'title': entry.title,
                        'summary': entry.summary,
                        'authors': [author.name for author in entry.authors],
                        'published': datetime.strptime(entry.published, '%Y-%m-%dT%H:%M:%SZ'),
                        'pdf_link': next((link.href for link in entry.links if link.type == 'application/pdf'), None),
                        'arxiv_url': entry.link
                    }
                    papers.append(paper)
                except Exception as entry_e:
                    logger.warning(f"Error parsing entry: {entry_e}")
                    continue
            
            return papers
        except Exception as e:
            logger.error(f"Error fetching from arXiv: {e}")
            return []
