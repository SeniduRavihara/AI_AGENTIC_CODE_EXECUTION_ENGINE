"""
DSA Orchestrator - Manages complex DSA problems using dynamic agent creation
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from .agent_factory import AgentFactory


class DSAOrchestrator:
    """
    Orchestrates execution of large-scale DSA problems using dynamic agent creation
    """
    
    def __init__(self):
        self.agent_factory = AgentFactory()
        self.execution_history = []
        
    async def execute_large_dsa_problem(self, code: str, input_data: Any, problem_type: str = "general") -> Dict[str, Any]:
        """
        Execute large DSA problem with intelligent agent coordination
        
        Args:
            code: DSA algorithm code
            input_data: Large input dataset
            problem_type: Type of DSA problem (sorting, graph, dp, etc.)
            
        Returns:
            Comprehensive execution results with performance metrics
        """
        
        start_time = datetime.now()
        execution_id = f"dsa_exec_{int(start_time.timestamp())}"
        
        print(f"🚀 Starting DSA Orchestration: {execution_id}")
        print(f"📊 Problem Type: {problem_type}")
        print(f"📏 Input Size: {self._estimate_input_size(input_data)}")
        
        try:
            # Phase 1: Analyze the problem
            analysis_result = await self._analyze_problem(code, input_data, problem_type)
            
            # Phase 2: Determine execution strategy
            strategy = await self._determine_execution_strategy(analysis_result, input_data)
            
            # Phase 3: Execute based on strategy
            if strategy["use_parallel"]:
                execution_result = await self._execute_parallel(code, input_data, strategy, problem_type)
            else:
                execution_result = await self._execute_sequential(code, input_data, problem_type)
            
            # Phase 4: Compile final results
            final_result = await self._compile_final_results(
                analysis_result, strategy, execution_result, start_time
            )
            
            self.execution_history.append({
                "execution_id": execution_id,
                "timestamp": start_time.isoformat(),
                "problem_type": problem_type,
                "strategy": strategy,
                "performance": final_result.get("performance_metrics", {})
            })
            
            return final_result
            
        except Exception as e:
            return {
                "success": False,
                "execution_id": execution_id,
                "error": f"DSA Orchestration failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    async def _analyze_problem(self, code: str, input_data: Any, problem_type: str) -> Dict[str, Any]:
        """Phase 1: Analyze problem complexity and characteristics"""
        
        print("🔍 Phase 1: Problem Analysis")
        
        # Create analyzer agent
        analyzer_tasks = [
            {
                "agent_type": "analyzer",
                "specialization": problem_type,
                "data": {
                    "code": code,
                    "input_size": self._estimate_input_size(input_data),
                    "problem_type": problem_type
                },
                "context": {"phase": "analysis"}
            }
        ]
        
        analysis_results = await self.agent_factory.execute_parallel_tasks(analyzer_tasks)
        return analysis_results[0] if analysis_results else {}
    
    async def _determine_execution_strategy(self, analysis: Dict[str, Any], input_data: Any) -> Dict[str, Any]:
        """Phase 2: Determine optimal execution strategy"""
        
        print("🎯 Phase 2: Strategy Determination")
        
        input_size = self._estimate_input_size(input_data)
        time_complexity = analysis.get("time_complexity", "O(n)")
        
        # Determine if parallel execution is beneficial
        use_parallel = False
        parallel_threshold = 10000
        
        if input_size > parallel_threshold:
            if "O(n²)" in time_complexity or "O(n³)" in time_complexity:
                use_parallel = True
            elif "O(n log n)" in time_complexity and input_size > 100000:
                use_parallel = True
        
        strategy = {
            "use_parallel": use_parallel,
            "input_size": input_size,
            "estimated_agents_needed": min(8, max(2, input_size // 50000)),
            "chunk_size": max(1000, input_size // 10) if use_parallel else input_size,
            "optimization_level": "high" if input_size > 100000 else "medium"
        }
        
        print(f"📋 Strategy: {'Parallel' if use_parallel else 'Sequential'} execution")
        print(f"🔢 Estimated agents needed: {strategy['estimated_agents_needed']}")
        
        return strategy
    
    async def _execute_parallel(self, code: str, input_data: Any, strategy: Dict[str, Any], problem_type: str) -> Dict[str, Any]:
        """Phase 3a: Execute using parallel agents"""
        
        print("⚡ Phase 3: Parallel Execution")
        
        # Step 1: Split the problem
        split_result = await self._split_problem(code, input_data, strategy, problem_type)
        
        if not split_result.get("parallel_safe", False):
            print("⚠️ Problem not suitable for parallelization, falling back to sequential")
            return await self._execute_sequential(code, input_data, problem_type)
        
        chunks = split_result.get("chunks", [])
        print(f"📦 Split into {len(chunks)} chunks")
        
        # Step 2: Execute chunks in parallel
        executor_tasks = []
        for chunk in chunks:
            executor_tasks.append({
                "agent_type": "executor",
                "specialization": problem_type,
                "data": {
                    "code": code,
                    "chunk": chunk,
                    "input_data": self._extract_chunk_data(input_data, chunk)
                },
                "context": {"execution_mode": "parallel"}
            })
        
        print(f"🔄 Executing {len(executor_tasks)} parallel tasks")
        chunk_results = await self.agent_factory.execute_parallel_tasks(executor_tasks)
        
        # Step 3: Merge results
        merge_result = await self._merge_results(chunk_results, split_result.get("merge_strategy", "simple"), problem_type)
        
        return {
            "success": True,
            "execution_mode": "parallel",
            "chunks_processed": len(chunks),
            "chunk_results": chunk_results,
            "final_result": merge_result,
            "parallel_efficiency": len(chunks) / max(1, len([r for r in chunk_results if r.get("success", False)]))
        }
    
    async def _execute_sequential(self, code: str, input_data: Any, problem_type: str) -> Dict[str, Any]:
        """Phase 3b: Execute using sequential processing"""
        
        print("🔄 Phase 3: Sequential Execution")
        
        executor_tasks = [{
            "agent_type": "executor",
            "specialization": problem_type,
            "data": {
                "code": code,
                "input_data": input_data,
                "chunk": {"chunk_id": 1, "start_index": 0, "end_index": self._estimate_input_size(input_data)}
            },
            "context": {"execution_mode": "sequential"}
        }]
        
        results = await self.agent_factory.execute_parallel_tasks(executor_tasks)
        
        return {
            "success": True,
            "execution_mode": "sequential",
            "result": results[0] if results else {}
        }
    
    async def _split_problem(self, code: str, input_data: Any, strategy: Dict[str, Any], problem_type: str) -> Dict[str, Any]:
        """Split large problem into manageable chunks"""
        
        splitter_tasks = [{
            "agent_type": "splitter",
            "specialization": problem_type,
            "data": {
                "code": code,
                "input_size": strategy["input_size"],
                "problem_type": problem_type,
                "chunk_size": strategy["chunk_size"]
            },
            "context": {"strategy": strategy}
        }]
        
        split_results = await self.agent_factory.execute_parallel_tasks(splitter_tasks)
        return split_results[0] if split_results else {"parallel_safe": False}
    
    async def _merge_results(self, chunk_results: List[Dict[str, Any]], merge_strategy: str, problem_type: str) -> Dict[str, Any]:
        """Merge results from parallel execution"""
        
        merger_tasks = [{
            "agent_type": "merger",
            "specialization": problem_type,
            "data": {
                "chunk_results": chunk_results,
                "merge_strategy": merge_strategy
            },
            "context": {"merge_phase": True}
        }]
        
        merge_results = await self.agent_factory.execute_parallel_tasks(merger_tasks)
        return merge_results[0] if merge_results else {"success": False}
    
    async def _compile_final_results(self, analysis: Dict[str, Any], strategy: Dict[str, Any], 
                                   execution: Dict[str, Any], start_time: datetime) -> Dict[str, Any]:
        """Phase 4: Compile comprehensive results"""
        
        print("📊 Phase 4: Results Compilation")
        
        end_time = datetime.now()
        total_duration = (end_time - start_time).total_seconds()
        
        return {
            "success": execution.get("success", False),
            "execution_mode": execution.get("execution_mode", "unknown"),
            "problem_analysis": analysis,
            "execution_strategy": strategy,
            "execution_results": execution,
            "performance_metrics": {
                "total_execution_time": total_duration,
                "agents_created": len(self.agent_factory.active_agents),
                "parallel_efficiency": execution.get("parallel_efficiency", 1.0),
                "estimated_speedup": strategy.get("estimated_agents_needed", 1) * execution.get("parallel_efficiency", 1.0),
                "memory_efficiency": "optimized" if strategy.get("optimization_level") == "high" else "standard"
            },
            "agent_factory_status": self.agent_factory.get_factory_status(),
            "timestamp": end_time.isoformat(),
            "orchestration_successful": True
        }
    
    def _estimate_input_size(self, input_data: Any) -> int:
        """Estimate size of input data"""
        if isinstance(input_data, (list, tuple)):
            return len(input_data)
        elif isinstance(input_data, str):
            return len(input_data)
        elif isinstance(input_data, dict):
            return len(str(input_data))
        else:
            return len(str(input_data))
    
    def _extract_chunk_data(self, input_data: Any, chunk: Dict[str, Any]) -> Any:
        """Extract relevant data for a specific chunk"""
        if isinstance(input_data, (list, tuple)):
            start = chunk.get("start_index", 0)
            end = chunk.get("end_index", len(input_data))
            return input_data[start:end]
        else:
            return input_data
    
    async def optimize_for_problem_type(self, code: str, problem_type: str) -> Dict[str, Any]:
        """Optimize code specifically for the given problem type"""
        
        print(f"🔧 Optimizing for {problem_type} problems")
        
        optimizer_tasks = [{
            "agent_type": "optimizer",
            "specialization": problem_type,
            "data": {
                "code": code,
                "problem_type": problem_type
            },
            "context": {"optimization_phase": True}
        }]
        
        optimization_results = await self.agent_factory.execute_parallel_tasks(optimizer_tasks)
        return optimization_results[0] if optimization_results else {"success": False}
    
    def get_orchestrator_stats(self) -> Dict[str, Any]:
        """Get comprehensive orchestrator statistics"""
        return {
            "total_executions": len(self.execution_history),
            "agent_factory_status": self.agent_factory.get_factory_status(),
            "recent_executions": self.execution_history[-5:],
            "performance_trends": self._analyze_performance_trends()
        }
    
    def _analyze_performance_trends(self) -> Dict[str, Any]:
        """Analyze performance trends from execution history"""
        if not self.execution_history:
            return {"trend": "no_data"}
        
        recent = self.execution_history[-10:]
        avg_speedup = sum(exec.get("performance", {}).get("estimated_speedup", 1.0) for exec in recent) / len(recent)
        
        return {
            "average_speedup": avg_speedup,
            "parallel_usage_rate": sum(1 for exec in recent if exec.get("strategy", {}).get("use_parallel", False)) / len(recent),
            "trend": "improving" if avg_speedup > 2.0 else "stable"
        }
