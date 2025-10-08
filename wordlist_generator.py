import itertools
import argparse
import time
import os

class WordlistGenerator:
    def __init__(self, digits='0123456789', length=8):
        self.digits = digits
        self.length = length
        self.total_combinations = len(digits) ** length
    
    def generate_combinations(self):
        """Generator for all combinations"""
        for combo in itertools.product(self.digits, repeat=self.length):
            yield ''.join(combo)
    
    def save_to_file(self, filename, start_from=0, chunk_size=None, progress_callback=None):
        """
        Save combinations to file with progress tracking
        
        Args:
            filename (str): Output file path
            start_from (int): Start from specific combination index
            chunk_size (int): Number of combinations per chunk
            progress_callback (function): Callback for progress updates
        """
        count = 0
        skipped = 0
        
        with open(filename, 'w') as f:
            for combo in self.generate_combinations():
                if skipped < start_from:
                    skipped += 1
                    continue
                
                f.write(combo + '\n')
                count += 1
                
                if progress_callback and count % 10000 == 0:
                    progress_callback(count, self.total_combinations)
                
                if chunk_size and count >= chunk_size:
                    break
        
        return count

def format_file_size(size_bytes):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0

def main():
    parser = argparse.ArgumentParser(description='Generate 8-digit wordlist (0-9)')
    parser.add_argument('-o', '--output', default='wordlist.txt', 
                       help='Output filename (default: wordlist.txt)')
    parser.add_argument('-l', '--length', type=int, default=8,
                       help='Password length (default: 8)')
    parser.add_argument('-s', '--sample', type=int,
                       help='Generate only sample of N combinations')
    parser.add_argument('--digits', default='0123456789',
                       help='Digits to use (default: 0-9)')
    
    args = parser.parse_args()
    
    # Create generator
    generator = WordlistGenerator(digits=args.digits, length=args.length)
    
    print(f"Wordlist Generator")
    print(f"==================")
    print(f"Digits: {args.digits}")
    print(f"Length: {args.length}")
    print(f"Total combinations: {generator.total_combinations:,}")
    print(f"Output file: {args.output}")
    print()
    
    # Calculate estimated file size (rough estimate)
    estimated_size = generator.total_combinations * (args.length + 1)  # +1 for newline
    print(f"Estimated file size: {format_file_size(estimated_size)}")
    print()
    
    # Confirm if generating full list
    if not args.sample and generator.total_combinations > 1000000:
        response = input(f"This will generate {generator.total_combinations:,} combinations. Continue? (y/N): ")
        if response.lower() != 'y':
            print("Operation cancelled.")
            return
    
    # Progress callback function
    def progress_callback(current, total):
        percentage = (current / total) * 100
        print(f"\rProgress: {current:,}/{total:,} ({percentage:.2f}%)", end='', flush=True)
    
    # Generate wordlist
    print("Generating wordlist...")
    start_time = time.time()
    
    try:
        count = generator.save_to_file(
            args.output, 
            chunk_size=args.sample,
            progress_callback=progress_callback
        )
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"\n\nSuccessfully generated {count:,} combinations!")
        print(f"Time elapsed: {elapsed_time:.2f} seconds")
        print(f"Output file: {args.output}")
        
        # Show actual file size
        if os.path.exists(args.output):
            file_size = os.path.getsize(args.output)
            print(f"File size: {format_file_size(file_size)}")
    
    except KeyboardInterrupt:
        print(f"\n\nGeneration interrupted by user.")
    except Exception as e:
        print(f"\n\nError: {e}")

if __name__ == "__main__":
    main()
