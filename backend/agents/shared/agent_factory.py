"""
Dynamic Agent Factory - Creates specialized agents for large-scale DSA problems
"""

import asyncio
from typing import Dict, Any, List, Optional, Type
from datetime import datetime
from .base_agent import BaseAgent


class AgentFactory:
    """
    Factory for creating specialized agents dynamically based on problem requirements
    """
    
    def __init__(self):
        self.active_agents: Dict[str, BaseAgent] = {}
        self.agent_pool: Dict[str, List[BaseAgent]] = {}
        self.max_agents_per_type = 10
        
    async def create_specialized_agent(self, agent_type: str, specialization: str, api_key: Optional[str] = None) -> str:
        """
        Create a specialized agent for specific tasks
        
        Args:
            agent_type: Type of agent (analyzer, optimizer, executor, etc.)
            specialization: Specific specialization (sorting, graph, dp, etc.)
            api_key: Gemini API key
            
        Returns:
            Agent ID for the created agent
        """
        
        agent_id = f"{agent_type}_{specialization}_{len(self.active_agents)}"
        
        if agent_type == "analyzer":
            agent = DSAAnalyzerAgent(specialization, api_key)
        elif agent_type == "optimizer":
            agent = DSAOptimizerAgent(specialization, api_key)
        elif agent_type == "executor":
            agent = DSAExecutorAgent(specialization, api_key)
        elif agent_type == "splitter":
            agent = DSASplitterAgent(specialization, api_key)
        elif agent_type == "merger":
            agent = DSAMergerAgent(specialization, api_key)
        else:
            agent = GenericDSAAgent(specialization, api_key)
        
        self.active_agents[agent_id] = agent
        
        # Add to pool for reuse
        if agent_type not in self.agent_pool:
            self.agent_pool[agent_type] = []
        
        print(f"🤖 Created specialized {agent_type} agent: {agent_id}")
        return agent_id
    
    async def get_or_create_agent(self, agent_type: str, specialization: str) -> str:
        """Get existing agent or create new one"""
        
        # Try to reuse existing agent
        for agent_id, agent in self.active_agents.items():
            if agent_id.startswith(f"{agent_type}_{specialization}") and not agent.is_busy:
                agent.is_busy = True
                return agent_id
        
        # Create new agent if under limit
        type_count = len([aid for aid in self.active_agents.keys() if aid.startswith(agent_type)])
        if type_count < self.max_agents_per_type:
            return await self.create_specialized_agent(agent_type, specialization)
        
        # Wait for agent to become available
        while True:
            for agent_id, agent in self.active_agents.items():
                if agent_id.startswith(f"{agent_type}_{specialization}") and not agent.is_busy:
                    agent.is_busy = True
                    return agent_id
            await asyncio.sleep(0.1)
    
    async def release_agent(self, agent_id: str):
        """Release agent back to pool"""
        if agent_id in self.active_agents:
            self.active_agents[agent_id].is_busy = False
            print(f"🔄 Released agent: {agent_id}")
    
    async def execute_parallel_tasks(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute multiple tasks in parallel using specialized agents"""
        
        async def execute_task(task):
            agent_id = await self.get_or_create_agent(task['agent_type'], task['specialization'])
            try:
                agent = self.active_agents[agent_id]
                result = await agent.execute_task(task['data'], task.get('context', {}))
                result['agent_id'] = agent_id
                return result
            finally:
                await self.release_agent(agent_id)
        
        # Execute all tasks in parallel
        results = await asyncio.gather(*[execute_task(task) for task in tasks])
        return results
    
    def get_factory_status(self) -> Dict[str, Any]:
        """Get current factory status"""
        return {
            "total_agents": len(self.active_agents),
            "agent_types": {},
            "active_agents": list(self.active_agents.keys()),
            "agent_pool_sizes": {k: len(v) for k, v in self.agent_pool.items()}
        }


class DSAAnalyzerAgent(BaseAgent):
    """Specialized agent for analyzing DSA problems"""
    
    def __init__(self, specialization: str, api_key: Optional[str] = None):
        super().__init__(api_key)
        self.specialization = specialization
        self.is_busy = False
    
    async def execute_task(self, code: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze DSA problem complexity and patterns"""
        
        prompt = f"""
You are a specialized DSA Analysis Agent focused on {self.specialization}.

Analyze this {self.specialization} code for:
1. Time complexity (Big O)
2. Space complexity
3. Algorithm patterns used
4. Optimization opportunities
5. Input size handling capabilities

Code to analyze:
```
{code}
```

Context: {context}

Provide analysis in JSON format:
{{
    "time_complexity": "O(n log n)",
    "space_complexity": "O(n)",
    "algorithm_patterns": ["divide_and_conquer", "sorting"],
    "optimization_suggestions": ["Use in-place sorting", "Consider parallel processing"],
    "max_input_size_estimate": 1000000,
    "bottlenecks": ["nested loops", "memory allocation"],
    "specialization": "{self.specialization}",
    "confidence": 0.95
}}
"""
        
        try:
            response = await self._generate_with_gemini(prompt)
            result = self._parse_json_response(response)
            result["agent_type"] = "analyzer"
            result["specialization"] = self.specialization
            return result
        except Exception as e:
            return self._create_error_response(f"Analysis failed: {str(e)}")
    
    def _create_fallback_response(self, response_text: str, error: str) -> Dict[str, Any]:
        return {
            "time_complexity": "O(unknown)",
            "space_complexity": "O(unknown)",
            "algorithm_patterns": [],
            "optimization_suggestions": [f"Analysis error: {error}"],
            "confidence": 0.3
        }


class DSASplitterAgent(BaseAgent):
    """Specialized agent for splitting large inputs into smaller chunks"""
    
    def __init__(self, specialization: str, api_key: Optional[str] = None):
        super().__init__(api_key)
        self.specialization = specialization
        self.is_busy = False
    
    async def execute_task(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Split large DSA problem into smaller manageable chunks"""
        
        code = data.get('code', '')
        input_size = data.get('input_size', 0)
        problem_type = data.get('problem_type', self.specialization)
        
        prompt = f"""
You are a DSA Splitting Agent specialized in {self.specialization}.

Given this large-scale {problem_type} problem, determine how to split it for parallel processing:

Code: {code[:500]}...
Input Size: {input_size}
Problem Type: {problem_type}

Provide splitting strategy in JSON format:
{{
    "split_strategy": "divide_and_conquer",
    "chunk_size": 10000,
    "num_chunks": 100,
    "parallel_safe": true,
    "merge_strategy": "simple_concatenation",
    "dependencies": [],
    "chunks": [
        {{"chunk_id": 1, "start_index": 0, "end_index": 9999}},
        {{"chunk_id": 2, "start_index": 10000, "end_index": 19999}}
    ],
    "estimated_speedup": 4.5,
    "specialization": "{self.specialization}"
}}
"""
        
        try:
            response = await self._generate_with_gemini(prompt)
            result = self._parse_json_response(response)
            result["agent_type"] = "splitter"
            return result
        except Exception as e:
            return self._create_error_response(f"Splitting failed: {str(e)}")
    
    def _create_fallback_response(self, response_text: str, error: str) -> Dict[str, Any]:
        return {
            "split_strategy": "sequential",
            "chunk_size": 1000,
            "num_chunks": 1,
            "parallel_safe": False,
            "merge_strategy": "simple_concatenation"
        }


class DSAExecutorAgent(BaseAgent):
    """Specialized agent for executing DSA code chunks"""
    
    def __init__(self, specialization: str, api_key: Optional[str] = None):
        super().__init__(api_key)
        self.specialization = specialization
        self.is_busy = False
    
    async def execute_task(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a chunk of DSA code"""
        
        code = data.get('code', '')
        chunk_data = data.get('chunk', {})
        
        prompt = f"""
You are a DSA Execution Agent specialized in {self.specialization}.

Execute this code chunk efficiently:

Code:
```
{code}
```

Chunk Data: {chunk_data}
Context: {context}

Provide execution results in JSON format:
{{
    "success": true,
    "result": "chunk_result_data",
    "execution_time": 0.05,
    "memory_used": "2MB",
    "chunk_id": {chunk_data.get('chunk_id', 0)},
    "output": ["result1", "result2"],
    "error": null,
    "specialization": "{self.specialization}"
}}
"""
        
        try:
            response = await self._generate_with_gemini(prompt)
            result = self._parse_json_response(response)
            result["agent_type"] = "executor"
            return result
        except Exception as e:
            return self._create_error_response(f"Execution failed: {str(e)}")
    
    def _create_fallback_response(self, response_text: str, error: str) -> Dict[str, Any]:
        return {
            "success": False,
            "result": None,
            "execution_time": 0.0,
            "error": f"Execution error: {error}"
        }


class DSAMergerAgent(BaseAgent):
    """Specialized agent for merging results from parallel execution"""
    
    def __init__(self, specialization: str, api_key: Optional[str] = None):
        super().__init__(api_key)
        self.specialization = specialization
        self.is_busy = False
    
    async def execute_task(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Merge results from multiple chunk executions"""
        
        chunk_results = data.get('chunk_results', [])
        merge_strategy = data.get('merge_strategy', 'simple_concatenation')
        
        prompt = f"""
You are a DSA Merger Agent specialized in {self.specialization}.

Merge these chunk results using strategy: {merge_strategy}

Chunk Results: {chunk_results}

Provide merged result in JSON format:
{{
    "success": true,
    "merged_result": "final_combined_result",
    "total_chunks_processed": {len(chunk_results)},
    "merge_strategy_used": "{merge_strategy}",
    "final_output": ["merged_data"],
    "performance_stats": {{
        "total_time": 2.5,
        "parallel_speedup": 4.2,
        "efficiency": 0.85
    }},
    "specialization": "{self.specialization}"
}}
"""
        
        try:
            response = await self._generate_with_gemini(prompt)
            result = self._parse_json_response(response)
            result["agent_type"] = "merger"
            return result
        except Exception as e:
            return self._create_error_response(f"Merging failed: {str(e)}")
    
    def _create_fallback_response(self, response_text: str, error: str) -> Dict[str, Any]:
        return {
            "success": False,
            "merged_result": None,
            "error": f"Merge error: {error}"
        }


class DSAOptimizerAgent(BaseAgent):
    """Specialized agent for optimizing DSA algorithms"""
    
    def __init__(self, specialization: str, api_key: Optional[str] = None):
        super().__init__(api_key)
        self.specialization = specialization
        self.is_busy = False
    
    async def execute_task(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize DSA code for better performance"""
        
        code = data.get('code', '')
        analysis = data.get('analysis', {})
        
        prompt = f"""
You are a DSA Optimization Agent specialized in {self.specialization}.

Optimize this code based on analysis:

Original Code:
```
{code}
```

Analysis: {analysis}

Provide optimized version in JSON format:
{{
    "optimized_code": "optimized_version_here",
    "optimizations_applied": ["removed_nested_loops", "used_hash_map"],
    "expected_improvement": {{
        "time_complexity": "O(n) instead of O(n²)",
        "space_complexity": "O(n) instead of O(1)",
        "estimated_speedup": 10.5
    }},
    "trade_offs": ["Uses more memory for better time complexity"],
    "specialization": "{self.specialization}"
}}
"""
        
        try:
            response = await self._generate_with_gemini(prompt)
            result = self._parse_json_response(response)
            result["agent_type"] = "optimizer"
            return result
        except Exception as e:
            return self._create_error_response(f"Optimization failed: {str(e)}")
    
    def _create_fallback_response(self, response_text: str, error: str) -> Dict[str, Any]:
        return {
            "optimized_code": "# Optimization failed",
            "optimizations_applied": [],
            "error": f"Optimization error: {error}"
        }


class GenericDSAAgent(BaseAgent):
    """Generic DSA agent for unspecialized tasks"""
    
    def __init__(self, specialization: str, api_key: Optional[str] = None):
        super().__init__(api_key)
        self.specialization = specialization
        self.is_busy = False
    
    async def execute_task(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute generic DSA task"""
        return {
            "success": True,
            "result": "Generic task completed",
            "agent_type": "generic",
            "specialization": self.specialization
        }
    
    def _create_fallback_response(self, response_text: str, error: str) -> Dict[str, Any]:
        return {
            "success": False,
            "error": f"Generic task error: {error}"
        }
