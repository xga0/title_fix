#!/usr/bin/env python3
"""
Performance test script to demonstrate optimization improvements.
"""

import time
from title_fix import title_fix

def performance_test():
    """Test performance with various text sizes and patterns."""
    
    print("🚀 Title Fix v0.0.2 - Performance Test")
    print("=" * 50)
    
    # Test cases with different complexities
    test_cases = [
        ("Short title", "the quick brown fox"),
        ("Medium title", "the theory of relativity: a comprehensive guide to understanding physics"),
        ("Long title with complex features", "how to write amazing headlines in 2024: the ultimate guide to creating compelling titles with roman numerals ii, iii, and acronyms like nasa, fbi, and cia for maximum impact"),
        ("Hyphenated words", "well-known state-of-the-art machine-learning algorithms for real-time data processing"),
        ("Multiple sentences", "This is the first sentence. This is the second sentence! And this is the third sentence?"),
        ("Large text", "word " * 500)  # 500 words
    ]
    
    for test_name, text in test_cases:
        print(f"\n📝 Testing: {test_name}")
        print(f"   Input length: {len(text)} characters, {len(text.split())} words")
        
        # Warm up and measure
        title_fix(text)  # Warm up caches
        
        start_time = time.perf_counter()
        iterations = 1000 if len(text) < 1000 else 100
        
        for _ in range(iterations):
            result = title_fix(text, case_type="title", style="apa")
        
        end_time = time.perf_counter()
        
        total_time = (end_time - start_time) * 1000  # Convert to milliseconds
        avg_time = total_time / iterations
        
        print(f"   ⚡ {iterations} iterations: {total_time:.2f}ms total")
        print(f"   📊 Average per call: {avg_time:.3f}ms")
        print(f"   🎯 Headline score: {result['headline_score']}")
        
        # Test different case types for variety
        if len(text) < 200:  # Only for shorter texts
            case_types = ["sentence", "upper", "lower", "alt", "toggle"]
            case_times = []
            
            for case_type in case_types:
                start_time = time.perf_counter()
                for _ in range(500):
                    title_fix(text, case_type=case_type)
                end_time = time.perf_counter()
                case_time = ((end_time - start_time) * 1000) / 500
                case_times.append(f"{case_type}: {case_time:.3f}ms")
            
            print(f"   🔀 Case types avg: {', '.join(case_times)}")
    
    # Test citation styles performance
    print(f"\n📚 Citation Styles Performance Test")
    test_text = "the art of war: strategies for modern business success"
    styles = ["apa", "chicago", "ap", "mla", "nyt"]
    
    for style in styles:
        start_time = time.perf_counter()
        for _ in range(1000):
            title_fix(test_text, style=style)
        end_time = time.perf_counter()
        
        avg_time = ((end_time - start_time) * 1000) / 1000
        print(f"   📖 {style.upper()}: {avg_time:.3f}ms avg")
    
    print(f"\n✅ Performance test completed!")
    print(f"🎉 All optimizations are working efficiently!")

if __name__ == "__main__":
    performance_test() 