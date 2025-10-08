I'll help you create a Python tool to generate an 8-digit wordlist using digits 0-9. Here are a few different approaches:

## Method 1: Simple Generator (Memory Efficient)

```python
import itertools

def generate_8_digit_wordlist():
    """Generate all possible 8-digit combinations (0-9)"""
    digits = '0123456789'
    
    # Using itertools.product for efficient generation
    for combination in itertools.product(digits, repeat=8):
        yield ''.join(combination)

# Usage example
def save_wordlist(filename="wordlist.txt", max_combinations=None):
    """
    Save generated combinations to a file
    
    Args:
        filename (str): Output filename
        max_combinations (int): Limit number of combinations (for testing)
    """
    count = 0
    with open(filename, 'w') as f:
        for combo in generate_8_digit_wordlist():
            f.write(combo + '\n')
            count += 1
            if max_combinations and count >= max_combinations:
                break
    
    print(f"Generated {count} combinations in {filename}")

# Test with a small sample
if __name__ == "__main__":
    # Generate first 100 combinations for testing
    save_wordlist("sample_wordlist.txt", max_combinations=100)
    print("Sample generated successfully!")
```

## Method 2: Complete Tool with Options

```python
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
```

## Method 3: Simple One-liner for Quick Generation

```python
# Quick and simple version for small samples
import itertools

def quick_generate(output_file="quick_wordlist.txt", count=1000):
    """Quickly generate a sample wordlist"""
    with open(output_file, 'w') as f:
        for i, combo in enumerate(itertools.product('0123456789', repeat=8)):
            if i >= count:
                break
            f.write(''.join(combo) + '\n')
    print(f"Generated {count} combinations in {output_file}")

# Usage
quick_generate("my_wordlist.txt", 10000)
```

## Usage Examples:

1. **Command Line Usage:**
```bash
# Generate full wordlist
python wordlist_generator.py

# Generate sample of 1000 combinations
python wordlist_generator.py --sample 1000

# Custom output file
python wordlist_generator.py -o my_passwords.txt

# Different length
python wordlist_generator.py -l 6
```

2. **Programmatic Usage:**
```python
# Use the generator directly
generator = WordlistGenerator()
for password in generator.generate_combinations():
    print(password)
    # Process each password
```

## Important Notes:

- **Total Combinations**: 8 digits with 10 possibilities each = 100,000,000 (100 million) combinations
- **File Size**: Approximately 900MB for the complete list
- **Memory Efficient**: The generator approach doesn't store all combinations in memory
- **Time**: Generating the complete list may take several minutes depending on your system

## Features:

- ✅ Memory-efficient generation
- ✅ Progress tracking
- ✅ Customizable length and digits
- ✅ Sample generation for testing
- ✅ File size estimation
- ✅ Resume capability
- ✅ Command-line interface

Choose the method that best fits your needs. Method 2 is the most feature-complete for production use, while Method 1 is simpler for basic requirements.
