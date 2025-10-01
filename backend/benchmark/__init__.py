"""
Benchmark Package - Performance comparison between AI agents and normal Python execution
"""

from .benchmark_system import BenchmarkSystem
from .run_benchmark import main as run_benchmark
from .test_benchmark import main as test_benchmark

__all__ = [
    "BenchmarkSystem",
    "run_benchmark", 
    "test_benchmark"
]

__version__ = "1.0.0"
__author__ = "AI Agentic Code Execution Engine"
__description__ = "Comprehensive benchmarking system for AI agent performance analysis"

