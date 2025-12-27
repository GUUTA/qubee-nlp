#!/usr/bin/env python3
"""
Script to build and process Afaan Oromoo text corpora.
Handles corpus creation, cleaning, and preparation for NLP tasks.
"""

import os
import sys
import argparse
import json
import pickle
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Set, Tuple, Optional
from collections import Counter, defaultdict
import logging
import re

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CorpusBuilder:
    """Build and process Afaan Oromoo text corpora."""
    
    def __init__(self, corpus_dir: str = './corpus'):
        """Initialize corpus builder."""
        self.corpus_dir = Path(corpus_dir)
        self.corpus_dir.mkdir(parents=True, exist_ok=True)
        
        # Subdirectories
        self.sources_dir = self.corpus_dir / 'sources'
        self.processed_dir = self.corpus_dir / 'processed'
        self.stats_dir = self.corpus_dir / 'statistics'
        
        for directory in [self.sources_dir, self.processed_dir, self.stats_dir]:
            directory.mkdir(exist_ok=True)
        
        # Initialize NLP components
        try:
            from qubee_nlp import QubeeTokenizer, normalize_qubee
            from qubee_nlp.alphabet import validate_qubee_text
            self.tokenizer = QubeeTokenizer(preserve_case=True)
            self.normalize = normalize_qubee
            self.validate = validate_qubee_text
            self.nlp_available = True
        except ImportError:
            logger.warning("Qubee NLP not available. Some features disabled.")
            self.nlp_available = False
    
    def add_text_file(self, filepath: Path, source_name: str = None) -> Optional[Path]:
        """
        Add a text file to the corpus.
        
        Args:
            filepath: Path to text file
            source_name: Name for this source
            
        Returns:
            Path to processed file in corpus
        """
        if not filepath.exists():
            logger.error(f"File not found: {filepath}")
            return None
        
        # Generate source name if not provided
        if not source_name:
            source_name = filepath.stem
        
        # Create source directory
        source_dir = self.sources_dir / source_name
        source_dir.mkdir(exist_ok=True)
        
        # Copy/process the file
        processed_file = source_dir / f'{source_name}.txt'
        
        try:
            # Read and clean the file
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f_in:
                content = f_in.read()
            
            # Basic cleaning
            cleaned = self._clean_text(content)
            
            # Write cleaned content
            with open(processed_file, 'w', encoding='utf-8') as f_out:
                f_out.write(cleaned)
            
            logger.info(f"Added {source_name}: {len(cleaned)} characters")
            return processed_file
            
        except Exception as e:
            logger.error(f"Failed to add {filepath}: {e}")
            return None
    
    def add_directory(self, dirpath: Path, source_name: str = None) -> List[Path]:
        """
        Add all text files from a directory.
        
        Args:
            dirpath: Path to directory
            source_name: Base name for source
            
        Returns:
            List of processed file paths
        """
        if not dirpath.exists() or not dirpath.is_dir():
            logger.error(f"Directory not found: {dirpath}")
            return []
        
        if not source_name:
            source_name = dirpath.name
        
        processed_files = []
        
        # Process all text files
        for filepath in dirpath.glob('**/*.txt'):
            rel_path = filepath.relative_to(dirpath)
            source_subname = f"{source_name}_{rel_path.stem}"
            
            processed = self.add_text_file(filepath, source_subname)
            if processed:
                processed_files.append(processed)
        
        logger.info(f"Added {len(processed_files)} files from {dirpath}")
        return processed_files
    
    def create_combined_corpus(self, corpus_name: str = 'combined') -> Optional[Path]:
        """
        Create a combined corpus from all sources.
        
        Args:
            corpus_name: Name for combined corpus
            
        Returns:
            Path to combined corpus file
        """
        combined_file = self.processed_dir / f'{corpus_name}.txt'
        metadata_file = self.processed_dir / f'{corpus_name}_metadata.json'
        
        sources = []
        total_chars = 0
        total_lines = 0
        
        logger.info(f"Creating combined corpus: {corpus_name}")
        
        try:
            with open(combined_file, 'w', encoding='utf-8') as f_out:
                # Process each source
                for source_dir in self.sources_dir.iterdir():
                    if not source_dir.is_dir():
                        continue
                    
                    source_stats = {
                        'name': source_dir.name,
                        'files': [],
                        'chars': 0,
                        'lines': 0
                    }
                    
                    # Process each file in source
                    for filepath in source_dir.glob('*.txt'):
                        with open(filepath, 'r', encoding='utf-8') as f_in:
                            content = f_in.read()
                        
                        # Write to combined file
                        f_out.write(content)
                        f_out.write('\n\n')  # Separate sources
                        
                        # Update statistics
                        file_stats = {
                            'file': filepath.name,
                            'chars': len(content),
                            'lines': content.count('\n') + 1
                        }
                        source_stats['files'].append(file_stats)
                        source_stats['chars'] += len(content)
                        source_stats['lines'] += file_stats['lines']
                        total_chars += len(content)
                        total_lines += file_stats['lines']
                    
                    sources.append(source_stats)
                
                # Create metadata
                metadata = {
                    'corpus_name': corpus_name,
                    'total_sources': len(sources),
                    'total_chars': total_chars,
                    'total_lines': total_lines,
                    'sources': sources,
                    'created': str(Path.timestamp(combined_file)) if combined_file.exists() else None
                }
                
                # Save metadata
                with open(metadata_file, 'w', encoding='utf-8') as f_meta:
                    json.dump(metadata, f_meta, indent=2, ensure_ascii=False)
            
            logger.info(f"Combined corpus created: {combined_file}")
            logger.info(f"  Sources: {len(sources)}")
            logger.info(f"  Characters: {total_chars:,}")
            logger.info(f"  Lines: {total_lines:,}")
            
            return combined_file
            
        except Exception as e:
            logger.error(f"Failed to create combined corpus: {e}")
            return None
    
    def analyze_corpus(self, corpus_file: Path) -> Optional[Dict[str, Any]]:
        """
        Analyze corpus statistics.
        
        Args:
            corpus_file: Path to corpus file
            
        Returns:
            Dictionary with analysis results
        """
        if not corpus_file.exists():
            logger.error(f"Corpus file not found: {corpus_file}")
            return None
        
        if not self.nlp_available:
            logger.error("Qubee NLP required for analysis")
            return None
        
        logger.info(f"Analyzing corpus: {corpus_file}")
        
        try:
            # Read corpus
            with open(corpus_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic statistics
            chars = len(content)
            lines = content.count('\n') + 1
            words = content.split()
            
            # Tokenize and analyze
            tokens = self.tokenizer.tokenize(content)
            unique_tokens = set(tokens)
            
            # Validate text
            is_valid, invalid_chars = self.validate(content)
            
            # Character frequency
            char_freq = Counter(content.lower())
            
            # Word frequency
            word_freq = Counter(tokens)
            
            # Sentence analysis
            sentences = self.tokenizer.sentence_tokenize(content)
            sentence_lengths = [len(self.tokenizer.tokenize(s)) for s in sentences]
            
            # Create analysis results
            analysis = {
                'basic': {
                    'characters': chars,
                    'lines': lines,
                    'words': len(words),
                    'tokens': len(tokens),
                    'unique_tokens': len(unique_tokens),
                    'sentences': len(sentences),
                    'is_valid_qubee': is_valid,
                    'invalid_characters': len(invalid_chars) if invalid_chars else 0
                },
                'averages': {
                    'chars_per_word': chars / len(words) if words else 0,
                    'words_per_sentence': sum(sentence_lengths) / len(sentences) if sentences else 0,
                    'chars_per_sentence': chars / len(sentences) if sentences else 0,
                    'tokens_per_sentence': len(tokens) / len(sentences) if sentences else 0
                },
                'distributions': {
                    'sentence_length': {
                        'min': min(sentence_lengths) if sentence_lengths else 0,
                        'max': max(sentence_lengths) if sentence_lengths else 0,
                        'mean': sum(sentence_lengths) / len(sentences) if sentences else 0,
                        'median': sorted(sentence_lengths)[len(sentence_lengths)//2] if sentence_lengths else 0
                    }
                }
            }
            
            # Save detailed statistics
            stats_file = self.stats_dir / f'{corpus_file.stem}_stats.json'
            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            
            # Save frequency lists
            if word_freq:
                freq_file = self.stats_dir / f'{corpus_file.stem}_word_freq.txt'
                with open(freq_file, 'w', encoding='utf-8') as f:
                    f.write("# Word Frequency List\n")
                    f.write(f"# Total words: {len(tokens)}\n")
                    f.write(f"# Unique words: {len(unique_tokens)}\n")
                    f.write("#" * 80 + "\n")
                    
                    for word, count in word_freq.most_common():
                        percentage = (count / len(tokens)) * 100
                        f.write(f"{word}\t{count}\t{percentage:.4f}%\n")
            
            logger.info(f"Analysis complete. Results in: {stats_file}")
            return analysis
            
        except Exception as e:
            logger.error(f"Corpus analysis failed: {e}")
            return None
    
    def create_train_test_split(self, corpus_file: Path, 
                               train_ratio: float = 0.8,
                               shuffle: bool = True) -> Tuple[Optional[Path], Optional[Path]]:
        """
        Create train/test split from corpus.
        
        Args:
            corpus_file: Path to corpus file
            train_ratio: Ratio for training data (0-1)
            shuffle: Whether to shuffle before splitting
            
        Returns:
            Tuple of (train_file, test_file) paths
        """
        if not corpus_file.exists():
            logger.error(f"Corpus file not found: {corpus_file}")
            return None, None
        
        try:
            # Read corpus
            with open(corpus_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Split into sentences if needed
            if len(lines) < 100:  # Few lines, split by sentences
                content = ''.join(lines)
                if self.nlp_available:
                    sentences = self.tokenizer.sentence_tokenize(content)
                    lines = [s + '\n' for s in sentences]
            
            # Shuffle if requested
            if shuffle:
                import random
                random.shuffle(lines)
            
            # Split
            split_idx = int(len(lines) * train_ratio)
            train_lines = lines[:split_idx]
            test_lines = lines[split_idx:]
            
            # Write splits
            train_file = self.processed_dir / f'{corpus_file.stem}_train.txt'
            test_file = self.processed_dir / f'{corpus_file.stem}_test.txt'
            
            with open(train_file, 'w', encoding='utf-8') as f:
                f.writelines(train_lines)
            
            with open(test_file, 'w', encoding='utf-8') as f:
                f.writelines(test_lines)
            
            logger.info(f"Train/test split created:")
            logger.info(f"  Train: {train_file} ({len(train_lines)} lines)")
            logger.info(f"  Test: {test_file} ({len(test_lines)} lines)")
            logger.info(f"  Ratio: {train_ratio:.1%} train, {1-train_ratio:.1%} test")
            
            return train_file, test_file
            
        except Exception as e:
            logger.error(f"Train/test split failed: {e}")
            return None, None
    
    def create_vocabulary_file(self, corpus_file: Path, 
                              min_freq: int = 5,
                              max_size: int = 50000) -> Optional[Path]:
        """
        Create vocabulary file from corpus.
        
        Args:
            corpus_file: Path to corpus file
            min_freq: Minimum word frequency
            max_size: Maximum vocabulary size
            
        Returns:
            Path to vocabulary file
        """
        if not corpus_file.exists():
            logger.error(f"Corpus file not found: {corpus_file}")
            return None
        
        if not self.nlp_available:
            logger.error("Qubee NLP required for vocabulary creation")
            return None
        
        try:
            # Read corpus
            with open(corpus_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Tokenize
            tokens = self.tokenizer.tokenize(content)
            
            # Count frequencies
            word_freq = Counter(tokens)
            
            # Filter by frequency and size
            vocab_items = [(word, count) for word, count in word_freq.items() 
                          if count >= min_freq]
            vocab_items.sort(key=lambda x: x[1], reverse=True)
            
            if max_size:
                vocab_items = vocab_items[:max_size]
            
            # Create vocabulary file
            vocab_file = self.processed_dir / f'{corpus_file.stem}_vocab.txt'
            
            with open(vocab_file, 'w', encoding='utf-8') as f:
                f.write("# Vocabulary File\n")
                f.write(f"# Source: {corpus_file.name}\n")
                f.write(f"# Total tokens: {len(tokens)}\n")
                f.write(f"# Unique tokens: {len(word_freq)}\n")
                f.write(f"# Minimum frequency: {min_freq}\n")
                f.write(f"# Vocabulary size: {len(vocab_items)}\n")
                f.write("#" * 80 + "\n\n")
                
                # Write special tokens
                f.write("<PAD>\t0\n")
                f.write("<UNK>\t1\n")
                f.write("<SOS>\t2\n")
                f.write("<EOS>\t3\n\n")
                
                # Write vocabulary
                for idx, (word, count) in enumerate(vocab_items, start=4):
                    percentage = (count / len(tokens)) * 100
                    f.write(f"{word}\t{idx}\t{count}\t{percentage:.6f}%\n")
            
            logger.info(f"Vocabulary created: {vocab_file}")
            logger.info(f"  Tokens: {len(tokens):,}")
            logger.info(f"  Unique: {len(word_freq):,}")
            logger.info(f"  Vocabulary: {len(vocab_items):,}")
            
            return vocab_file
            
        except Exception as e:
            logger.error(f"Vocabulary creation failed: {e}")
            return None
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        
        # Basic cleaning
        cleaned = text
        
        # Remove excessive whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # Remove control characters (keep basic ones)
        cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', cleaned)
        
        # Normalize quotes and dashes
        cleaned = cleaned.replace('"', '"').replace("'", "'")
        cleaned = cleaned.replace('–', '-').replace('—', '-')
        
        # Remove excessive line breaks (keep paragraph breaks)
        cleaned = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned)
        
        # Trim whitespace
        cleaned = cleaned.strip()
        
        # Apply Qubee normalization if available
        if self.nlp_available:
            cleaned = self.normalize(cleaned, preserve_case=True)
        
        return cleaned
    
    def generate_corpus_report(self, corpus_file: Path) -> Optional[Path]:
        """
        Generate HTML report for corpus.
        
        Args:
            corpus_file: Path to corpus file
            
        Returns:
            Path to HTML report file
        """
        if not corpus_file.exists():
            logger.error(f"Corpus file not found: {corpus_file}")
            return None
        
        # Analyze corpus first
        analysis = self.analyze_corpus(corpus_file)
        if not analysis:
            return None
        
        # Generate HTML report
        report_file = self.stats_dir / f'{corpus_file.stem}_report.html'
        
        try:
            html_content = self._generate_html_report(corpus_file, analysis)
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Corpus report generated: {report_file}")
            return report_file
            
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            return None
    
    def _generate_html_report(self, corpus_file: Path, analysis: Dict[str, Any]) -> str:
        """Generate HTML report content."""
        
        basic = analysis['basic']
        averages = analysis['averages']
        distributions = analysis['distributions']
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Corpus Report: {corpus_file.name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
        .section {{ margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; }}
        .stat-card {{ background: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 4px solid #3498db; }}
        .stat-value {{ font-size: 24px; font-weight: bold; color: #2c3e50; }}
        .stat-label {{ color: #7f8c8d; margin-top: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #f2f2f2; }}
        .valid {{ color: #27ae60; font-weight: bold; }}
        .invalid {{ color: #e74c3c; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Corpus Analysis Report</h1>
            <p>File: {corpus_file.name}</p>
            <p>Generated: {Path.timestamp(corpus_file) if corpus_file.exists() else 'N/A'}</p>
        </div>
        
        <div class="section">
            <h2>Basic Statistics</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{basic['characters']:,}</div>
                    <div class="stat-label">Characters</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{basic['words']:,}</div>
                    <div class="stat-label">Words</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{basic['tokens']:,}</div>
                    <div class="stat-label">Tokens</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{basic['unique_tokens']:,}</div>
                    <div class="stat-label">Unique Tokens</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{basic['sentences']:,}</div>
                    <div class="stat-label">Sentences</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{basic['lines']:,}</div>
                    <div class="stat-label">Lines</div>
                </div>
            </div>
            
            <div style="margin-top: 20px;">
                <h3>Qubee Validation</h3>
                <p>
                    Status: 
                    <span class="{'valid' if basic['is_valid_qubee'] else 'invalid'}">
                        {'✓ Valid' if basic['is_valid_qubee'] else '✗ Invalid'}
                    </span>
                </p>
                {f"<p>Invalid characters: {basic['invalid_characters']}</p>" if not basic['is_valid_qubee'] else ""}
            </div>
        </div>
        
        <div class="section">
            <h2>Averages</h2>
            <table>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>Characters per word</td>
                    <td>{averages['chars_per_word']:.2f}</td>
                </tr>
                <tr>
                    <td>Words per sentence</td>
                    <td>{averages['words_per_sentence']:.2f}</td>
                </tr>
                <tr>
                    <td>Characters per sentence</td>
                    <td>{averages['chars_per_sentence']:.2f}</td>
                </tr>
                <tr>
                    <td>Tokens per sentence</td>
                    <td>{averages['tokens_per_sentence']:.2f}</td>
                </tr>
            </table>
        </div>
        
        <div class="section">
            <h2>Sentence Length Distribution</h2>
            <table>
                <tr>
                    <th>Statistic</th>
                    <th>Value (words)</th>
                </tr>
                <tr>
                    <td>Minimum</td>
                    <td>{distributions['sentence_length']['min']}</td>
                </tr>
                <tr>
                    <td>Maximum</td>
                    <td>{distributions['sentence_length']['max']}</td>
                </tr>
                <tr>
                    <td>Mean</td>
                    <td>{distributions['sentence_length']['mean']:.2f}</td>
                </tr>
                <tr>
                    <td>Median</td>
                    <td>{distributions['sentence_length']['median']}</td>
                </tr>
            </table>
        </div>
        
        <div class="section">
            <h2>Additional Information</h2>
            <p>Corpus file: <code>{corpus_file}</code></p>
            <p>Statistics directory: <code>{self.stats_dir}</code></p>
            <p>Generated with Qubee NLP Corpus Builder</p>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def cleanup(self):
        """Clean up temporary files."""
        logger.info("Cleaning up corpus builder...")
        
        # Remove empty directories
        for directory in [self.sources_dir, self.processed_dir, self.stats_dir]:
            if directory.exists():
                for item in directory.iterdir():
                    if item.is_dir() and not any(item.iterdir()):
                        item.rmdir()
                        logger.debug(f"Removed empty directory: {item}")
        
        logger.info("Cleanup complete")

def main():
    """Main function for CLI."""
    parser = argparse.ArgumentParser(
        description='Build and process Afaan Oromoo text corpora'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Add text file command
    add_file_parser = subparsers.add_parser('add-file', help='Add text file to corpus')
    add_file_parser.add_argument('file', help='Text file to add')
    add_file_parser.add_argument('--name', help='Source name (default: filename)')
    
    # Add directory command
    add_dir_parser = subparsers.add_parser('add-dir', help='Add directory of text files')
    add_dir_parser.add_argument('directory', help='Directory to add')
    add_dir_parser.add_argument('--name', help='Source name (default: directory name)')
    
    # Combine command
    combine_parser = subparsers.add_parser('combine', help='Create combined corpus')
    combine_parser.add_argument('--name', default='combined', help='Corpus name')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze corpus')
    analyze_parser.add_argument('corpus', help='Corpus file to analyze')
    
    # Split command
    split_parser = subparsers.add_parser('split', help='Create train/test split')
    split_parser.add_argument('corpus', help='Corpus file to split')
    split_parser.add_argument('--train-ratio', type=float, default=0.8,
                             help='Training ratio (default: 0.8)')
    split_parser.add_argument('--no-shuffle', action='store_true',
                             help='Do not shuffle before splitting')
    
    # Vocabulary command
    vocab_parser = subparsers.add_parser('vocab', help='Create vocabulary')
    vocab_parser.add_argument('corpus', help='Corpus file')
    vocab_parser.add_argument('--min-freq', type=int, default=5,
                             help='Minimum frequency (default: 5)')
    vocab_parser.add_argument('--max-size', type=int, default=50000,
                             help='Maximum vocabulary size (default: 50000)')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate corpus report')
    report_parser.add_argument('corpus', help='Corpus file')
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser('cleanup', help='Cleanup temporary files')
    
    parser.add_argument('--corpus-dir', default='./corpus',
                       help='Corpus directory (default: ./corpus)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize builder
    builder = CorpusBuilder(args.corpus_dir)
    
    # Execute command
    if args.command == 'add-file':
        filepath = Path(args.file)
        builder.add_text_file(filepath, args.name)
    
    elif args.command == 'add-dir':
        dirpath = Path(args.directory)
        builder.add_directory(dirpath, args.name)
    
    elif args.command == 'combine':
        builder.create_combined_corpus(args.name)
    
    elif args.command == 'analyze':
        corpus_file = Path(args.corpus)
        builder.analyze_corpus(corpus_file)
    
    elif args.command == 'split':
        corpus_file = Path(args.corpus)
        builder.create_train_test_split(
            corpus_file, 
            args.train_ratio, 
            not args.no_shuffle
        )
    
    elif args.command == 'vocab':
        corpus_file = Path(args.corpus)
        builder.create_vocabulary_file(
            corpus_file,
            args.min_freq,
            args.max_size
        )
    
    elif args.command == 'report':
        corpus_file = Path(args.corpus)
        builder.generate_corpus_report(corpus_file)
    
    elif args.command == 'cleanup':
        builder.cleanup()

if __name__ == '__main__':
    main()