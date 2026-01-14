import logging
import requests
import urllib.parse
from datetime import datetime

logger = logging.getLogger(__name__)

class OpenAlexService:
    BASE_URL = 'https://api.openalex.org/works'

    def search_papers(self, query, max_results=5):
        try:
            params = {
                'search': query,
                'per-page': max_results,
                'filter': 'has_fulltext:true' # Optional: ensure full text is somewhat available or pdf
            }
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            papers = []
            for entry in data.get('results', []):
                try:
                    # Normalize data
                    authors = [author.get('author', {}).get('display_name') for author in entry.get('authorships', [])]
                    
                    # Handle date
                    pub_date = None
                    if entry.get('publication_date'):
                         try:
                            pub_date = datetime.strptime(entry.get('publication_date'), '%Y-%m-%d')
                         except ValueError:
                             pass
                    
                    # Get abstract (OpenAlex provides inverted index, rebuilding is needed or use different field)
                    # OpenAlex doesn't always provide plain text abstract directly in list view easily without reconstruction
                    # Use 'display_name' or title if abstract is hard.
                    # Workaround: OpenAlex abstract is inverted index. For simplicity in this demo, we might skip full abstract 
                    # reconstruction or use a placeholder if not simple. 
                    # Actually, let's try to get 'abstract_inverted_index' if we want to reconstruct, but that's complex.
                    # For now, let's look for a snippet or just use "Abstract available at source".
                    # Better: Check if 'best_oa_location' has a pdf.
                    
                    summary = "Abstract reconstruction from OpenAlex inverted index is complex. Please view original source."
                    # If we really want it, we'd reconstruct it. Let's keep it simple for MVP.

                    pdf_link = None
                    if entry.get('open_access') and entry.get('open_access').get('is_oa'):
                        pdf_link = entry.get('best_oa_location', {}).get('pdf_url')
                    
                    source_url = entry.get('id') # usually https://openalex.org/W...

                    paper = {
                        'id': entry.get('id').split('/')[-1], # Extract ID
                        'title': entry.get('title'),
                        'summary': summary,
                        'authors': authors,
                        'published': pub_date,
                        'pdf_link': pdf_link,
                        'arxiv_url': source_url,
                        'source': 'OpenAlex'
                    }
                    papers.append(paper)
                except Exception as entry_e:
                    logger.warning(f"Error parsing OpenAlex entry: {entry_e}")
                    continue
            
            return papers
        except Exception as e:
            logger.error(f"Error fetching from OpenAlex: {e}")
            return []
