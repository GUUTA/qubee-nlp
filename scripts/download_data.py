
## 3. **scripts/ Directory**

### **scripts/download_data.py**
```python
#!/usr/bin/env python3
"""
Script to download and prepare data for Afaan Oromoo NLP.
Supports downloading from various sources and preparing training data.
"""

import os
import sys
import argparse
import requests
import json
import tarfile
import zipfile
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataDownloader:
    """Download and prepare data for Afaan Oromoo NLP."""
    
    # Known data sources
    DATA_SOURCES = {
        'wikipedia': {
            'url': 'https://dumps.wikimedia.org/orwiki/latest/orwiki-latest-pages-articles.xml.bz2',
            'description': 'Oromo Wikipedia dump',
            'format': 'xml.bz2',
            'size': '~100MB',
        },
        'common_crawl': {
            'url': 'https://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2023-50/segments/.../warc.paths.gz',
            'description': 'Common Crawl web data (Oromo segments)',
            'format': 'warc.gz',
            'size': 'varies',
        },
        'news': {
            'url': 'https://example.com/oromo-news-corpus.tar.gz',
            'description': 'Oromo news corpus',
            'format': 'tar.gz',
            'size': '~50MB',
        },
        'literature': {
            'url': 'https://example.com/oromo-literature.zip',
            'description': 'Oromo literature corpus',
            'format': 'zip',
            'size': '~30MB',
        },
    }
    
    def __init__(self, data_dir: str = './data'):
        """Initialize downloader with data directory."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Subdirectories
        self.raw_dir = self.data_dir / 'raw'
        self.processed_dir = self.data_dir / 'processed'
        self.models_dir = self.data_dir / 'models'
        
        for directory in [self.raw_dir, self.processed_dir, self.models_dir]:
            directory.mkdir(exist_ok=True)
    
    def list_sources(self):
        """List available data sources."""
        print("Available data sources:")
        print("-" * 80)
        for source_id, info in self.DATA_SOURCES.items():
            print(f"\n{source_id}:")
            print(f"  Description: {info['description']}")
            print(f"  Format: {info['format']}")
            print(f"  Size: {info['size']}")
            print(f"  URL: {info['url'][:60]}...")
    
    def download(self, source: str, force: bool = False) -> Optional[Path]:
        """
        Download data from a source.
        
        Args:
            source: Source identifier
            force: Force re-download even if file exists
            
        Returns:
            Path to downloaded file or None if failed
        """
        if source not in self.DATA_SOURCES:
            logger.error(f"Unknown source: {source}")
            logger.info(f"Available sources: {list(self.DATA_SOURCES.keys())}")
            return None
        
        source_info = self.DATA_SOURCES[source]
        url = source_info['url']
        filename = url.split('/')[-1]
        filepath = self.raw_dir / filename
        
        # Check if file already exists
        if filepath.exists() and not force:
            logger.info(f"File already exists: {filepath}")
            return filepath
        
        logger.info(f"Downloading {source} from {url}")
        logger.info(f"Destination: {filepath}")
        
        try:
            # Download with progress bar
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            block_size = 8192
            
            with open(filepath, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=block_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # Show progress
                        if total_size:
                            percent = (downloaded / total_size) * 100
                            sys.stdout.write(f"\rDownloaded: {downloaded}/{total_size} bytes ({percent:.1f}%)")
                            sys.stdout.flush()
            
            print()  # New line after progress
            logger.info(f"Download complete: {filepath}")
            return filepath
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Download failed: {e}")
            return None
    
    def extract(self, filepath: Path, remove_original: bool = False) -> Optional[Path]:
        """
        Extract downloaded file.
        
        Args:
            filepath: Path to compressed file
            remove_original: Remove original file after extraction
            
        Returns:
            Path to extracted directory
        """
        if not filepath.exists():
            logger.error(f"File not found: {filepath}")
            return None
        
        # Determine extraction method based on file extension
        ext = filepath.suffix.lower()
        
        # Create extraction directory
        extract_dir = self.raw_dir / filepath.stem
        extract_dir.mkdir(exist_ok=True)
        
        try:
            if ext in ['.gz', '.bz2', '.xz']:
                # Handle single compressed files
                import tarfile
                
                if ext == '.gz' and '.tar.gz' in filepath.name:
                    # tar.gz file
                    with tarfile.open(filepath, 'r:gz') as tar:
                        tar.extractall(extract_dir)
                elif ext == '.bz2' and '.tar.bz2' in filepath.name:
                    # tar.bz2 file
                    with tarfile.open(filepath, 'r:bz2') as tar:
                        tar.extractall(extract_dir)
                else:
                    # Single compressed file
                    import gzip
                    import bz2
                    
                    if ext == '.gz':
                        decompressor = gzip.open
                    elif ext == '.bz2':
                        decompressor = bz2.open
                    else:
                        logger.error(f"Unsupported compression: {ext}")
                        return None
                    
                    # Extract to single file
                    with decompressor(filepath, 'rb') as f_in:
                        content = f_in.read()
                    
                    output_file = extract_dir / filepath.stem
                    with open(output_file, 'wb') as f_out:
                        f_out.write(content)
            
            elif ext == '.zip':
                # ZIP file
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
            
            elif ext == '.tar':
                # TAR file
                with tarfile.open(filepath, 'r') as tar:
                    tar.extractall(extract_dir)
            
            else:
                logger.error(f"Unsupported file format: {ext}")
                return None
            
            logger.info(f"Extracted to: {extract_dir}")
            
            # Remove original if requested
            if remove_original:
                filepath.unlink()
                logger.info(f"Removed original file: {filepath}")
            
            return extract_dir
            
        except Exception as e:
            logger.error(f"Extraction failed: {e}")
            return None
    
    def prepare_wikipedia(self, xml_path: Path) -> Optional[Path]:
        """
        Prepare Wikipedia dump for processing.
        
        Args:
            xml_path: Path to Wikipedia XML dump
            
        Returns:
            Path to processed text file
        """
        try:
            import mwparserfromhell
            import mwxml
            from tqdm import tqdm
            
            output_file = self.processed_dir / 'wikipedia_articles.txt'
            
            logger.info(f"Processing Wikipedia dump: {xml_path}")
            logger.info(f"Output: {output_file}")
            
            # Count total pages for progress bar
            dump = mwxml.Dump.from_file(str(xml_path))
            total_pages = sum(1 for _ in dump)
            
            # Process pages
            with open(output_file, 'w', encoding='utf-8') as f_out:
                dump = mwxml.Dump.from_file(str(xml_path))
                
                for page in tqdm(dump, total=total_pages, desc="Processing"):
                    # Skip non-article pages
                    if page.namespace != 0:
                        continue
                    
                    for revision in page:
                        # Parse wikitext
                        wikicode = mwparserfromhell.parse(revision.text)
                        
                        # Extract plain text
                        text = wikicode.strip_code()
                        
                        # Clean and write
                        if text.strip():
                            # Basic cleaning
                            text = text.replace('\n', ' ').strip()
                            if text:
                                f_out.write(text + '\n')
            
            logger.info(f"Wikipedia processing complete: {output_file}")
            return output_file
            
        except ImportError:
            logger.error("Required packages not installed. Install with:")
            logger.error("pip install mwparserfromhell mwxml tqdm")
            return None
        except Exception as e:
            logger.error(f"Wikipedia processing failed: {e}")
            return None
    
    def create_sample_dataset(self, size_mb: int = 10) -> Path:
        """
        Create a sample dataset for testing.
        
        Args:
            size_mb: Size of sample dataset in MB
            
        Returns:
            Path to sample dataset
        """
        sample_text = """
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
        
        # Repeat text to reach desired size
        target_size = size_mb * 1024 * 1024  # Convert MB to bytes
        text_size = len(sample_text.encode('utf-8'))
        repetitions = target_size // text_size + 1
        
        sample_file = self.processed_dir / f'sample_dataset_{size_mb}mb.txt'
        
        logger.info(f"Creating sample dataset: {sample_file}")
        logger.info(f"Target size: {size_mb}MB, repetitions: {repetitions}")
        
        with open(sample_file, 'w', encoding='utf-8') as f:
            for i in range(repetitions):
                f.write(sample_text)
                if i % 100 == 0:
                    sys.stdout.write(f"\rProgress: {i}/{repetitions} repetitions")
                    sys.stdout.flush()
        
        print()  # New line
        actual_size = sample_file.stat().st_size / (1024 * 1024)
        logger.info(f"Sample dataset created: {actual_size:.1f}MB")
        
        return sample_file
    
    def create_vocabulary(self, text_file: Path, min_freq: int = 5) -> Optional[Path]:
        """
        Create vocabulary from text file.
        
        Args:
            text_file: Path to text file
            min_freq: Minimum frequency for words
            
        Returns:
            Path to vocabulary file
        """
        from collections import Counter
        from qubee_nlp import word_tokenize
        
        if not text_file.exists():
            logger.error(f"Text file not found: {text_file}")
            return None
        
        logger.info(f"Creating vocabulary from: {text_file}")
        
        word_counts = Counter()
        total_words = 0
        
        # Count words
        with open(text_file, 'r', encoding='utf-8') as f:
            for line in f:
                tokens = word_tokenize(line.strip())
                word_counts.update(tokens)
                total_words += len(tokens)
        
        # Filter by frequency
        vocab = {word: count for word, count in word_counts.items() 
                if count >= min_freq}
        
        # Sort by frequency
        sorted_vocab = sorted(vocab.items(), key=lambda x: x[1], reverse=True)
        
        # Write vocabulary
        vocab_file = self.processed_dir / 'vocabulary.txt'
        with open(vocab_file, 'w', encoding='utf-8') as f:
            f.write(f"# Vocabulary from {text_file.name}\n")
            f.write(f"# Total words: {total_words}\n")
            f.write(f"# Unique words: {len(word_counts)}\n")
            f.write(f"# Words with freq >= {min_freq}: {len(vocab)}\n")
            f.write("#" * 80 + "\n")
            
            for word, count in sorted_vocab:
                frequency = (count / total_words) * 100
                f.write(f"{word}\t{count}\t{frequency:.6f}%\n")
        
        logger.info(f"Vocabulary created: {vocab_file}")
        logger.info(f"Words: {total_words}, Unique: {len(word_counts)}, "
                   f"Filtered: {len(vocab)}")
        
        return vocab_file
    
    def cleanup(self, keep_processed: bool = True):
        """Clean up temporary files."""
        logger.info("Cleaning up...")
        
        # Remove raw files but keep processed
        for item in self.raw_dir.iterdir():
            if item.is_file():
                item.unlink()
                logger.debug(f"Removed: {item}")
            elif item.is_dir():
                import shutil
                shutil.rmtree(item)
                logger.debug(f"Removed directory: {item}")
        
        if not keep_processed:
            for item in self.processed_dir.iterdir():
                if item.is_file():
                    item.unlink()
        
        logger.info("Cleanup complete")

def main():
    """Main function for CLI."""
    parser = argparse.ArgumentParser(
        description='Download and prepare data for Afaan Oromoo NLP'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List available data sources')
    
    # Download command
    download_parser = subparsers.add_parser('download', help='Download data')
    download_parser.add_argument('source', help='Data source to download')
    download_parser.add_argument('--force', action='store_true', 
                                help='Force re-download')
    download_parser.add_argument('--extract', action='store_true',
                                help='Extract after download')
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract data')
    extract_parser.add_argument('file', help='File to extract')
    extract_parser.add_argument('--remove', action='store_true',
                               help='Remove original after extraction')
    
    # Prepare Wikipedia command
    wiki_parser = subparsers.add_parser('wiki', help='Prepare Wikipedia data')
    wiki_parser.add_argument('xml_file', help='Wikipedia XML dump file')
    
    # Sample dataset command
    sample_parser = subparsers.add_parser('sample', help='Create sample dataset')
    sample_parser.add_argument('--size', type=int, default=10,
                              help='Size in MB (default: 10)')
    
    # Vocabulary command
    vocab_parser = subparsers.add_parser('vocab', help='Create vocabulary')
    vocab_parser.add_argument('text_file', help='Text file to process')
    vocab_parser.add_argument('--min-freq', type=int, default=5,
                             help='Minimum frequency (default: 5)')
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser('cleanup', help='Cleanup temporary files')
    cleanup_parser.add_argument('--keep-processed', action='store_true',
                               help='Keep processed files')
    
    parser.add_argument('--data-dir', default='./data',
                       help='Data directory (default: ./data)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize downloader
    downloader = DataDownloader(args.data_dir)
    
    # Execute command
    if args.command == 'list':
        downloader.list_sources()
    
    elif args.command == 'download':
        filepath = downloader.download(args.source, args.force)
        if filepath and args.extract:
            downloader.extract(filepath)
    
    elif args.command == 'extract':
        filepath = Path(args.file)
        downloader.extract(filepath, args.remove)
    
    elif args.command == 'wiki':
        xml_path = Path(args.xml_file)
        downloader.prepare_wikipedia(xml_path)
    
    elif args.command == 'sample':
        downloader.create_sample_dataset(args.size)
    
    elif args.command == 'vocab':
        text_file = Path(args.text_file)
        downloader.create_vocabulary(text_file, args.min_freq)
    
    elif args.command == 'cleanup':
        downloader.cleanup(args.keep_processed)

if __name__ == '__main__':
    main()