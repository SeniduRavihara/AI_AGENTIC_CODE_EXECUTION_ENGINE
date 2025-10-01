# Benchmark System

Comprehensive performance comparison between AI agents and normal Python execution.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r benchmark_requirements.txt
```

### 2. Make Sure Server is Running
```bash
cd ..  # Go back to backend directory
python run_server.py
```

### 3. Run Benchmark
```bash
# Quick test
python test_benchmark.py

# Full benchmark system
python run_benchmark.py

# Direct benchmark
python benchmark_system.py
```

## 📊 What You Get

### Performance Graphs
- **Overall Performance Comparison** - Bar chart comparing all methods
- **Algorithm-Specific Performance** - Line charts for each algorithm
- **Speed Mode Comparison** - Speedup factors for different AI modes
- **Complexity Analysis** - Scatter plot of complexity vs performance

### Test Algorithms
1. **Simple Math** (O(n)) - Basic arithmetic operations
2. **Bubble Sort** (O(n²)) - Sorting algorithm
3. **Fibonacci Recursive** (O(2^n)) - Recursive algorithm
4. **Matrix Multiplication** (O(n³)) - Nested loops
5. **Binary Search** (O(log n)) - Search algorithm

### Speed Modes
- **Turbo** - Maximum speed, minimal AI (< 2s target)
- **Fast** - Balanced speed with selective AI (< 5s target)
- **Balanced** - Adapts based on complexity (< 8s target)

## 📈 Expected Results

Based on the 49-second baseline:
- **Simple algorithms**: 2-5x speedup
- **Complex algorithms**: 1-3x speedup
- **Overall improvement**: 50-90% faster execution

## 📁 Generated Files

- `benchmark_results.json` - Raw benchmark data
- `overall_performance.png` - Main comparison chart
- `*_performance.png` - Algorithm-specific charts
- `speed_mode_comparison.png` - Speed mode effectiveness
- `complexity_analysis.png` - Complexity vs performance

## 🎯 Usage Examples

### Quick Test
```bash
python test_benchmark.py
```

### Full Benchmark
```bash
python run_benchmark.py
# Choose option 2 for full benchmark
```

### Custom Benchmark
```bash
python run_benchmark.py
# Choose option 3 for custom benchmark
```

## 📊 Sample Output

```
🧪 Bubble Sort (O(n²))
----------------------------------------
  📊 Normal Python: 0.045s (avg)
  ⚡ AI Turbo: 0.012s (avg) - 3.8x speedup
  🚀 AI Fast: 0.018s (avg) - 2.5x speedup
  ⚖️ AI Balanced: 0.025s (avg) - 1.8x speedup
```

## 🔧 Configuration

You can modify `benchmark_system.py` to:
- Add new test algorithms
- Change input sizes
- Adjust speed modes
- Customize graph generation

## 📝 Requirements

- Python 3.8+
- matplotlib
- numpy
- requests
- FastAPI server running on localhost:8000

