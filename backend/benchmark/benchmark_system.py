"""
Benchmark System - Compare AI Agent Execution vs Normal Python Execution
"""

import asyncio
import time
import subprocess
import sys
import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Tuple
import requests
import tempfile
import os


class BenchmarkSystem:
    """
    Comprehensive benchmarking system to compare AI execution vs normal Python execution
    """
    
    def __init__(self, server_url: str = "http://localhost:8000"):
        self.server_url = server_url
        self.results = []
        self.test_algorithms = self._get_test_algorithms()
    
    def _get_test_algorithms(self) -> List[Dict[str, Any]]:
        """Get test algorithms with different complexities"""
        return [
            {
                "name": "Simple Math",
                "code": """
def simple_math(n):
    result = 0
    for i in range(n):
        result += i * 2
    return result

# Test execution
result = simple_math(1000)
print(f"Simple math result: {result}")
""",
                "complexity": "O(n)",
                "expected_time": 0.001,
                "input_sizes": [100, 500, 1000, 5000, 10000]
            },
            {
                "name": "Bubble Sort",
                "code": """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# Test execution
import random
test_array = [random.randint(1, 1000) for _ in range(100)]
sorted_array = bubble_sort(test_array)
print(f"Sorted array (first 10): {sorted_array[:10]}")
""",
                "complexity": "O(n²)",
                "expected_time": 0.01,
                "input_sizes": [50, 100, 200, 500, 1000]
            },
            {
                "name": "Fibonacci Recursive",
                "code": """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Test execution
result = fibonacci(15)
print(f"Fibonacci(15) = {result}")
""",
                "complexity": "O(2^n)",
                "expected_time": 0.1,
                "input_sizes": [10, 15, 20, 25, 30]
            },
            {
                "name": "Matrix Multiplication",
                "code": """
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
size = 50
A = [[random.randint(1, 10) for _ in range(size)] for _ in range(size)]
B = [[random.randint(1, 10) for _ in range(size)] for _ in range(size)]
result = matrix_multiply(A, B)
print(f"Matrix multiplication completed: {len(result)}x{len(result[0])}")
""",
                "complexity": "O(n³)",
                "expected_time": 0.5,
                "input_sizes": [20, 30, 40, 50, 60]
            },
            {
                "name": "Binary Search",
                "code": """
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
sorted_array = sorted([random.randint(1, 10000) for _ in range(10000)])
target = sorted_array[5000]
result = binary_search(sorted_array, target)
print(f"Found {target} at index: {result}")
""",
                "complexity": "O(log n)",
                "expected_time": 0.001,
                "input_sizes": [1000, 5000, 10000, 50000, 100000]
            }
        ]
    
    async def benchmark_ai_execution(self, code: str, algorithm_name: str, 
                                   input_size: int, speed_mode: str = "turbo") -> Dict[str, Any]:
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
                    "success": True,
                    "execution_time": end_time - start_time,
                    "ai_reasoning": result.get("ai_reasoning", ""),
                    "console_output": result.get("console_output", []),
                    "performance_grade": result.get("speed_coordinator", {}).get("performance_grade", "Unknown"),
                    "method": "AI Agent"
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "execution_time": end_time - start_time,
                    "method": "AI Agent"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "execution_time": 0.0,
                "method": "AI Agent"
            }
    
    def benchmark_normal_execution(self, code: str, algorithm_name: str, 
                                 input_size: int) -> Dict[str, Any]:
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
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "execution_time": end_time - start_time,
                    "console_output": result.stdout.strip().split('\n'),
                    "method": "Normal Python"
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr,
                    "execution_time": end_time - start_time,
                    "method": "Normal Python"
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Execution timeout (60s)",
                "execution_time": 60.0,
                "method": "Normal Python"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "execution_time": 0.0,
                "method": "Normal Python"
            }
    
    async def run_comprehensive_benchmark(self, speed_modes: List[str] = None) -> Dict[str, Any]:
        """Run comprehensive benchmark comparing all approaches"""
        if speed_modes is None:
            speed_modes = ["turbo", "fast", "balanced"]
        
        print("🚀 Starting Comprehensive Benchmark")
        print("=" * 60)
        
        all_results = []
        
        for algorithm in self.test_algorithms:
            print(f"\n🧪 Testing Algorithm: {algorithm['name']}")
            print(f"📊 Complexity: {algorithm['complexity']}")
            print("-" * 40)
            
            algorithm_results = {
                "algorithm": algorithm['name'],
                "complexity": algorithm['complexity'],
                "results": []
            }
            
            for input_size in algorithm['input_sizes']:
                print(f"  📏 Input Size: {input_size}")
                
                # Modify code for different input sizes
                modified_code = self._modify_code_for_input_size(algorithm['code'], input_size)
                
                # Test normal Python execution
                normal_result = self.benchmark_normal_execution(
                    modified_code, algorithm['name'], input_size
                )
                normal_result['input_size'] = input_size
                algorithm_results['results'].append(normal_result)
                
                # Test AI execution with different speed modes
                for speed_mode in speed_modes:
                    ai_result = await self.benchmark_ai_execution(
                        modified_code, algorithm['name'], input_size, speed_mode
                    )
                    ai_result['input_size'] = input_size
                    ai_result['speed_mode'] = speed_mode
                    algorithm_results['results'].append(ai_result)
                
                # Show progress
                if normal_result['success']:
                    print(f"    ✅ Normal: {normal_result['execution_time']:.3f}s")
                else:
                    print(f"    ❌ Normal: Failed")
                
                for speed_mode in speed_modes:
                    ai_result = next(r for r in algorithm_results['results'] 
                                   if r.get('speed_mode') == speed_mode and r['input_size'] == input_size)
                    if ai_result['success']:
                        print(f"    ⚡ AI-{speed_mode}: {ai_result['execution_time']:.3f}s")
                    else:
                        print(f"    ❌ AI-{speed_mode}: Failed")
            
            all_results.append(algorithm_results)
        
        return {
            "benchmark_timestamp": datetime.now().isoformat(),
            "total_algorithms": len(self.test_algorithms),
            "speed_modes_tested": speed_modes,
            "results": all_results
        }
    
    def _modify_code_for_input_size(self, code: str, input_size: int) -> str:
        """Modify code to use specific input size"""
        # Simple modifications for different algorithms
        if "range(1000)" in code:
            code = code.replace("range(1000)", f"range({input_size})")
        elif "range(100)" in code:
            code = code.replace("range(100)", f"range({input_size})")
        elif "range(10000)" in code:
            code = code.replace("range(10000)", f"range({input_size})")
        elif "size = 50" in code:
            code = code.replace("size = 50", f"size = {input_size}")
        elif "fibonacci(15)" in code:
            code = code.replace("fibonacci(15)", f"fibonacci({input_size})")
        
        return code
    
    def generate_performance_graphs(self, benchmark_results: Dict[str, Any], 
                                  save_path: str = "benchmark_results"):
        """Generate comprehensive performance graphs"""
        try:
            import matplotlib.pyplot as plt
            import numpy as np
            
            # Create output directory
            os.makedirs(save_path, exist_ok=True)
            
            # 1. Overall Performance Comparison
            self._plot_overall_performance(benchmark_results, save_path)
            
            # 2. Algorithm-specific Performance
            self._plot_algorithm_performance(benchmark_results, save_path)
            
            # 3. Speed Mode Comparison
            self._plot_speed_mode_comparison(benchmark_results, save_path)
            
            # 4. Complexity Analysis
            self._plot_complexity_analysis(benchmark_results, save_path)
            
            print(f"\n📊 Performance graphs saved to: {save_path}/")
            
        except ImportError:
            print("❌ matplotlib not available. Install with: pip install matplotlib")
        except Exception as e:
            print(f"❌ Error generating graphs: {str(e)}")
    
    def _plot_overall_performance(self, results: Dict[str, Any], save_path: str):
        """Plot overall performance comparison"""
        plt.figure(figsize=(12, 8))
        
        algorithms = []
        normal_times = []
        ai_turbo_times = []
        ai_fast_times = []
        ai_balanced_times = []
        
        for algorithm_result in results['results']:
            algorithm_name = algorithm_result['algorithm']
            algorithms.append(algorithm_name)
            
            # Get average times for this algorithm
            normal_results = [r for r in algorithm_result['results'] if r['method'] == 'Normal Python' and r['success']]
            ai_turbo_results = [r for r in algorithm_result['results'] if r.get('speed_mode') == 'turbo' and r['success']]
            ai_fast_results = [r for r in algorithm_result['results'] if r.get('speed_mode') == 'fast' and r['success']]
            ai_balanced_results = [r for r in algorithm_result['results'] if r.get('speed_mode') == 'balanced' and r['success']]
            
            normal_times.append(np.mean([r['execution_time'] for r in normal_results]) if normal_results else 0)
            ai_turbo_times.append(np.mean([r['execution_time'] for r in ai_turbo_results]) if ai_turbo_results else 0)
            ai_fast_times.append(np.mean([r['execution_time'] for r in ai_fast_results]) if ai_fast_results else 0)
            ai_balanced_times.append(np.mean([r['execution_time'] for r in ai_balanced_results]) if ai_balanced_results else 0)
        
        x = np.arange(len(algorithms))
        width = 0.2
        
        plt.bar(x - 1.5*width, normal_times, width, label='Normal Python', color='blue', alpha=0.7)
        plt.bar(x - 0.5*width, ai_turbo_times, width, label='AI Turbo', color='red', alpha=0.7)
        plt.bar(x + 0.5*width, ai_fast_times, width, label='AI Fast', color='orange', alpha=0.7)
        plt.bar(x + 1.5*width, ai_balanced_times, width, label='AI Balanced', color='green', alpha=0.7)
        
        plt.xlabel('Algorithms')
        plt.ylabel('Execution Time (seconds)')
        plt.title('AI Agent vs Normal Python Execution Performance')
        plt.xticks(x, algorithms, rotation=45)
        plt.legend()
        plt.yscale('log')
        plt.tight_layout()
        plt.savefig(f"{save_path}/overall_performance.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_algorithm_performance(self, results: Dict[str, Any], save_path: str):
        """Plot performance for each algorithm"""
        for algorithm_result in results['results']:
            algorithm_name = algorithm_result['algorithm']
            
            # Extract data
            input_sizes = []
            normal_times = []
            ai_turbo_times = []
            ai_fast_times = []
            ai_balanced_times = []
            
            for result in algorithm_result['results']:
                if result['input_size'] not in input_sizes:
                    input_sizes.append(result['input_size'])
            
            input_sizes.sort()
            
            for size in input_sizes:
                size_results = [r for r in algorithm_result['results'] if r['input_size'] == size]
                
                normal_result = next((r for r in size_results if r['method'] == 'Normal Python' and r['success']), None)
                ai_turbo_result = next((r for r in size_results if r.get('speed_mode') == 'turbo' and r['success']), None)
                ai_fast_result = next((r for r in size_results if r.get('speed_mode') == 'fast' and r['success']), None)
                ai_balanced_result = next((r for r in size_results if r.get('speed_mode') == 'balanced' and r['success']), None)
                
                normal_times.append(normal_result['execution_time'] if normal_result else 0)
                ai_turbo_times.append(ai_turbo_result['execution_time'] if ai_turbo_result else 0)
                ai_fast_times.append(ai_fast_result['execution_time'] if ai_fast_result else 0)
                ai_balanced_times.append(ai_balanced_result['execution_time'] if ai_balanced_result else 0)
            
            # Plot
            plt.figure(figsize=(10, 6))
            plt.plot(input_sizes, normal_times, 'b-o', label='Normal Python', linewidth=2)
            plt.plot(input_sizes, ai_turbo_times, 'r-s', label='AI Turbo', linewidth=2)
            plt.plot(input_sizes, ai_fast_times, 'orange', marker='^', label='AI Fast', linewidth=2)
            plt.plot(input_sizes, ai_balanced_times, 'g-d', label='AI Balanced', linewidth=2)
            
            plt.xlabel('Input Size')
            plt.ylabel('Execution Time (seconds)')
            plt.title(f'{algorithm_name} Performance Comparison')
            plt.legend()
            plt.yscale('log')
            plt.xscale('log')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(f"{save_path}/{algorithm_name.replace(' ', '_').lower()}_performance.png", 
                       dpi=300, bbox_inches='tight')
            plt.close()
    
    def _plot_speed_mode_comparison(self, results: Dict[str, Any], save_path: str):
        """Plot speed mode effectiveness"""
        plt.figure(figsize=(10, 6))
        
        speed_modes = ['turbo', 'fast', 'balanced']
        speedup_data = {mode: [] for mode in speed_modes}
        
        for algorithm_result in results['results']:
            for speed_mode in speed_modes:
                speedup_values = []
                
                for result in algorithm_result['results']:
                    if result.get('speed_mode') == speed_mode and result['success']:
                        # Find corresponding normal execution
                        normal_result = next((r for r in algorithm_result['results'] 
                                            if r['input_size'] == result['input_size'] 
                                            and r['method'] == 'Normal Python' and r['success']), None)
                        
                        if normal_result and result['execution_time'] > 0:
                            speedup = normal_result['execution_time'] / result['execution_time']
                            speedup_values.append(speedup)
                
                if speedup_values:
                    speedup_data[speed_mode].append(np.mean(speedup_values))
                else:
                    speedup_data[speed_mode].append(0)
        
        algorithms = [r['algorithm'] for r in results['results']]
        x = np.arange(len(algorithms))
        width = 0.25
        
        for i, mode in enumerate(speed_modes):
            plt.bar(x + i*width, speedup_data[mode], width, label=f'AI {mode.title()}', alpha=0.7)
        
        plt.xlabel('Algorithms')
        plt.ylabel('Speedup Factor (x faster)')
        plt.title('AI Speed Mode Effectiveness')
        plt.xticks(x + width, algorithms, rotation=45)
        plt.legend()
        plt.axhline(y=1, color='black', linestyle='--', alpha=0.5, label='Baseline (Normal Python)')
        plt.tight_layout()
        plt.savefig(f"{save_path}/speed_mode_comparison.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_complexity_analysis(self, results: Dict[str, Any], save_path: str):
        """Plot complexity analysis"""
        plt.figure(figsize=(12, 8))
        
        complexities = ['O(log n)', 'O(n)', 'O(n²)', 'O(n³)', 'O(2^n)']
        complexity_colors = {'O(log n)': 'green', 'O(n)': 'blue', 'O(n²)': 'orange', 
                           'O(n³)': 'red', 'O(2^n)': 'purple'}
        
        for complexity in complexities:
            complexity_results = [r for r in results['results'] if r['complexity'] == complexity]
            if not complexity_results:
                continue
            
            # Get average performance for this complexity
            avg_normal = []
            avg_ai_turbo = []
            input_sizes = []
            
            for result in complexity_results:
                normal_times = [r['execution_time'] for r in result['results'] 
                              if r['method'] == 'Normal Python' and r['success']]
                ai_turbo_times = [r['execution_time'] for r in result['results'] 
                                if r.get('speed_mode') == 'turbo' and r['success']]
                
                if normal_times and ai_turbo_times:
                    avg_normal.append(np.mean(normal_times))
                    avg_ai_turbo.append(np.mean(ai_turbo_times))
                    input_sizes.append(len(normal_times))
            
            if avg_normal and avg_ai_turbo:
                plt.scatter(avg_normal, avg_ai_turbo, 
                           label=f'{complexity}', 
                           color=complexity_colors[complexity], 
                           s=100, alpha=0.7)
        
        # Add diagonal line for reference
        max_time = max(max(avg_normal) if 'avg_normal' in locals() else [0], 
                      max(avg_ai_turbo) if 'avg_ai_turbo' in locals() else [0])
        plt.plot([0, max_time], [0, max_time], 'k--', alpha=0.5, label='Equal Performance')
        
        plt.xlabel('Normal Python Execution Time (seconds)')
        plt.ylabel('AI Agent Execution Time (seconds)')
        plt.title('Complexity Analysis: AI vs Normal Execution')
        plt.legend()
        plt.xscale('log')
        plt.yscale('log')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f"{save_path}/complexity_analysis.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    def save_benchmark_results(self, results: Dict[str, Any], filename: str = "benchmark_results.json"):
        """Save benchmark results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"📄 Benchmark results saved to: {filename}")
    
    def print_summary(self, results: Dict[str, Any]):
        """Print benchmark summary"""
        print("\n" + "="*60)
        print("📊 BENCHMARK SUMMARY")
        print("="*60)
        
        for algorithm_result in results['results']:
            algorithm_name = algorithm_result['algorithm']
            complexity = algorithm_result['complexity']
            
            print(f"\n🧪 {algorithm_name} ({complexity})")
            print("-" * 40)
            
            # Calculate averages
            normal_results = [r for r in algorithm_result['results'] if r['method'] == 'Normal Python' and r['success']]
            ai_turbo_results = [r for r in algorithm_result['results'] if r.get('speed_mode') == 'turbo' and r['success']]
            ai_fast_results = [r for r in algorithm_result['results'] if r.get('speed_mode') == 'fast' and r['success']]
            ai_balanced_results = [r for r in algorithm_result['results'] if r.get('speed_mode') == 'balanced' and r['success']]
            
            if normal_results:
                avg_normal = np.mean([r['execution_time'] for r in normal_results])
                print(f"  📊 Normal Python: {avg_normal:.3f}s (avg)")
                
                if ai_turbo_results:
                    avg_turbo = np.mean([r['execution_time'] for r in ai_turbo_results])
                    speedup_turbo = avg_normal / avg_turbo
                    print(f"  ⚡ AI Turbo: {avg_turbo:.3f}s (avg) - {speedup_turbo:.1f}x speedup")
                
                if ai_fast_results:
                    avg_fast = np.mean([r['execution_time'] for r in ai_fast_results])
                    speedup_fast = avg_normal / avg_fast
                    print(f"  🚀 AI Fast: {avg_fast:.3f}s (avg) - {speedup_fast:.1f}x speedup")
                
                if ai_balanced_results:
                    avg_balanced = np.mean([r['execution_time'] for r in ai_balanced_results])
                    speedup_balanced = avg_normal / avg_balanced
                    print(f"  ⚖️ AI Balanced: {avg_balanced:.3f}s (avg) - {speedup_balanced:.1f}x speedup")


async def main():
    """Main benchmark execution"""
    print("🚀 AI Agent vs Normal Python Benchmark System")
    print("=" * 60)
    
    # Initialize benchmark system
    benchmark = BenchmarkSystem()
    
    # Run comprehensive benchmark
    results = await benchmark.run_comprehensive_benchmark()
    
    # Print summary
    benchmark.print_summary(results)
    
    # Save results
    benchmark.save_benchmark_results(results)
    
    # Generate graphs
    benchmark.generate_performance_graphs(results)
    
    print("\n🎯 Benchmark completed successfully!")
    print("📊 Check the generated graphs and JSON file for detailed analysis.")


if __name__ == "__main__":
    asyncio.run(main())
