"""Text similarity matching using TF-IDF + Cosine similarity with meaningful word filtering"""
import numpy as np
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SimilarityMatcher:
    """Matches answers using TF-IDF + Cosine similarity on meaningful words only"""
    
    # Function words to exclude (prepositions, articles, conjunctions, etc.)
    STOP_WORDS = {
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 'her', 'his',
        'i', 'if', 'in', 'into', 'is', 'it', 'its', 'of', 'on', 'or', 'that', 'the', 'to', 'was',
        'we', 'which', 'who', 'will', 'with', 'you', 'your', 'can', 'could', 'would', 'should',
        'may', 'might', 'must', 'do', 'does', 'did', 'have', 'had', 'been', 'being', 'having',
        'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other', 'same', 'such', 'no',
        'nor', 'not', 'only', 'so', 'than', 'too', 'very', 'also', 'up', 'out', 'about',
        'q', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
        'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'  # Single letters often from OCR artifacts
    }
    
    def __init__(self, answer_key: List[str], similarity_threshold: float = 0.70):
        """Initialize matcher with answer key"""
        self.answer_key = answer_key
        self.similarity_threshold = similarity_threshold
        
        # Filter answer key to keep only meaningful words
        filtered_answers = [self._filter_meaningful_words(answer) for answer in answer_key]
        
        self.vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 3), lowercase=True, max_features=500)
        self.answer_vectors = self.vectorizer.fit_transform(filtered_answers)
    
    def _filter_meaningful_words(self, text: str) -> str:
        """Remove function words, keep only meaningful words"""
        # Split into words and convert to lowercase
        words = text.lower().split()
        
        # Filter out stop words
        meaningful_words = [w for w in words if w not in self.STOP_WORDS and len(w) > 1]
        
        return ' '.join(meaningful_words)
    
    def match(self, student_answer: str) -> float:
        """Calculate best similarity score for student answer (0.0-1.0)"""
        try:
            # Filter student answer to keep only meaningful words
            filtered_student = self._filter_meaningful_words(student_answer)
            
            student_vector = self.vectorizer.transform([filtered_student])
            similarities = cosine_similarity(student_vector, self.answer_vectors)[0]
            return float(np.max(similarities))
        except:
            return 0.0
    
    def is_correct(self, student_answer: str) -> bool:
        """Check if answer meets threshold"""
        return self.match(student_answer) >= self.similarity_threshold
