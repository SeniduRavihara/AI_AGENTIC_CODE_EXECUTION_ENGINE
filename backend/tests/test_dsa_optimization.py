"""
Test script for DSA Optimization with Dynamic Agent Factory
"""

import requests
import json
import time

# Test DSA problems with different optimization levels
def test_dsa_optimization():
    
    print("🧠 Testing DSA Optimization System")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    # Test 1: Large Sorting Problem
    sorting_code = """
# Large-scale sorting problem
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Large dataset
import random
large_array = [random.randint(1, 100000) for _ in range(50000)]
print(f"Sorting array of size: {len(large_array)}")

sorted_array = merge_sort(large_array)
print(f"First 10 elements: {sorted_array[:10]}")
print(f"Last 10 elements: {sorted_array[-10:]}")
"""
    
    # Test 2: Graph Problem
    graph_code = """
# Graph traversal - DFS with large graph
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    path = []
    
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            path.append(vertex)
            # Add neighbors to stack
            for neighbor in graph.get(vertex, []):
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return path

# Large graph (10000 nodes)
graph = {}
for i in range(10000):
    graph[i] = [j for j in range(max(0, i-5), min(10000, i+6)) if j != i]

print(f"Graph has {len(graph)} nodes")
result = dfs_iterative(graph, 0)
print(f"DFS traversed {len(result)} nodes")
print(f"First 20 nodes: {result[:20]}")
"""
    
    # Test 3: Dynamic Programming Problem
    dp_code = """
# Large-scale DP problem - Fibonacci with memoization
def fibonacci_dp(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 2:
        return 1
    memo[n] = fibonacci_dp(n-1, memo) + fibonacci_dp(n-2, memo)
    return memo[n]

# Calculate large Fibonacci numbers
large_n = 1000
print(f"Calculating Fibonacci({large_n})")
result = fibonacci_dp(large_n)
print(f"Fibonacci({large_n}) = {str(result)[:50]}...")
print(f"Result length: {len(str(result))} digits")
"""
    
    test_cases = [
        {
            "name": "Large Sorting Problem",
            "code": sorting_code,
            "problem_type": "sorting",
            "optimization_levels": ["sequential", "auto", "parallel", "aggressive"]
        },
        {
            "name": "Graph Traversal Problem", 
            "code": graph_code,
            "problem_type": "graph",
            "optimization_levels": ["auto", "parallel"]
        },
        {
            "name": "Dynamic Programming Problem",
            "code": dp_code,
            "problem_type": "dp", 
            "optimization_levels": ["auto", "aggressive"]
        }
    ]
    
    for test_case in test_cases:
        print(f"\n🧪 Testing: {test_case['name']}")
        print("-" * 40)
        
        for opt_level in test_case['optimization_levels']:
            print(f"\n⚙️ Optimization Level: {opt_level}")
            
            payload = {
                "code": test_case['code'],
                "language": "python",
                "problem_type": test_case['problem_type'],
                "optimization_level": opt_level,
                "input_data": list(range(1000)) if test_case['problem_type'] == 'sorting' else None
            }
            
            try:
                start_time = time.time()
                response = requests.post(f"{base_url}/execute-dsa", json=payload, timeout=60)
                end_time = time.time()
                
                if response.status_code == 200:
                    result = response.json()
                    
                    print(f"✅ Success!")
                    print(f"📊 Total Time: {end_time - start_time:.2f}s")
                    print(f"🤖 Execution Method: {result.get('execution_method', 'Unknown')}")
                    
                    if 'dsa_coordinator' in result:
                        coord = result['dsa_coordinator']
                        print(f"🧠 Orchestrator Used: {coord.get('orchestrator_used', False)}")
                        print(f"🎯 Approach: {coord.get('execution_approach', {}).get('reason', 'N/A')}")
                        print(f"📈 Agents Created: {coord.get('agents_created', 0)}")
                    
                    if 'performance_metrics' in result:
                        perf = result['performance_metrics']
                        print(f"⚡ Estimated Speedup: {perf.get('estimated_speedup', 1.0):.1f}x")
                        print(f"🔧 Memory Efficiency: {perf.get('memory_efficiency', 'standard')}")
                    
                else:
                    print(f"❌ Error: {response.status_code}")
                    print(f"Details: {response.text}")
                    
            except requests.exceptions.Timeout:
                print(f"⏰ Timeout after 60 seconds")
            except Exception as e:
                print(f"❌ Error: {str(e)}")
    
    print(f"\n🎯 DSA Optimization Testing Complete!")
    print("=" * 60)

def test_agent_factory_scaling():
    """Test agent factory scaling with multiple concurrent requests"""
    
    print("\n🏭 Testing Agent Factory Scaling")
    print("-" * 40)
    
    base_url = "http://localhost:8000"
    
    # Simple sorting code for concurrent testing
    simple_code = """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

test_array = [64, 34, 25, 12, 22, 11, 90]
result = bubble_sort(test_array.copy())
print(f"Sorted: {result}")
"""
    
    import concurrent.futures
    import threading
    
    def make_request(request_id):
        payload = {
            "code": simple_code,
            "language": "python", 
            "problem_type": "sorting",
            "optimization_level": "parallel"
        }
        
        try:
            start = time.time()
            response = requests.post(f"{base_url}/execute-dsa", json=payload, timeout=30)
            end = time.time()
            
            if response.status_code == 200:
                result = response.json()
                agents_created = result.get('dsa_coordinator', {}).get('agents_created', 0)
                return {
                    "request_id": request_id,
                    "success": True,
                    "time": end - start,
                    "agents_created": agents_created
                }
            else:
                return {"request_id": request_id, "success": False, "error": response.text}
                
        except Exception as e:
            return {"request_id": request_id, "success": False, "error": str(e)}
    
    # Make 5 concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_request, i) for i in range(5)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    successful = [r for r in results if r.get('success', False)]
    
    print(f"📊 Concurrent Requests: 5")
    print(f"✅ Successful: {len(successful)}")
    print(f"⏱️ Average Time: {sum(r['time'] for r in successful) / len(successful):.2f}s")
    print(f"🤖 Total Agents Created: {sum(r['agents_created'] for r in successful)}")

if __name__ == "__main__":
    try:
        # Test basic health first
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("🟢 Server is healthy")
            test_dsa_optimization()
            test_agent_factory_scaling()
        else:
            print("🔴 Server health check failed")
            
    except requests.exceptions.ConnectionError:
        print("🔴 Cannot connect to server. Please start the backend server first:")
        print("   cd backend && python run_server.py")
    except Exception as e:
        print(f"🔴 Test failed: {str(e)}")
