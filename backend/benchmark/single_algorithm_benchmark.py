"""
Single Algorithm Benchmark - Measure execution time vs input size
Compare AI Agent vs Normal Python execution for one algorithm
"""

import asyncio
import time
import subprocess
import sys
import tempfile
import os
import requests
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Any


class SingleAlgorithmBenchmark:
    """
    Focused benchmark for one algorithm with varying input sizes
    """
    
    def __init__(self, server_url: str = "http://localhost:8000"):
        self.server_url = server_url
        self.results = []
    
    def get_algorithm_template(self, algorithm_name: str) -> Dict[str, Any]:
        """Get algorithm template with placeholder for input size"""
        
        algorithms = {
            "bubble_sort": {
                "name": "Bubble Sort",
                "complexity": "O(n²)",
                "template": """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# Test execution
import random
test_array = [random.randint(1, 1000) for _ in range({input_size})]
sorted_array = bubble_sort(test_array)
print(f"Sorted array size: {len(sorted_array)}")
print(f"First 5 elements: {sorted_array[:5]}")
""",
                "input_sizes": [50, 100, 200, 500, 1000, 2000, 5000]
            },
            
            "simple_math": {
                "name": "Simple Math",
                "complexity": "O(n)",
                "template": """
def simple_math(n):
    result = 0
    for i in range(n):
        result += i * 2
    return result

# Test execution
result = simple_math({input_size})
print(f"Result for n={input_size}: {result}")
""",
                "input_sizes": [1000, 5000, 10000, 50000, 100000, 500000, 1000000]
            },
            
            "fibonacci": {
                "name": "Fibonacci Recursive",
                "complexity": "O(2^n)",
                "template": """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Test execution
result = fibonacci({input_size})
print(f"Fibonacci({input_size}) = {result}")
""",
                "input_sizes": [10, 15, 20, 25, 30, 35, 40]
            },
            
            "matrix_multiply": {
                "name": "Matrix Multiplication",
                "complexity": "O(n³)",
                "template": """
def matrix_multiply(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    
    if cols_A != rows_B:
        raise ValueError("Cannot multiply matrices")
    
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    
    return result

# Test execution
import random
size = {input_size}
A = [[random.randint(1, 10) for _ in range(size)] for _ in range(size)]
B = [[random.randint(1, 10) for _ in range(size)] for _ in range(size)]
result = matrix_multiply(A, B)
print(f"Matrix multiplication completed: {len(result)}x{len(result[0])}")
""",
                "input_sizes": [20, 30, 40, 50, 60, 70, 80]
            },
            
            "binary_search": {
                "name": "Binary Search",
                "complexity": "O(log n)",
                "template": """
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Test execution
import random
sorted_array = sorted([random.randint(1, 100000) for _ in range({input_size})])
target = sorted_array[{input_size}//2]  # Search for middle element
result = binary_search(sorted_array, target)
print(f"Found {target} at index: {result}")
""",
                "input_sizes": [1000, 5000, 10000, 50000, 100000, 500000, 1000000]
            }
        }
        
        return algorithms.get(algorithm_name, algorithms["bubble_sort"])
    
    def benchmark_normal_execution(self, code: str, input_size: int) -> Dict[str, Any]:
        """Benchmark normal Python execution"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            # Execute with Python
            start_time = time.time()
            result = subprocess.run([sys.executable, temp_file], 
                                  capture_output=True, text=True, timeout=60)
            end_time = time.time()
            
            # Clean up
            os.unlink(temp_file)
            
            return {
                "success": result.returncode == 0,
                "execution_time": end_time - start_time,
                "output": result.stdout.strip(),
                "error": result.stderr.strip() if result.stderr else None,
                "method": "Normal Python"
            }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "execution_time": 60.0,
                "error": "Execution timeout (60s)",
                "method": "Normal Python"
            }
        except Exception as e:
            return {
                "success": False,
                "execution_time": 0.0,
                "error": str(e),
                "method": "Normal Python"
            }
    
    async def benchmark_ai_execution(self, code: str, input_size: int, speed_mode: str = "turbo") -> Dict[str, Any]:
        """Benchmark AI agent execution"""
        try:
            payload = {
                "code": code,
                "language": "python",
                "problem_type": "general",
                "speed_mode": speed_mode
            }
            
            start_time = time.time()
            response = requests.post(f"{self.server_url}/execute-speed", json=payload, timeout=60)
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": result.get("success", False),
                    "execution_time": end_time - start_time,
                    "output": result.get("console_output", []),
                    "performance_grade": result.get("speed_coordinator", {}).get("performance_grade", "Unknown"),
                    "method": f"AI Agent ({speed_mode})"
                }
            else:
                return {
                    "success": False,
                    "execution_time": end_time - start_time,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "method": f"AI Agent ({speed_mode})"
                }
                
        except Exception as e:
            return {
                "success": False,
                "execution_time": 0.0,
                "error": str(e),
                "method": f"AI Agent ({speed_mode})"
            }
    
    async def run_benchmark(self, algorithm_name: str, speed_mode: str = "turbo") -> Dict[str, Any]:
        """Run benchmark for one algorithm with varying input sizes"""
        
        print(f"🧪 Single Algorithm Benchmark: {algorithm_name.upper()}")
        print("=" * 60)
        
        # Get algorithm template
        algorithm = self.get_algorithm_template(algorithm_name)
        print(f"📊 Algorithm: {algorithm['name']}")
        print(f"🔢 Complexity: {algorithm['complexity']}")
        print(f"⚡ Speed Mode: {speed_mode}")
        print(f"📏 Input Sizes: {algorithm['input_sizes']}")
        print("-" * 60)
        
        results = {
            "algorithm": algorithm['name'],
            "complexity": algorithm['complexity'],
            "speed_mode": speed_mode,
            "input_sizes": [],
            "normal_times": [],
            "ai_times": [],
            "speedups": [],
            "detailed_results": []
        }
        
        for input_size in algorithm['input_sizes']:
            print(f"\n📏 Testing Input Size: {input_size}")
            
            # Generate code for this input size
            code = algorithm['template'].format(input_size=input_size)
            
            # Test normal Python execution
            print("  🔄 Testing Normal Python...")
            normal_result = self.benchmark_normal_execution(code, input_size)
            
            # Test AI agent execution
            print("  🤖 Testing AI Agent...")
            ai_result = await self.benchmark_ai_execution(code, input_size, speed_mode)
            
            # Store results
            if normal_result['success'] and ai_result['success']:
                normal_time = normal_result['execution_time']
                ai_time = ai_result['execution_time']
                speedup = normal_time / ai_time if ai_time > 0 else 0
                
                results['input_sizes'].append(input_size)
                results['normal_times'].append(normal_time)
                results['ai_times'].append(ai_time)
                results['speedups'].append(speedup)
                
                print(f"    ✅ Normal Python: {normal_time:.3f}s")
                print(f"    ⚡ AI Agent: {ai_time:.3f}s")
                print(f"    🚀 Speedup: {speedup:.1f}x")
                
                results['detailed_results'].append({
                    "input_size": input_size,
                    "normal_time": normal_time,
                    "ai_time": ai_time,
                    "speedup": speedup,
                    "normal_output": normal_result['output'],
                    "ai_output": ai_result['output']
                })
            else:
                print(f"    ❌ Normal Python: {'Failed' if not normal_result['success'] else 'Success'}")
                print(f"    ❌ AI Agent: {'Failed' if not ai_result['success'] else 'Success'}")
                if not normal_result['success']:
                    print(f"      Error: {normal_result.get('error', 'Unknown')}")
                if not ai_result['success']:
                    print(f"      Error: {ai_result.get('error', 'Unknown')}")
        
        return results
    
    def generate_graph(self, results: Dict[str, Any], save_path: str = "single_algorithm_benchmark.png"):
        """Generate performance graph"""
        try:
            plt.figure(figsize=(12, 8))
            
            input_sizes = results['input_sizes']
            normal_times = results['normal_times']
            ai_times = results['ai_times']
            
            # Plot both lines
            plt.plot(input_sizes, normal_times, 'b-o', label='Normal Python', linewidth=2, markersize=6)
            plt.plot(input_sizes, ai_times, 'r-s', label=f'AI Agent ({results["speed_mode"]})', linewidth=2, markersize=6)
            
            # Customize plot
            plt.xlabel('Input Size', fontsize=12)
            plt.ylabel('Execution Time (seconds)', fontsize=12)
            plt.title(f'{results["algorithm"]} Performance Comparison\nComplexity: {results["complexity"]}', fontsize=14)
            plt.legend(fontsize=12)
            plt.grid(True, alpha=0.3)
            
            # Use log scale for better visualization
            plt.yscale('log')
            if max(input_sizes) / min(input_sizes) > 10:
                plt.xscale('log')
            
            # Add speedup annotations
            for i, (size, normal, ai, speedup) in enumerate(zip(input_sizes, normal_times, ai_times, results['speedups'])):
                if speedup > 1:
                    plt.annotate(f'{speedup:.1f}x', 
                               xy=(size, ai), 
                               xytext=(5, 5), 
                               textcoords='offset points',
                               fontsize=8,
                               color='green' if speedup > 2 else 'orange')
            
            plt.tight_layout()
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"\n📊 Graph saved to: {save_path}")
            
        except ImportError:
            print("❌ matplotlib not available. Install with: pip install matplotlib")
        except Exception as e:
            print(f"❌ Error generating graph: {str(e)}")
    
    def print_summary(self, results: Dict[str, Any]):
        """Print benchmark summary"""
        print("\n" + "=" * 60)
        print("📊 BENCHMARK SUMMARY")
        print("=" * 60)
        print(f"Algorithm: {results['algorithm']}")
        print(f"Complexity: {results['complexity']}")
        print(f"Speed Mode: {results['speed_mode']}")
        print(f"Successful Tests: {len(results['input_sizes'])}/{len(results['input_sizes'])}")
        
        if results['speedups']:
            avg_speedup = np.mean(results['speedups'])
            max_speedup = max(results['speedups'])
            min_speedup = min(results['speedups'])
            
            print(f"\n🚀 Speedup Statistics:")
            print(f"  Average Speedup: {avg_speedup:.1f}x")
            print(f"  Maximum Speedup: {max_speedup:.1f}x")
            print(f"  Minimum Speedup: {min_speedup:.1f}x")
            
            print(f"\n📈 Performance by Input Size:")
            for i, (size, normal, ai, speedup) in enumerate(zip(results['input_sizes'], results['normal_times'], results['ai_times'], results['speedups'])):
                print(f"  Size {size:>6}: Normal {normal:>6.3f}s | AI {ai:>6.3f}s | {speedup:>4.1f}x speedup")
        
        print("\n✅ Benchmark completed!")


async def main():
    """Main function"""
    print("🚀 Single Algorithm Benchmark System")
    print("=" * 50)
    
    # Available algorithms
    algorithms = ["bubble_sort", "simple_math", "fibonacci", "matrix_multiply", "binary_search"]
    
    print("Available algorithms:")
    for i, alg in enumerate(algorithms, 1):
        print(f"  {i}. {alg}")
    
    # Get user choice
    while True:
        try:
            choice = input(f"\nSelect algorithm (1-{len(algorithms)}): ").strip()
            choice_idx = int(choice) - 1
            
            if 0 <= choice_idx < len(algorithms):
                algorithm_name = algorithms[choice_idx]
                break
            else:
                print("❌ Invalid choice. Please try again.")
        except ValueError:
            print("❌ Please enter a number.")
    
    # Get speed mode
    speed_modes = ["turbo", "fast", "balanced"]
    print(f"\nAvailable speed modes: {speed_modes}")
    
    while True:
        speed_mode = input("Select speed mode (default: turbo): ").strip().lower()
        if not speed_mode:
            speed_mode = "turbo"
            break
        elif speed_mode in speed_modes:
            break
        else:
            print("❌ Invalid speed mode. Please try again.")
    
    # Run benchmark
    benchmark = SingleAlgorithmBenchmark()
    results = await benchmark.run_benchmark(algorithm_name, speed_mode)
    
    # Print summary
    benchmark.print_summary(results)
    
    # Generate graph
    graph_filename = f"{algorithm_name}_benchmark.png"
    benchmark.generate_graph(results, graph_filename)
    
    # Save results to JSON
    import json
    json_filename = f"{algorithm_name}_results.json"
    with open(json_filename, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"📄 Results saved to: {json_filename}")


if __name__ == "__main__":
    asyncio.run(main())

