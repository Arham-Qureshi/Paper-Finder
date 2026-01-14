from services.arxiv_service import ArxivService
from services.semantic_scholar_service import SemanticScholarService
from services.open_alex_service import OpenAlexService
from services.aggregator_service import PaperAggregatorService

def test_services():
    query = "deep learning"
    
    print("Testing Arxiv...")
    try:
        arxiv = ArxivService()
        res1 = arxiv.search_papers(query, max_results=1)
        print(f"Arxiv found: {len(res1)}")
        if res1: print(f"Sample: {res1[0]['title']}")
    except Exception as e:
        print(f"Arxiv failed: {e}")

    print("\nTesting Semantic Scholar...")
    try:
        ss = SemanticScholarService()
        res2 = ss.search_papers(query, max_results=1)
        print(f"Semantic Scholar found: {len(res2)}")
        if res2: print(f"Sample: {res2[0]['title']}")
    except Exception as e:
        print(f"Semantic Scholar failed: {e}")
    
    print("\nTesting OpenAlex...")
    try:
        oa = OpenAlexService()
        res3 = oa.search_papers(query, max_results=1)
        print(f"OpenAlex found: {len(res3)}")
        if res3: print(f"Sample: {res3[0]['title']}")
    except Exception as e:
        print(f"OpenAlex failed: {e}")

    print("\nTesting Aggregator...")
    try:
        agg = PaperAggregatorService()
        res_agg = agg.search_papers(query, max_results_per_service=2)
        print(f"Aggregator found: {len(res_agg)}")
        sources = set(p.get('source', 'Unknown') for p in res_agg)
        print(f"Sources found: {sources}")
    except Exception as e:
        print(f"Aggregator failed: {e}")

if __name__ == "__main__":
    test_services()
