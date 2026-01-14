import csv
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

class ExportService:
    def export_to_csv(self, papers):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Title', 'Authors', 'Published Date', 'Summary', 'Link'])
        
        for paper in papers:
            writer.writerow([
                paper.title,
                paper.authors,
                paper.published_date,
                paper.summary[:200] + '...', # Truncate summary for CSV
                paper.pdf_link or paper.id
            ])
        
        return output.getvalue().encode('utf-8')

    def export_to_pdf(self, papers):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph("Reading List", styles['Title']))
        story.append(Spacer(1, 12))

        for paper in papers:
            title_text = f"<b>{paper.title}</b>"
            story.append(Paragraph(title_text, styles['Heading2']))
            
            meta_text = f"Authors: {paper.authors} | Date: {paper.published_date}"
            story.append(Paragraph(meta_text, styles['Normal']))
            story.append(Spacer(1, 6))
            
            if paper.summary:
                summary_text = paper.summary[:500] + "..." if len(paper.summary) > 500 else paper.summary
                story.append(Paragraph(summary_text, styles['Normal']))
            
            if paper.pdf_link:
                link = f'<link href="{paper.pdf_link}">{paper.pdf_link}</link>'
                story.append(Paragraph(link, styles['Normal']))
                
            story.append(Spacer(1, 12))
            story.append(Paragraph("-" * 60, styles['Normal']))
            story.append(Spacer(1, 12))

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
