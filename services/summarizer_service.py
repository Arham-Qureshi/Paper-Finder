from transformers import pipeline
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SummarizerService:
    def __init__(self, model_name="sshleifer/distilbart-cnn-12-6"):
        """
        Initialize the summarization service.
        Model is loaded lazily to improve startup time.
        """
        self.model_name = model_name
        self.summarizer = None

    def _load_model(self):
        if self.summarizer:
            return

        try:
            logger.info(f"Loading summarizer model {self.model_name}...")
            self.summarizer = pipeline("summarization", model=self.model_name)
            logger.info(f"Summarizer model {self.model_name} loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load summarizer model: {e}")
            self.summarizer = None

    def summarize(self, text, max_length=150, min_length=50):
        if not self.summarizer:
            self._load_model()
            
        if not self.summarizer:
            return "Summarization model is not active."
        
        try:
            # Chunking could be added here if text is too long (token limit)
            # For now, we truncate blindly if needed or rely on pipeline truncation
            # The pipeline usually handles truncation but explicit header/truncation is safer
            
            # Simple summarization call
            summary = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False, truncation=True)
            return summary[0]['summary_text']
        except Exception as e:
            logger.error(f"Error during summarization: {e}")
            return "Error generating summary."

    def generate_bullets(self, text):
        # A crude way to get bullets is to ask for a longer summary and split it, 
        # or just format the output. For a specialized bullet-point model, we'd need a different prompt/model.
        # Here we'll just generate a summary and try to split it by sentences for 'bullets'.
        summary = self.summarize(text, max_length=200, min_length=100)
        sentences = summary.split('. ')
        bullets = [s.strip() + '.' for s in sentences if s.strip()]
        return bullets

# Singleton instance (optional, or instantiate in app factory)
# summarizer = SummarizerService()
