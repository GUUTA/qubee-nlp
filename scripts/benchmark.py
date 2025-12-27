#!/usr/bin/env python3
"""
Benchmark script for Qubee NLP library.
Tests performance, accuracy, and memory usage of various components.
"""

import time
import sys
import argparse
import statistics
import tracemalloc
from pathlib import Path
from typing import Dict, List, Any, Tuple
import logging
import json
import csv
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class QubeeNLPBenchmark:
    """Benchmark suite for Qubee NLP library."""
    
    def __init__(self, output_dir: str = './benchmarks'):
        """Initialize benchmark suite."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Test data
        self.test_texts = self._generate_test_texts()
        
        # Import Qubee NLP components
        try:
            from qubee_nlp import (
                QubeeTokenizer,
                word_tokenize,
                sentence_tokenize,
                validate_qubee_text,
                normalize_qubee,
                QubeeAlphabet
            )
            from qubee_nlp.stemmer import QubeeStemmer
            from qubee_nlp.pos import POSTagger
            from qubee_nlp.stopwords import get_stopwords, remove_stopwords
            
            self.QubeeTokenizer = QubeeTokenizer
            self.word_tokenize = word_tokenize
            self.sentence_tokenize = sentence_tokenize
            self.validate_qubee_text = validate_qubee_text
            self.normalize_qubee = normalize_qubee
            self.QubeeAlphabet = QubeeAlphabet
            self.QubeeStemmer = QubeeStemmer
            self.POSTagger = POSTagger
            self.get_stopwords = get_stopwords
            self.remove_stopwords = remove_stopwords
            
            self.nlp_available = True
            logger.info("Qubee NLP successfully imported")
            
        except ImportError as e:
            logger.error(f"Failed to import Qubee NLP: {e}")
            self.nlp_available = False
    
    def _generate_test_texts(self) -> Dict[str, str]:
        """Generate test texts of various sizes."""
        
        base_text = """
Afaan Oromoo afaan Kushitikii kan dubbatamu Oromiyaa fi naannawa ishee keessatti dha.
Afaanichi afaan baayyinaan dubbatamu Afriikaa keessatti, Afrikaa Kibbaa fi Kaabaati.
Qubee sirna barreeffama Afaan Oromoo sirna Laatin irratti hundaa'e dha.

Oromiyaan biyya guddaa Afriikaa keessatti argamti.
Biyyichi baayyina ummataa fi ballina lafaatiin Afriikaa keessatti lammaffaa dha.
Oromiyaan naannoo biyyoo adda addaa wajjin dhadhaabdi.

Gadaa sirna haaraa hawaasaa Oromoo dha.
Sirnichii mooraa siyaasaa, dinagdee, hawaasaa fi aadaa of keessaa qaba.
Gadaa sirna demokraatawaa kan ture yeroo dheeraaf.

Barreeffama Afaan Oromoo qabxii waggaa dheeraaf kan hin barreeffamin ture.
Hanga waggaa 1990tti, Afaan Oromoo afaan dubbatu qofa ture, afaan barreeffamaa miti.
Qubee yeroo ammaa kan fayyadamu, waggaa 1991tti fudhatame.

Barnoota Afaan Oromoo yeroo ammaa hedduu guddate.
Mana barumsaa adda addaatti Afaan Oromoo barsiisamu.
Kitaabni, gaazexeen, fi Internetiin baayyinaan Afaan Oromootiin argamu.
"""
        
        # Create texts of different sizes
        texts = {
            'tiny': base_text,  # ~1KB
            'small': base_text * 10,  # ~10KB
            'medium': base_text * 100,  # ~100KB
            'large': base_text * 1000,  # ~1MB
            'huge': base_text * 10000,  # ~10MB
        }
        
       