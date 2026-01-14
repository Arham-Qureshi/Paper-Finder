from flask import Blueprint, render_template, request, jsonify, send_file, flash, redirect, url_for
from models import db, Paper, Bookmark, SearchHistory
from services.aggregator_service import PaperAggregatorService
from services.arxiv_service import ArxivService # Kept for fallback or specific ID lookup if needed
from services.summarizer_service import SummarizerService
from services.export_service import ExportService
import datetime
import io

main = Blueprint('main', __name__)

aggregator_service = PaperAggregatorService()
arxiv_service = ArxivService() # Kept for specific ID lookups if aggregator doesn't support get_by_id yet
summarizer_service = SummarizerService() # Note: This will load the model on startup!
export_service = ExportService()

@main.route('/')
def index():
    history = SearchHistory.query.order_by(SearchHistory.timestamp.desc()).limit(5).all()
    return render_template('index.html', history=history)

@main.route('/search')
def search():
    query = request.args.get('q')
    if not query:
        return redirect(url_for('main.index'))
        
    # Log search
    search_entry = SearchHistory(search_query=query)
    db.session.add(search_entry)
    db.session.commit()
        
    # Use aggregator
    papers = aggregator_service.search_papers(query)
    return render_template('results.html', papers=papers, query=query)

@main.route('/paper/<path:paper_id>')
def paper_detail(paper_id):
    # Check if we have cached this paper details in DB, if not fetch from arXiv? 
    # Since arXiv ID might contain slashes (e.g., cond-mat/0001234), we map logic carefully.
    # For simplicity, we re-fetch or pass data. 
    # A better approach: We search by ID using the same service.
    
    # NOTE: paper_id comes from URL, might be encoded.
    # In search results, we pass links like /paper/1234.5678
    
    # Try fetching from DB first
    paper = Paper.query.get(paper_id)
    if not paper:
        # Fetch from arXiv by ID
        # Reuse search with id_list approach or just search
        # ArxivService needs a 'get_by_id'
        results = arxiv_service.search_papers(f'id:{paper_id}', max_results=1)
        if results:
            data = results[0]
            # Cache it? Maybe not yet, only when bookmarked.
            # But to show details, 'data' dict is enough for template.
            # Let's mock a Paper object or use dict in template
            paper = data
        else:
            flash("Paper not found", "error")
            return redirect(url_for('main.index'))
            
    return render_template('detail.html', paper=paper)

@main.route('/summarize', methods=['POST'])
def summarize():
    text = request.json.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    summary = summarizer_service.summarize(text)
    bullets = summarizer_service.generate_bullets(text)
    
    return jsonify({
        'summary': summary,
        'bullets': bullets
    })

@main.route('/bookmarks')
def bookmarks():
    bookmarks = Bookmark.query.all()
    return render_template('bookmarks.html', bookmarks=bookmarks)

@main.route('/bookmark/add', methods=['POST'])
def add_bookmark():
    data = request.json
    paper_id = data.get('paper_id')
    
    if not paper_id:
        return jsonify({'error': 'Paper ID required'}), 400
        
    # Check if paper exists in DB, if not create it (we need details)
    paper = Paper.query.get(paper_id)
    if not paper:
        # In a real app, passing all details from frontend is risky/messy. 
        # Ideally we fetch from arXiv service again or use the cached data we displayed.
        # Here we'll expect the frontend to pass minimal necessary info or we re-fetch.
        # For simplicity, let's assume we re-fetch if missing, or user passed title/etc.
        
        # Let's try to fetch from arXiv again to be safe and consistent
        results = arxiv_service.search_papers(f'id:{paper_id}', max_results=1)
        if results:
            p_data = results[0]
            paper = Paper(
                id=p_data['id'],
                title=p_data['title'],
                authors=', '.join(p_data['authors']),
                published_date=p_data['published'],
                summary=p_data['summary'],
                pdf_link=p_data['pdf_link'],
                ai_summary_short=None, # Generated on demand
                ai_summary_bullets=None
            )
            db.session.add(paper)
            db.session.commit()
        else:
             return jsonify({'error': 'Paper not found on arXiv'}), 404

    # Check if already bookmarked
    if Bookmark.query.filter_by(paper_id=paper_id).first():
       return jsonify({'message': 'Already bookmarked'}), 200

    bookmark = Bookmark(paper_id=paper_id)
    db.session.add(bookmark)
    db.session.commit()
    
    return jsonify({'message': 'Bookmark added successfully'}), 201

@main.route('/export/<format>')
def export_bookmarks(format):
    bookmarks = Bookmark.query.all()
    papers = [b.paper for b in bookmarks]
    
    if format == 'csv':
        data = export_service.export_to_csv(papers)
        mimetype = 'text/csv'
        filename = 'reading_list.csv'
    elif format == 'pdf':
        data = export_service.export_to_pdf(papers)
        mimetype = 'application/pdf'
        filename = 'reading_list.pdf'
    else:
        return "Invalid format", 400
        
    return send_file(
        io.BytesIO(data),
        mimetype=mimetype,
        as_attachment=True,
        download_name=filename
    )
