from .arxiv_service import ArxivService
from .semantic_scholar_service import SemanticScholarService
from .open_alex_service import OpenAlexService
import logging
import concurrent.futures

logger = logging.getLogger(__name__)

class PaperAggregatorService:
    def __init__(self):
        self.arxiv = ArxivService()
        self.semantic = SemanticScholarService()
        self.openalex = OpenAlexService()
        # Enable all by default
        self.services = [self.arxiv, self.semantic, self.openalex]

    def search_papers(self, query, max_results_per_service=5):
        all_papers = []
        
        # Sequential for safety first, but concurrent is better. 
        # Let's try simple sequential to debug easily, if slow we optimize.
        # Actually, let's just do sequential as per plan.
        
        for service in self.services:
            try:
                papers = service.search_papers(query, max_results=max_results_per_service)
                # Tag source if not already
                for p in papers:
                    if 'source' not in p:
                        p['source'] = service.__class__.__name__.replace('Service', '')
                all_papers.extend(papers)
            except Exception as e:
                logger.error(f"Error in aggregator with service {service}: {e}")
                
        # Deduplication could go here (by title similarity or id if possible)
        # For now, just return all mixed.
        return all_papers
