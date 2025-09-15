import subprocess
import tempfile
import os
import time
import json
from typing import Dict, Any, List, Tuple
from app.core.config import settings

class CodeExecutionService:
    def __init__(self):
        self.max_execution_time = settings.max_execution_time
        self.max_memory_limit = settings.max_memory_limit * 1024 * 1024  # Convert MB to bytes

    async def execute_python_code(self, code: str, test_cases: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Execute Python code with given test cases.
        Returns execution results including status, time, memory usage, and test results.
        """
        results = {
            "status": "pending",
            "execution_time": 0.0,
            "memory_used": 0,
            "test_cases_passed": 0,
            "total_test_cases": len(test_cases),
            "error_message": None,
            "outputs": []
        }
        
        try:
            for i, test_case in enumerate(test_cases):
                input_data = test_case["input_data"]
                expected_output = test_case["expected_output"].strip()
                
                # Execute code with current test case
                execution_result = await self._run_single_test(code, input_data)
                
                if execution_result["status"] == "error":
                    results["status"] = "runtime_error"
                    results["error_message"] = execution_result["error"]
                    break
                elif execution_result["status"] == "timeout":
                    results["status"] = "time_limit_exceeded"
                    results["error_message"] = f"Time limit exceeded ({self.max_execution_time}s)"
                    break
                else:
                    actual_output = execution_result["output"].strip()
                    results["outputs"].append({
                        "input": input_data,
                        "expected": expected_output,
                        "actual": actual_output,
                        "passed": actual_output == expected_output
                    })
                    
                    if actual_output == expected_output:
                        results["test_cases_passed"] += 1
                    
                    # Update timing and memory info
                    results["execution_time"] = max(results["execution_time"], execution_result["execution_time"])
                    results["memory_used"] = max(results["memory_used"], execution_result["memory_used"])
            
            # Determine final status
            if results["status"] == "pending":
                if results["test_cases_passed"] == results["total_test_cases"]:
                    results["status"] = "accepted"
                else:
                    results["status"] = "wrong_answer"
                    
        except Exception as e:
            results["status"] = "runtime_error"
            results["error_message"] = str(e)
        
        return results

    async def _run_single_test(self, code: str, input_data: str) -> Dict[str, Any]:
        """Run a single test case and return the result."""
        
        # Create a wrapper script that handles input/output
        wrapper_code = f'''
import sys
import io
import time
import traceback

# Redirect stdin
sys.stdin = io.StringIO("""{input_data}""")

# Capture stdout
captured_output = io.StringIO()
sys.stdout = captured_output

start_time = time.time()

try:
    # User's code
{self._indent_code(code)}
    
    execution_time = time.time() - start_time
    output = captured_output.getvalue()
    
    print("{{OUTPUT_START}}" + output + "{{OUTPUT_END}}", file=sys.stderr)
    print("{{TIME_START}}" + str(execution_time) + "{{TIME_END}}", file=sys.stderr)
    
except Exception as e:
    execution_time = time.time() - start_time
    print("{{ERROR_START}}" + str(e) + "\\n" + traceback.format_exc() + "{{ERROR_END}}", file=sys.stderr)
    print("{{TIME_START}}" + str(execution_time) + "{{TIME_END}}", file=sys.stderr)
'''

        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(wrapper_code)
                temp_file = f.name
            
            # Execute with timeout
            process = subprocess.Popen(
                ['python3', temp_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            try:
                stdout, stderr = process.communicate(timeout=self.max_execution_time)
                
                # Parse results from stderr
                result = self._parse_execution_result(stderr)
                
                if process.returncode != 0 and result["status"] != "error":
                    result = {
                        "status": "error",
                        "error": stderr,
                        "execution_time": 0.0,
                        "memory_used": 0,
                        "output": ""
                    }
                
                return result
                
            except subprocess.TimeoutExpired:
                process.kill()
                return {
                    "status": "timeout",
                    "error": "Time limit exceeded",
                    "execution_time": self.max_execution_time,
                    "memory_used": 0,
                    "output": ""
                }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "execution_time": 0.0,
                "memory_used": 0,
                "output": ""
            }
        
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_file)
            except:
                pass

    def _indent_code(self, code: str) -> str:
        """Indent user code for wrapper script."""
        return '\n'.join('    ' + line for line in code.split('\n'))

    def _parse_execution_result(self, stderr: str) -> Dict[str, Any]:
        """Parse execution results from stderr."""
        result = {
            "status": "success",
            "output": "",
            "execution_time": 0.0,
            "memory_used": 0,
            "error": None
        }
        
        try:
            # Extract output
            if "{OUTPUT_START}" in stderr and "{OUTPUT_END}" in stderr:
                start = stderr.find("{OUTPUT_START}") + len("{OUTPUT_START}")
                end = stderr.find("{OUTPUT_END}")
                result["output"] = stderr[start:end]
            
            # Extract execution time
            if "{TIME_START}" in stderr and "{TIME_END}" in stderr:
                start = stderr.find("{TIME_START}") + len("{TIME_START}")
                end = stderr.find("{TIME_END}")
                try:
                    result["execution_time"] = float(stderr[start:end])
                except:
                    pass
            
            # Extract error
            if "{ERROR_START}" in stderr and "{ERROR_END}" in stderr:
                start = stderr.find("{ERROR_START}") + len("{ERROR_START}")
                end = stderr.find("{ERROR_END}")
                result["error"] = stderr[start:end]
                result["status"] = "error"
        
        except Exception as e:
            result["status"] = "error"
            result["error"] = f"Failed to parse execution result: {str(e)}"
        
        return result