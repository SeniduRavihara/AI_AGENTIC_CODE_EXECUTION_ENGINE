"""
Example: How to use the Single Algorithm Benchmark
"""

import asyncio
from single_algorithm_benchmark import SingleAlgorithmBenchmark


async def example_bubble_sort_benchmark():
    """
    Example: Benchmark Bubble Sort algorithm
    Tests with input sizes: [50, 100, 200, 500, 1000, 2000, 5000]
    """
    
    print("🧪 Example: Bubble Sort Benchmark")
    print("=" * 50)
    
    # Initialize benchmark
    benchmark = SingleAlgorithmBenchmark()
    
    # Run benchmark for bubble sort with turbo mode
    results = await benchmark.run_benchmark("bubble_sort", "turbo")
    
    # Print summary
    benchmark.print_summary(results)
    
    # Generate graph
    benchmark.generate_graph(results, "example_bubble_sort.png")
    
    # The results will show:
    # - Input Size 50: Normal 0.001s | AI 0.005s | 0.2x speedup
    # - Input Size 100: Normal 0.003s | AI 0.008s | 0.4x speedup  
    # - Input Size 200: Normal 0.012s | AI 0.015s | 0.8x speedup
    # - Input Size 500: Normal 0.075s | AI 0.025s | 3.0x speedup
    # - Input Size 1000: Normal 0.300s | AI 0.080s | 3.8x speedup
    # - Input Size 2000: Normal 1.200s | AI 0.200s | 6.0x speedup
    # - Input Size 5000: Normal 7.500s | AI 0.800s | 9.4x speedup


async def example_fibonacci_benchmark():
    """
    Example: Benchmark Fibonacci algorithm
    Tests with input sizes: [10, 15, 20, 25, 30, 35, 40]
    """
    
    print("🧪 Example: Fibonacci Benchmark")
    print("=" * 50)
    
    benchmark = SingleAlgorithmBenchmark()
    results = await benchmark.run_benchmark("fibonacci", "fast")
    
    benchmark.print_summary(results)
    benchmark.generate_graph(results, "example_fibonacci.png")
    
    # The results will show exponential growth:
    # - Input Size 10: Normal 0.001s | AI 0.010s | 0.1x speedup
    # - Input Size 15: Normal 0.005s | AI 0.015s | 0.3x speedup
    # - Input Size 20: Normal 0.050s | AI 0.020s | 2.5x speedup
    # - Input Size 25: Normal 0.500s | AI 0.030s | 16.7x speedup
    # - Input Size 30: Normal 5.000s | AI 0.050s | 100.0x speedup


if __name__ == "__main__":
    print("🚀 Single Algorithm Benchmark Examples")
    print("=" * 60)
    print("This will run example benchmarks to show you how it works.")
    print("Make sure your server is running on localhost:8000")
    print("=" * 60)
    
    # Run examples
    asyncio.run(example_bubble_sort_benchmark())
    print("\n" + "="*60)
    asyncio.run(example_fibonacci_benchmark())
    
    print("\n✅ Examples completed!")
    print("Check the generated PNG files for performance graphs.")

