"""
Simple runner for single algorithm benchmark
"""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .single_algorithm_benchmark import SingleAlgorithmBenchmark


async def quick_bubble_sort_test():
    """Quick test with bubble sort"""
    print("🧪 Quick Bubble Sort Benchmark")
    print("=" * 40)
    
    benchmark = SingleAlgorithmBenchmark()
    results = await benchmark.run_benchmark("bubble_sort", "turbo")
    benchmark.print_summary(results)
    benchmark.generate_graph(results, "bubble_sort_quick_test.png")


async def quick_fibonacci_test():
    """Quick test with fibonacci"""
    print("🧪 Quick Fibonacci Benchmark")
    print("=" * 40)
    
    benchmark = SingleAlgorithmBenchmark()
    results = await benchmark.run_benchmark("fibonacci", "turbo")
    benchmark.print_summary(results)
    benchmark.generate_graph(results, "fibonacci_quick_test.png")


async def custom_algorithm_test(algorithm_name: str, speed_mode: str = "turbo"):
    """Test specific algorithm"""
    print(f"🧪 Custom {algorithm_name.title()} Benchmark")
    print("=" * 40)
    
    benchmark = SingleAlgorithmBenchmark()
    results = await benchmark.run_benchmark(algorithm_name, speed_mode)
    benchmark.print_summary(results)
    
    graph_filename = f"{algorithm_name}_custom_test.png"
    benchmark.generate_graph(results, graph_filename)
    
    # Save results
    import json
    json_filename = f"{algorithm_name}_custom_results.json"
    with open(json_filename, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"📄 Results saved to: {json_filename}")


def main():
    """Main function with menu"""
    print("🚀 Single Algorithm Benchmark Runner")
    print("=" * 50)
    print("Choose test:")
    print("1. Quick Bubble Sort Test")
    print("2. Quick Fibonacci Test")
    print("3. Custom Algorithm Test")
    print("4. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                asyncio.run(quick_bubble_sort_test())
                break
            elif choice == "2":
                asyncio.run(quick_fibonacci_test())
                break
            elif choice == "3":
                algorithms = ["bubble_sort", "simple_math", "fibonacci", "matrix_multiply", "binary_search"]
                print(f"\nAvailable algorithms: {algorithms}")
                algorithm = input("Enter algorithm name: ").strip()
                speed_mode = input("Enter speed mode (turbo/fast/balanced, default: turbo): ").strip() or "turbo"
                asyncio.run(custom_algorithm_test(algorithm, speed_mode))
                break
            elif choice == "4":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-4.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            break


if __name__ == "__main__":
    main()

