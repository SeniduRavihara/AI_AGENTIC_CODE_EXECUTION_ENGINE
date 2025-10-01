'use client';

import { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';

const Editor = dynamic(() => import('@monaco-editor/react'), { ssr: false });

interface ExecutionResult {
  success: boolean;
  final_variables: Record<string, any>;
  console_output: string[];
  execution_steps: string[];
  ai_reasoning: string;
  confidence: number;
  execution_time: number;
  timestamp: string;
  coordinator: {
    agent_used: string;
    execution_method: string;
  };
}

export default function Home() {
  const [language, setLanguage] = useState('python');
  
  const getLanguageExample = (lang: string) => {
    if (lang === 'java') {
      return `// AI Java Interpreter - Basic Java Test
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Testing Java execution with AI reasoning!");
        System.out.println("==========================================");
        
        // Test 1: Basic variables
        int age = 25;
        String status;
        System.out.println("Age: " + age);
        
        if (age >= 18) {
            status = "adult";
            System.out.println("Since " + age + " >= 18, you are an " + status);
        } else {
            status = "minor";
            System.out.println("Since " + age + " < 18, you are a " + status);
        }
        
        // Test 2: Loops and calculations
        int sum = 0;
        for (int i = 1; i <= 5; i++) {
            sum += i;
            System.out.println("Adding " + i + ", sum is now: " + sum);
        }
        
        System.out.println("==========================================");
        System.out.println("Final status: " + status + ", sum: " + sum);
    }
}`;
    } else {
      return `# AI Python Interpreter - If/Else Statement Test
print("Testing if/else statements with AI reasoning!")
print("=" * 50)

# Test 1: Basic if/else
age = 25
print(f"Age: {age}")

if age >= 18:
    status = "adult"
    print(f"Since {age} >= 18, you are an {status}")
else:
    status = "minor"
    print(f"Since {age} < 18, you are a {status}")

# Test 2: Nested conditions
score = 85
print(f"\\nScore: {score}")

if score >= 90:
    grade = "A"
    print(f"Excellent! Grade: {grade}")
elif score >= 80:
    grade = "B"
    print(f"Good job! Grade: {grade}")
elif score >= 70:
    grade = "C"
    print(f"Average. Grade: {grade}")
else:
    grade = "F"
    print(f"Need improvement. Grade: {grade}")

# Test 3: Complex condition
x = 15
y = 10
print(f"\\nx = {x}, y = {y}")

if x > y and x > 10:
    result = "x is large and greater than y"
    print(f"Complex condition true: {result}")
else:
    result = "condition not met"
    print(f"Complex condition false: {result}")

print("=" * 50)
print(f"Final status: {status}, grade: {grade}, result: {result}")`;
    }
  };

  const [code, setCode] = useState(() => getLanguageExample('python'));
  const [result, setResult] = useState<ExecutionResult | null>(null);
  const [isExecuting, setIsExecuting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState('console');
  const [isMaximized, setIsMaximized] = useState(false);
  const [sessionTime, setSessionTime] = useState('00:00:00');

  // Session timer
  useEffect(() => {
    const startTime = Date.now();
    const timer = setInterval(() => {
      const elapsed = Date.now() - startTime;
      const hours = Math.floor(elapsed / 3600000);
      const minutes = Math.floor((elapsed % 3600000) / 60000);
      const seconds = Math.floor((elapsed % 60000) / 1000);
      setSessionTime(`${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`);
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const executeCode = async () => {
    setIsExecuting(true);
    setError(null);
    setResult(null);

    try {
      console.log('Sending request:', { code: code.substring(0, 100) + '...', language });
      
      const response = await fetch('http://localhost:8000/execute', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code: code,
          language: language,
        }),
      });

      console.log('Response status:', response.status);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Error response:', errorText);
        throw new Error(`HTTP error! status: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Execution failed');
    } finally {
      setIsExecuting(false);
    }
  };

  const copyCode = () => {
    navigator.clipboard.writeText(code);
  };

  const resetCode = () => {
    setCode(getLanguageExample(language));
  };

  const handleLanguageChange = (newLanguage: string) => {
    setLanguage(newLanguage);
    setCode(getLanguageExample(newLanguage));
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0a0a0a] via-[#111111] to-[#0a0a0a] text-white">
      {/* Premium Header */}
      <header className="bg-gradient-to-r from-[#0a0a0a] via-[#111111] to-[#0a0a0a] border-b border-[#1f1f1f] shadow-2xl backdrop-blur-xl">
        <div className="max-w-full px-8 py-6">
          <div className="flex items-center justify-between">
            {/* Left Section - Branding */}
            <div className="flex items-center space-x-6">
              <div className="relative group">
                <div className="absolute inset-0 bg-gradient-to-r from-orange-500 via-red-500 to-pink-500 rounded-2xl blur opacity-40 group-hover:opacity-60 transition-opacity duration-300"></div>
                <div className="relative bg-gradient-to-r from-[#1a1a1a] to-[#262626] p-4 rounded-2xl border border-[#333] shadow-xl">
                  <span className="text-3xl">🤖</span>
                </div>
              </div>
              
              <div className="flex flex-col">
                <div className="flex items-center space-x-3">
                  <h1 className="text-2xl font-bold bg-gradient-to-r from-white via-gray-100 to-gray-300 bg-clip-text text-transparent">
                    AI Python Interpreter
                  </h1>
                  <div className="flex items-center px-3 py-1.5 bg-gradient-to-r from-orange-500/20 to-red-500/20 border border-orange-500/30 rounded-full shadow-lg">
                    <span className="text-orange-400 mr-1.5">✨</span>
                    <span className="text-sm font-medium text-orange-300">Powered by Gemini</span>
                  </div>
                </div>
                <p className="text-gray-400 mt-1">Advanced AI-powered code execution and analysis</p>
              </div>
            </div>

            {/* Center Section - Status Indicators */}
            <div className="hidden lg:flex items-center space-x-6">
              <div className="flex items-center space-x-4">
                <div className="relative group">
                  <div className="absolute inset-0 bg-gradient-to-r from-emerald-500/20 to-green-500/20 rounded-lg blur-sm"></div>
                  <div className="relative flex items-center space-x-2 px-4 py-2.5 bg-gradient-to-r from-[#1a1a1a] to-[#222222] border border-emerald-500/20 rounded-lg">
                    <div className="w-3 h-3 bg-gradient-to-r from-emerald-400 to-green-400 rounded-full animate-pulse"></div>
                    <span className="text-sm font-medium text-gray-200">Python 3.11</span>
                    <span className="text-emerald-400">⚡</span>
                  </div>
                </div>
                
                <div className="flex items-center space-x-3 px-4 py-2.5 bg-gradient-to-r from-[#1a1a1a] to-[#1f1f1f] border border-[#333] rounded-lg">
                  <span className="text-blue-400">📊</span>
                  <span className="text-sm text-gray-300">Session: {sessionTime}</span>
                </div>
              </div>
            </div>

            {/* Right Section - Action Controls */}
            <div className="flex items-center space-x-4">
              {/* Language Selector */}
              <div className="flex items-center space-x-2">
                <span className="text-sm text-gray-400">Language:</span>
                <select 
                  value={language}
                  onChange={(e) => handleLanguageChange(e.target.value)}
                  className="bg-gradient-to-b from-[#2a2a2a] to-[#1f1f1f] border border-[#404040] rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-orange-500 transition-colors"
                >
                  <option value="python">🐍 Python</option>
                  <option value="java">☕ Java</option>
                </select>
              </div>
              
              <div className="flex items-center space-x-2">
                <button className="p-3 bg-gradient-to-b from-[#2a2a2a] to-[#1f1f1f] hover:from-[#333] hover:to-[#2a2a2a] border border-[#404040] hover:border-[#525252] rounded-xl transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95 group">
                  <span className="text-gray-400 group-hover:text-white transition-all duration-300">⚙️</span>
                </button>
                
                <button 
                  onClick={() => setIsMaximized(!isMaximized)}
                  className="p-3 bg-gradient-to-b from-[#2a2a2a] to-[#1f1f1f] hover:from-[#333] hover:to-[#2a2a2a] border border-[#404040] hover:border-[#525252] rounded-xl transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95 group"
                >
                  {isMaximized ? 
                    <span className="text-gray-400 group-hover:text-white transition-colors duration-200">🗕</span> :
                    <span className="text-gray-400 group-hover:text-white transition-colors duration-200">🗖</span>
                  }
                </button>
              </div>
              
              <div className="w-px h-10 bg-gradient-to-b from-transparent via-[#404040] to-transparent"></div>
              
              <button
                onClick={executeCode}
                disabled={isExecuting}
                className="group relative px-8 py-3 bg-gradient-to-r from-orange-600 via-red-600 to-pink-600 hover:from-orange-500 hover:via-red-500 hover:to-pink-500 border border-orange-500/50 rounded-xl shadow-lg hover:shadow-orange-500/25 hover:shadow-xl transition-all duration-300 transform hover:scale-105 active:scale-95 disabled:opacity-60 disabled:cursor-not-allowed disabled:hover:scale-100 overflow-hidden"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700 skew-x-12"></div>
                <div className="relative flex items-center space-x-2">
                  {isExecuting ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                      <span className="text-white font-medium">Analyzing...</span>
                    </>
                  ) : (
                    <>
                      <span className="text-white group-hover:scale-110 transition-transform duration-200">▶️</span>
                      <span className="text-white font-medium">Execute Code</span>
                    </>
                  )}
                </div>
              </button>
            </div>
          </div>
        </div>

        {/* Status Bar */}
        <div className="flex items-center justify-between px-8 py-3 bg-gradient-to-r from-[#0f0f0f] to-[#141414] border-t border-[#1a1a1a]">
          <div className="flex items-center space-x-6 text-sm">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></div>
              <span className="text-gray-400">System Ready</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-blue-400">💻</span>
              <span className="text-gray-500">CPU: 15%</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-purple-400">💾</span>
              <span className="text-gray-500">Memory: 2.1GB</span>
            </div>
          </div>
          
          <div className="flex items-center space-x-4 text-sm text-gray-500">
            <span>AI Enhanced Execution</span>
            <span>•</span>
            <span>Press Ctrl+Enter to run</span>
          </div>
        </div>
      </header>

      {/* Error Banner */}
      {error && (
        <div className="mx-8 mt-6 p-4 bg-gradient-to-r from-red-900/30 to-red-800/30 border border-red-500/50 rounded-xl backdrop-blur-sm shadow-lg">
          <div className="flex items-start space-x-3">
            <span className="text-red-400 flex-shrink-0 mt-0.5">❌</span>
            <div>
              <p className="text-red-300 font-medium">{error}</p>
              <p className="text-red-400 text-sm mt-1">
                Make sure the backend server is running on http://localhost:8000
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Main Interface */}
      <div className="flex-1 flex h-[calc(100vh-200px)]">
        {/* Code Editor Panel */}
        <div className="flex-1 flex flex-col bg-gradient-to-br from-[#1a1a1a] to-[#1f1f1f] m-4 rounded-2xl border border-[#2a2a2a] shadow-2xl overflow-hidden">
          {/* Editor Header */}
          <div className="flex items-center justify-between px-6 py-4 bg-gradient-to-r from-[#1f1f1f] to-[#252525] border-b border-[#2a2a2a]">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 px-3 py-2 bg-gradient-to-r from-[#2a2a2a] to-[#333333] border border-[#404040] rounded-lg">
                <span className="text-orange-400">{language === 'java' ? '☕' : '📜'}</span>
                <span className="text-sm text-gray-200 font-medium">
                  {language === 'java' ? 'HelloWorld.java' : 'main.py'}
                </span>
              </div>
              <div className="flex items-center space-x-2 text-sm text-gray-400">
                <span>💻</span>
                <span>{language === 'java' ? 'Java 17' : 'Python 3.11.0'}</span>
              </div>
            </div>
            
            <div className="flex items-center space-x-3">
              <button
                onClick={copyCode}
                className="p-2.5 bg-gradient-to-b from-[#2a2a2a] to-[#222222] hover:from-[#333333] hover:to-[#2a2a2a] border border-[#404040] hover:border-[#525252] rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95 group"
                title="Copy code"
              >
                <span className="text-gray-400 group-hover:text-white transition-colors duration-200">📋</span>
              </button>
              
              <button
                onClick={resetCode}
                className="p-2.5 bg-gradient-to-b from-[#2a2a2a] to-[#222222] hover:from-[#333333] hover:to-[#2a2a2a] border border-[#404040] hover:border-[#525252] rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95 group"
                title="Reset code"
              >
                <span className="text-gray-400 group-hover:text-white transition-all duration-200">🔄</span>
              </button>
              
              <button className="p-2.5 bg-gradient-to-b from-[#2a2a2a] to-[#222222] hover:from-[#333333] hover:to-[#2a2a2a] border border-[#404040] hover:border-[#525252] rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105 active:scale-95 group">
                <span className="text-gray-400 group-hover:text-white transition-colors duration-200">⋯</span>
              </button>
            </div>
          </div>
          
          {/* Monaco Editor */}
          <div className="flex-1 relative">
            <Editor
              height="100%"
              defaultLanguage={language}
              language={language}
              value={code}
              onChange={(value) => setCode(value || '')}
              theme="vs-dark"
              options={{
                fontSize: 14,
                fontFamily: 'Monaco, Menlo, "Fira Code", "Ubuntu Mono", monospace',
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                automaticLayout: true,
                tabSize: 4,
                insertSpaces: true,
                wordWrap: 'on',
                lineNumbers: 'on',
                renderLineHighlight: 'line',
                cursorStyle: 'line',
                smoothScrolling: true,
                fontLigatures: true,
                bracketPairColorization: { enabled: true },
                guides: {
                  bracketPairs: true,
                  indentation: true
                }
              }}
            />
            <div className="absolute inset-0 pointer-events-none bg-gradient-to-t from-black/5 via-transparent to-transparent"></div>
          </div>

          {/* Editor Footer */}
          <div className="px-6 py-3 bg-gradient-to-r from-[#1a1a1a] to-[#1f1f1f] border-t border-[#2a2a2a]">
            <div className="flex items-center justify-between text-sm">
              <div className="flex items-center space-x-4 text-gray-500">
                <span>Lines: {code.split('\n').length}</span>
                <span>•</span>
                <span>Characters: {code.length}</span>
                <span>•</span>
                <span>Ready for execution</span>
              </div>
              <div className="flex items-center space-x-2 text-gray-400">
                <span>👁️</span>
                <span>Live Analysis</span>
              </div>
            </div>
          </div>
        </div>

        {/* Results Panel */}
        <div className="w-1/2 flex flex-col bg-gradient-to-br from-[#1a1a1a] to-[#1f1f1f] m-4 ml-0 rounded-2xl border border-[#2a2a2a] shadow-2xl overflow-hidden">
          {/* Results Header */}
          <div className="px-6 py-4 bg-gradient-to-r from-[#1f1f1f] to-[#252525] border-b border-[#2a2a2a]">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="flex items-center space-x-2 px-3 py-2 bg-gradient-to-r from-[#2a2a2a] to-[#333333] border border-[#404040] rounded-lg">
                  <span className="text-purple-400">🤖</span>
                  <span className="text-sm text-gray-200 font-medium">AI Analysis</span>
                </div>
                {result && (
                  <div className="flex items-center space-x-2">
                    {result.success ? (
                      <span className="text-green-400">✅</span>
                    ) : (
                      <span className="text-red-400">❌</span>
                    )}
                    <span className={`text-sm font-medium ${result.success ? 'text-green-400' : 'text-red-400'}`}>
                      {result.success ? 'Success' : 'Failed'}
                    </span>
                  </div>
                )}
              </div>
              
              <div className="flex items-center space-x-2">
                <button className="p-2 bg-gradient-to-b from-[#2a2a2a] to-[#222222] hover:from-[#333333] hover:to-[#2a2a2a] border border-[#404040] hover:border-[#525252] rounded-lg transition-all duration-200 group">
                  <span className="text-gray-400 group-hover:text-white transition-colors duration-200">⬇️</span>
                </button>
                <button className="p-2 bg-gradient-to-b from-[#2a2a2a] to-[#222222] hover:from-[#333333] hover:to-[#2a2a2a] border border-[#404040] hover:border-[#525252] rounded-lg transition-all duration-200 group">
                  <span className="text-gray-400 group-hover:text-white transition-colors duration-200">📤</span>
                </button>
              </div>
            </div>

            {/* Tab Navigation */}
            <div className="flex items-center space-x-1 mt-4">
              {['console', 'variables', 'steps', 'reasoning', 'details'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                    activeTab === tab
                      ? 'bg-gradient-to-r from-orange-500/20 to-red-500/20 border border-orange-500/30 text-orange-300'
                      : 'text-gray-400 hover:text-white hover:bg-[#2a2a2a]'
                  }`}
                >
                  {tab.charAt(0).toUpperCase() + tab.slice(1)}
                </button>
              ))}
            </div>
          </div>
          
          {/* Results Content */}
          <div className="flex-1 overflow-auto">
            {isExecuting ? (
              <div className="flex items-center justify-center h-full px-8">
                <div className="text-center space-y-6 max-w-sm mx-auto">
                  <div className="relative flex justify-center">
                    <div className="w-20 h-20 border-4 border-orange-500/30 border-t-orange-500 rounded-full animate-spin"></div>
                    <div className="absolute inset-0 flex items-center justify-center">
                      <span className="text-orange-400 text-3xl">🤖</span>
                    </div>
                  </div>
                  <div className="space-y-3">
                    <p className="text-white text-lg font-semibold">AI is analyzing your code...</p>
                    <p className="text-gray-400 text-center leading-relaxed">This may take a few moments</p>
                  </div>
                </div>
              </div>
            ) : result ? (
              <div className="p-6">
                {activeTab === 'console' && (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-semibold text-white">Console Output</h3>
                      <div className="flex items-center space-x-2 text-sm text-gray-400">
                        <span>💻</span>
                        <span>{result.console_output?.length || 0} lines</span>
                      </div>
                    </div>
                    <div className="bg-black border border-[#333] rounded-xl overflow-hidden">
                      <div className="bg-[#1a1a1a] border-b border-[#333] px-4 py-2 flex items-center space-x-2">
                        <span className="text-green-400 text-sm">●</span>
                        <span className="text-white text-sm font-mono">Python Console</span>
                        <div className="flex-1"></div>
                        <span className="text-gray-500 text-xs">Output</span>
                      </div>
                      <div className="p-4 font-mono text-sm min-h-[200px] max-h-[400px] overflow-auto">
                        {result.console_output && result.console_output.length > 0 ? (
                          <div className="space-y-1">
                            {result.console_output.map((line, index) => (
                              <div key={index} className="text-white leading-relaxed">
                                {line}
                              </div>
                            ))}
                          </div>
                        ) : (
                          <div className="text-gray-500 italic flex items-center justify-center h-32">
                            <div className="text-center">
                              <div className="text-2xl mb-2">📟</div>
                              <div>No console output</div>
                              <div className="text-xs mt-1">(no print statements executed)</div>
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                    <div className="text-xs text-gray-500 flex items-center space-x-2">
                      <span>📝</span>
                      <span>Output from print() statements and expressions</span>
                    </div>
                  </div>
                )}

                {activeTab === 'variables' && Object.keys(result.final_variables).length > 0 && (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-semibold text-white">Final Variables</h3>
                      <div className="flex items-center space-x-2 text-sm text-gray-400">
                        <span>📚</span>
                        <span>{Object.keys(result.final_variables).length} variables</span>
                      </div>
                    </div>
                    <div className="grid gap-3">
                      {Object.entries(result.final_variables).map(([key, value]) => (
                        <div key={key} className="bg-gradient-to-r from-[#252526] to-[#2a2a2a] border border-[#3e3e3e] rounded-xl p-4 hover:border-[#4a4a4a] transition-colors duration-200">
                          <div className="flex items-center justify-between mb-2">
                            <span className="font-mono text-orange-400 font-medium">{key}</span>
                            <span className="font-mono text-white bg-[#1a1a1a] px-2 py-1 rounded-lg border border-[#333]">
                              {typeof value === 'string' ? `"${value}"` : String(value)}
                            </span>
                          </div>
                          <div className="flex items-center space-x-2">
                            <span className="text-xs px-2 py-1 bg-blue-500/20 border border-blue-500/30 rounded-full text-blue-300">
                              {typeof value}
                            </span>
                            <span className="text-xs text-gray-500">
                              Size: {typeof value === 'string' ? value.length : String(value).length} chars
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {activeTab === 'steps' && result.execution_steps.length > 0 && (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-semibold text-white">Execution Steps</h3>
                      <div className="flex items-center space-x-2 text-sm text-gray-400">
                        <span>📈</span>
                        <span>{result.execution_steps.length} steps</span>
                      </div>
                    </div>
                    <div className="space-y-3">
                      {result.execution_steps.map((step, index) => (
                        <div key={index} className="flex items-start space-x-4 p-4 bg-gradient-to-r from-[#252526] to-[#2a2a2a] border border-[#3e3e3e] rounded-xl hover:border-[#4a4a4a] transition-colors duration-200">
                          <div className="w-8 h-8 bg-gradient-to-r from-orange-500 to-red-500 text-white rounded-xl flex items-center justify-center text-sm font-bold flex-shrink-0 shadow-lg">
                            {index + 1}
                          </div>
                          <p className="text-gray-200 leading-relaxed">{step}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {activeTab === 'reasoning' && (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-semibold text-white">AI Reasoning</h3>
                      <div className="flex items-center space-x-2 text-sm text-gray-400">
                        <span>{Math.round(result.confidence * 100)}% confidence</span>
                      </div>
                    </div>
                    <div className="bg-gradient-to-br from-[#252526] to-[#2a2a2a] border border-[#3e3e3e] rounded-xl p-6 hover:border-[#4a4a4a] transition-colors duration-200">
                      <p className="text-gray-200 leading-relaxed whitespace-pre-wrap">
                        {result.ai_reasoning}
                      </p>
                    </div>
                  </div>
                )}

                {activeTab === 'details' && (
                  <div className="space-y-6">
                    <h3 className="text-lg font-semibold text-white">Execution Details</h3>
                    
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-gradient-to-br from-[#252526] to-[#2a2a2a] border border-[#3e3e3e] rounded-xl p-4">
                        <div className="flex items-center space-x-3 mb-3">
                          <span className="text-purple-400">🤖</span>
                          <span className="text-sm font-medium text-gray-300">Agent Used</span>
                        </div>
                        <p className="text-white font-medium">{result.coordinator.agent_used}</p>
                      </div>
                      
                      <div className="bg-gradient-to-br from-[#252526] to-[#2a2a2a] border border-[#3e3e3e] rounded-xl p-4">
                        <div className="flex items-center space-x-3 mb-3">
                          <span className="text-yellow-400">⚡</span>
                          <span className="text-sm font-medium text-gray-300">Execution Method</span>
                        </div>
                        <p className="text-white font-medium">{result.coordinator.execution_method}</p>
                      </div>
                      
                      <div className="bg-gradient-to-br from-[#252526] to-[#2a2a2a] border border-[#3e3e3e] rounded-xl p-4">
                        <div className="flex items-center space-x-3 mb-3">
                          <span className="text-blue-400">⏰</span>
                          <span className="text-sm font-medium text-gray-300">Execution Time</span>
                        </div>
                        <p className="text-white font-medium">{(result.execution_time * 1000).toFixed(2)}ms</p>
                      </div>
                      
                      <div className="bg-gradient-to-br from-[#252526] to-[#2a2a2a] border border-[#3e3e3e] rounded-xl p-4">
                        <div className="flex items-center space-x-3 mb-3">
                          <span className="text-green-400">📊</span>
                          <span className="text-sm font-medium text-gray-300">Confidence</span>
                        </div>
                        <div className="space-y-2">
                          <p className="text-white font-medium">{(result.confidence * 100).toFixed(1)}%</p>
                          <div className="w-full bg-[#1a1a1a] rounded-full h-2">
                            <div 
                              className="bg-gradient-to-r from-green-500 to-emerald-500 h-2 rounded-full transition-all duration-300"
                              style={{ width: `${result.confidence * 100}%` }}
                            ></div>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="bg-gradient-to-br from-[#252526] to-[#2a2a2a] border border-[#3e3e3e] rounded-xl p-4">
                      <div className="flex items-center space-x-3 mb-3">
                        <span className="text-orange-400">⏰</span>
                        <span className="text-sm font-medium text-gray-300">Timestamp</span>
                      </div>
                      <p className="text-white font-medium">
                        {new Date(result.timestamp).toLocaleString()}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex items-center justify-center h-full px-8">
                <div className="text-center space-y-8 max-w-md mx-auto">
                  <div className="relative flex justify-center">
                    <div className="w-24 h-24 bg-gradient-to-r from-[#252526] to-[#2a2a2a] border border-[#3e3e3e] rounded-2xl flex items-center justify-center shadow-xl">
                      <div className="text-5xl">🚀</div>
                    </div>
                    <div className="absolute -top-2 -right-2 w-8 h-8 bg-gradient-to-r from-orange-500 to-red-500 rounded-full flex items-center justify-center">
                      <span className="text-white text-sm">✨</span>
                    </div>
                  </div>
                  <div className="space-y-3">
                    <h3 className="text-2xl font-bold text-white">Ready for AI Analysis</h3>
                    <p className="text-gray-400 text-center leading-relaxed">
                      Execute your Python code to see detailed AI-powered analysis, variable tracking, and intelligent reasoning.
                    </p>
                  </div>
                  <div className="flex items-center justify-center space-x-6 text-sm text-gray-500">
                    <div className="flex items-center space-x-2">
                      <span className="text-lg">🤖</span>
                      <span>AI Powered</span>
                    </div>
                    <div className="w-1 h-1 bg-gray-600 rounded-full"></div>
                    <div className="flex items-center space-x-2">
                      <span className="text-lg">⚡</span>
                      <span>Real-time Analysis</span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}