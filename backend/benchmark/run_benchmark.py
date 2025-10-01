"""
Simple Benchmark Runner - Easy way to run performance comparisons
"""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .benchmark_system import BenchmarkSystem


async def quick_benchmark():
    """Run a quick benchmark with essential algorithms"""
    print("⚡ Quick Benchmark - Essential Algorithms Only")
    print("=" * 50)
    
    benchmark = BenchmarkSystem()
    
    # Test with just turbo mode for speed
    results = await benchmark.run_comprehensive_benchmark(speed_modes=["turbo"])
    
    # Print summary
    benchmark.print_summary(results)
    
    # Save results
    benchmark.save_benchmark_results(results, "quick_benchmark_results.json")
    
    # Generate graphs
    benchmark.generate_performance_graphs(results, "quick_benchmark_graphs")
    
    print("\n✅ Quick benchmark completed!")


async def full_benchmark():
    """Run full benchmark with all speed modes"""
    print("🚀 Full Benchmark - All Speed Modes")
    print("=" * 50)
    
    benchmark = BenchmarkSystem()
    
    # Test all speed modes
    results = await benchmark.run_comprehensive_benchmark(speed_modes=["turbo", "fast", "balanced"])
    
    # Print summary
    benchmark.print_summary(results)
    
    # Save results
    benchmark.save_benchmark_results(results, "full_benchmark_results.json")
    
    # Generate graphs
    benchmark.generate_performance_graphs(results, "full_benchmark_graphs")
    
    print("\n✅ Full benchmark completed!")


async def custom_benchmark():
    """Run custom benchmark with user-selected algorithms"""
    print("🎯 Custom Benchmark")
    print("=" * 50)
    
    benchmark = BenchmarkSystem()
    
    # Show available algorithms
    print("Available algorithms:")
    for i, alg in enumerate(benchmark.test_algorithms):
        print(f"  {i+1}. {alg['name']} ({alg['complexity']})")
    
    # For demo, let's test just sorting and fibonacci
    selected_algorithms = [benchmark.test_algorithms[1], benchmark.test_algorithms[2]]  # Bubble Sort and Fibonacci
    
    # Create custom results structure
    custom_results = {
        "benchmark_timestamp": "custom",
        "total_algorithms": len(selected_algorithms),
        "speed_modes_tested": ["turbo"],
        "results": []
    }
    
    for algorithm in selected_algorithms:
        print(f"\n🧪 Testing: {algorithm['name']}")
        
        algorithm_results = {
            "algorithm": algorithm['name'],
            "complexity": algorithm['complexity'],
            "results": []
        }
        
        # Test with smaller input sizes for demo
        test_sizes = algorithm['input_sizes'][:3]  # First 3 sizes only
        
        for input_size in test_sizes:
            print(f"  📏 Input Size: {input_size}")
            
            modified_code = benchmark._modify_code_for_input_size(algorithm['code'], input_size)
            
            # Test normal execution
            normal_result = benchmark.benchmark_normal_execution(modified_code, algorithm['name'], input_size)
            normal_result['input_size'] = input_size
            algorithm_results['results'].append(normal_result)
            
            # Test AI execution
            ai_result = await benchmark.benchmark_ai_execution(modified_code, algorithm['name'], input_size, "turbo")
            ai_result['input_size'] = input_size
            ai_result['speed_mode'] = "turbo"
            algorithm_results['results'].append(ai_result)
            
            print(f"    ✅ Normal: {normal_result['execution_time']:.3f}s")
            if ai_result['success']:
                print(f"    ⚡ AI-Turbo: {ai_result['execution_time']:.3f}s")
            else:
                print(f"    ❌ AI-Turbo: Failed")
        
        custom_results['results'].append(algorithm_results)
    
    # Print summary
    benchmark.print_summary(custom_results)
    
    # Save results
    benchmark.save_benchmark_results(custom_results, "custom_benchmark_results.json")
    
    # Generate graphs
    benchmark.generate_performance_graphs(custom_results, "custom_benchmark_graphs")
    
    print("\n✅ Custom benchmark completed!")


def main():
    """Main function with menu"""
    print("🚀 AI Agent Performance Benchmark System")
    print("=" * 50)
    print("Choose benchmark type:")
    print("1. Quick Benchmark (Turbo mode only)")
    print("2. Full Benchmark (All speed modes)")
    print("3. Custom Benchmark (Selected algorithms)")
    print("4. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                asyncio.run(quick_benchmark())
                break
            elif choice == "2":
                asyncio.run(full_benchmark())
                break
            elif choice == "3":
                asyncio.run(custom_benchmark())
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
