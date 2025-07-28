
"""
Tests for AI rating system functionality
"""
import pytest
import json
import tempfile
import os
from pathlib import Path
from utils.ai_rating_system import AIRatingManager

class TestAIRatingSystem:
    """Test the AI rating system"""
    
    def setup_method(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_ratings_file = Path(self.temp_dir) / "test_ratings.jsonl"
        
    def teardown_method(self):
        """Clean up test environment"""
        if self.test_ratings_file.exists():
            os.remove(self.test_ratings_file)
        os.rmdir(self.temp_dir)
    
    def test_record_rating_success(self):
        """Test successful rating recording"""
        manager = AIRatingManager()
        manager.ratings_file = self.test_ratings_file
        
        success = manager.record_rating(
            question="What is the tax threshold?",
            response="The tax threshold is 183 days.",
            rating="thumbs_up",
            session_id="test_session"
        )
        
        assert success is True
        assert self.test_ratings_file.exists()
        
        # Verify rating was written correctly
        with open(self.test_ratings_file, 'r') as f:
            data = json.loads(f.read().strip())
            assert data["question"] == "What is the tax threshold?"
            assert data["rating"] == "thumbs_up"
            assert data["session_id"] == "test_session"
    
    def test_get_rating_stats(self):
        """Test rating statistics calculation"""
        manager = AIRatingManager()
        manager.ratings_file = self.test_ratings_file
        
        # Add some test ratings
        test_ratings = [
            {"question": "Q1", "response": "R1", "rating": "thumbs_up", "question_length": 10, "response_length": 20},
            {"question": "Q2", "response": "R2", "rating": "thumbs_up", "question_length": 15, "response_length": 25},
            {"question": "Q3", "response": "R3", "rating": "thumbs_down", "question_length": 20, "response_length": 30},
        ]
        
        with open(self.test_ratings_file, 'w') as f:
            for rating in test_ratings:
                f.write(json.dumps(rating) + "\n")
        
        stats = manager.get_rating_stats()
        
        assert stats["total_ratings"] == 3
        assert stats["thumbs_up"] == 2
        assert stats["thumbs_down"] == 1
        assert stats["thumbs_up_percentage"] == 66.7
        assert stats["average_question_length"] == 15  # (10+15+20)/3
        assert stats["average_response_length"] == 25  # (20+25+30)/3
    
    def test_empty_rating_stats(self):
        """Test rating stats with no data"""
        manager = AIRatingManager()
        manager.ratings_file = self.test_ratings_file
        
        stats = manager.get_rating_stats()
        
        assert stats["total_ratings"] == 0
        assert stats["thumbs_up"] == 0
        assert stats["thumbs_down"] == 0
        assert stats["thumbs_up_percentage"] == 0
