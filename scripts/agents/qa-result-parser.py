#!/usr/bin/env python3
"""
Test Result Parser for Autonomous Testing
Parses JUnit XML and Playwright reports into structured JSON format
"""

import json
import xml.etree.ElementTree as ET
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import re

class TestResultParser:
    """Parse test results from various formats"""
    
    def __init__(self, results_dir: str):
        self.results_dir = Path(results_dir)
        # If results_dir is actually a file path, use its parent
        if self.results_dir.is_file():
            self.results_dir = self.results_dir.parent
        self.failures = []
        self.results = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "errors": 0
        }
    
    def parse(self) -> Dict[str, Any]:
        """Parse all test results in the directory"""
        # Validate results directory exists
        if not self.results_dir.exists():
            print(f"[PARSER] Warning: Results directory does not exist: {self.results_dir}", file=sys.stderr)
            return {
                "results": {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "errors": 0},
                "failures": [],
                "summary": {"passRate": 0.0, "failureRate": 0.0, "status": "no_results"}
            }
        
        # Try to parse execution log for compilation errors if no test results found
        execution_log = self.results_dir.parent / "execution.log"
        if execution_log.exists():
            compilation_errors = self._parse_compilation_errors(execution_log)
            if compilation_errors:
                print(f"[PARSER] Found {len(compilation_errors)} compilation errors in execution log")
                for i, error in enumerate(compilation_errors):
                    file_path = error.get("file", "")
                    service = error.get("service", "unknown")
                    self.failures.append({
                        "id": f"compilation-{service}-{i}",
                        "testName": file_path.split("/")[-1] if file_path else "compilation",
                        "className": service,
                        "errorType": "CompilationError",
                        "errorMessage": error.get("message", ""),
                        "stackTrace": error.get("details", ""),
                        "category": "compilation",
                        "confidence": 0.95,
                        "sourceFile": error.get("sourceFile", file_path),
                        "service": service,
                        "file": file_path,
                        "details": error.get("details", "")
                    })
                self.results["errors"] = len(compilation_errors)
                self.results["failed"] = len(compilation_errors)
        
        if not self.results_dir.is_dir():
            print(f"[PARSER] Error: Path is not a directory: {self.results_dir}", file=sys.stderr)
            return {
                "results": {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "errors": 0},
                "failures": [],
                "summary": {"passRate": 0.0, "failureRate": 0.0, "status": "error"}
            }
        
        print(f"[PARSER] Parsing test results from: {self.results_dir}")
        
        # Find all JUnit XML files
        try:
            junit_files = list(self.results_dir.rglob("TEST-*.xml"))
            playwright_files = list(self.results_dir.rglob("results.json"))
        except OSError as e:
            print(f"[PARSER] Error accessing results directory: {e}", file=sys.stderr)
            return {
                "results": {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "errors": 0},
                "failures": [],
                "summary": {"passRate": 0.0, "failureRate": 0.0, "status": "error"}
            }
        
        # Parse JUnit XML files
        for junit_file in junit_files:
            self._parse_junit_xml(junit_file)
        
        # Parse Playwright results
        for playwright_file in playwright_files:
            self._parse_playwright_json(playwright_file)
        
        # If we found compilation errors but no test results, return them
        if self.failures and self.results["total"] == 0:
            self.results["total"] = len(self.failures)
        
        return {
            "results": self.results,
            "failures": self.failures,
            "summary": self._generate_summary()
        }
    
    def _parse_compilation_errors(self, log_file: Path) -> List[Dict[str, Any]]:
        """Parse compilation errors from execution log"""
        errors = []
        try:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Pattern for Maven compilation errors - improved to capture full error message
            error_pattern = r'\[ERROR\]\s+(/workspace/[^\s]+\.java):\[(\d+),(\d+)\]\s+((?:cannot find symbol|package [^\s]+ does not exist|symbol:.*?location:).*?)(?=\[ERROR\]|\[INFO\]|\[WARNING\]|$)'
            matches = re.finditer(error_pattern, content, re.MULTILINE | re.DOTALL)
            
            seen_errors = set()  # Track unique errors to avoid duplicates
            for match in matches:
                file_path = match.group(1)
                line = match.group(2)
                col = match.group(3)
                error_text = match.group(4).strip()
                
                # Extract relative file path
                relative_path = file_path.replace("/workspace/", "")
                
                # Extract service name from path
                service_match = re.search(r'/workspace/services/([^/]+)/', file_path)
                service = service_match.group(1) if service_match else "unknown"
                if not service_match:
                    # Try shared/models
                    if "/workspace/shared/" in file_path:
                        service = "shared-models"
                    elif "/workspace/tests/" in file_path:
                        service = "tests"
                
                # Create unique error key to avoid duplicates
                error_key = f"{relative_path}:{line}:{error_text[:100]}"
                if error_key in seen_errors:
                    continue
                seen_errors.add(error_key)
                
                # Extract error type
                if "cannot find symbol" in error_text:
                    error_type = "cannot find symbol"
                elif "package" in error_text and "does not exist" in error_text:
                    error_type = "package does not exist"
                else:
                    error_type = error_text.split('\n')[0][:50]
                
                # Extract error details
                error_details = error_text[:500]
                
                errors.append({
                    "file": relative_path,
                    "line": line,
                    "column": col,
                    "service": service,
                    "type": error_type,
                    "message": f"{error_type} at {relative_path}:{line}:{col}",
                    "details": error_details,
                    "sourceFile": relative_path  # Add for solution finder
                })
            
            # Also look for BUILD FAILURE patterns
            if "BUILD FAILURE" in content and not errors:
                # Extract the error summary
                failure_match = re.search(r'\[ERROR\](.*?)\[ERROR\]', content, re.DOTALL)
                if failure_match:
                    error_text = failure_match.group(1)
                    errors.append({
                        "file": "build",
                        "service": "build",
                        "type": "BUILD FAILURE",
                        "message": "Build failed - compilation errors detected",
                        "details": error_text[:500]
                    })
                    
        except Exception as e:
            print(f"[PARSER] Error parsing compilation errors: {e}", file=sys.stderr)
        
        return errors
    
    def _parse_junit_xml(self, xml_file: Path):
        """Parse JUnit XML test results"""
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            # Handle both JUnit 4 and 5 formats
            if root.tag == "testsuite":
                self._parse_junit_testsuite(root, xml_file)
            elif root.tag == "testsuites":
                for testsuite in root.findall("testsuite"):
                    self._parse_junit_testsuite(testsuite, xml_file)
        except Exception as e:
            print(f"[PARSER] Error parsing {xml_file}: {e}", file=sys.stderr)
    
    def _parse_junit_testsuite(self, testsuite: ET.Element, xml_file: Path):
        """Parse a single testsuite element"""
        # Extract service name from path
        service_name = self._extract_service_name(xml_file)
        
        # Get test counts
        tests = int(testsuite.get("tests", 0))
        failures = int(testsuite.get("failures", 0))
        errors = int(testsuite.get("errors", 0))
        skipped = int(testsuite.get("skipped", 0))
        
        passed = tests - failures - errors - skipped
        
        self.results["total"] += tests
        self.results["passed"] += passed
        self.results["failed"] += failures
        self.results["errors"] += errors
        self.results["skipped"] += skipped
        
        # Parse test cases
        for testcase in testsuite.findall("testcase"):
            self._parse_testcase(testcase, service_name, xml_file)
    
    def _parse_testcase(self, testcase: ET.Element, service_name: str, xml_file: Path):
        """Parse a single test case"""
        test_class = testcase.get("classname", "").split(".")[-1]
        test_method = testcase.get("name", "")
        
        # Check for failures
        failure = testcase.find("failure")
        error = testcase.find("error")
        
        if failure is not None or error is not None:
            issue = failure if failure is not None else error
            error_type = issue.get("type", "Unknown")
            error_message = issue.get("message", "")
            stack_trace = issue.text or ""
            
            # Categorize the failure
            category = self._categorize_failure(error_type, error_message, stack_trace)
            
            # Calculate confidence (simplified - will be enhanced by problem analyzer)
            confidence = self._estimate_confidence(error_type, error_message)
            
            failure_data = {
                "id": f"{service_name}-{test_class}-{test_method}",
                "service": service_name,
                "testClass": test_class,
                "testMethod": test_method,
                "errorType": error_type,
                "errorMessage": error_message,
                "stackTrace": stack_trace[:5000],  # Limit stack trace size
                "category": category,
                "confidence": confidence,
                "sourceFile": str(xml_file.relative_to(self.results_dir.parent.parent.parent))
            }
            
            self.failures.append(failure_data)
    
    def _parse_playwright_json(self, json_file: Path):
        """Parse Playwright test results JSON"""
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            # Playwright results structure
            if isinstance(data, dict) and "suites" in data:
                for suite in data.get("suites", []):
                    for spec in suite.get("specs", []):
                        for test in spec.get("tests", []):
                            self._parse_playwright_test(test, json_file)
        except Exception as e:
            print(f"[PARSER] Error parsing Playwright results {json_file}: {e}", file=sys.stderr)
    
    def _parse_playwright_test(self, test: Dict, json_file: Path):
        """Parse a single Playwright test result"""
        test_title = test.get("title", "")
        test_file = test.get("file", "")
        
        results = test.get("results", [])
        for result in results:
            status = result.get("status", "")
            
            if status == "passed":
                self.results["passed"] += 1
                self.results["total"] += 1
            elif status == "failed":
                self.results["failed"] += 1
                self.results["total"] += 1
                
                # Extract failure details
                error = result.get("error", {})
                error_message = error.get("message", "")
                stack_trace = error.get("stack", "")
                
                category = self._categorize_failure("PlaywrightError", error_message, stack_trace)
                confidence = self._estimate_confidence("PlaywrightError", error_message)
                
                failure_data = {
                    "id": f"e2e-{test_file}-{test_title}",
                    "service": "frontend",
                    "testClass": test_file,
                    "testMethod": test_title,
                    "errorType": "PlaywrightError",
                    "errorMessage": error_message,
                    "stackTrace": stack_trace[:5000],
                    "category": category,
                    "confidence": confidence,
                    "sourceFile": str(json_file.relative_to(self.results_dir.parent.parent.parent))
                }
                
                self.failures.append(failure_data)
            elif status == "skipped":
                self.results["skipped"] += 1
                self.results["total"] += 1
    
    def _extract_service_name(self, xml_file: Path) -> str:
        """Extract service name from file path"""
        parts = xml_file.parts
        for i, part in enumerate(parts):
            if part in ["services", "tests"]:
                if i + 1 < len(parts):
                    return parts[i + 1]
        return "unknown"
    
    def _categorize_failure(self, error_type: str, error_message: str, stack_trace: str) -> str:
        """Categorize failure type"""
        error_lower = error_type.lower()
        message_lower = error_message.lower() if error_message else ""
        stack_lower = stack_trace.lower() if stack_trace else ""
        
        # Compilation errors
        if any(keyword in error_lower for keyword in ["compilation", "syntax", "cannot find symbol", "package does not exist"]):
            return "compilation"
        
        # Null pointer
        if "nullpointerexception" in error_lower or "null" in message_lower:
            return "null-pointer"
        
        # Assertion failures
        if "assertion" in error_lower or "expected" in message_lower or "but was" in message_lower:
            return "assertion"
        
        # Timeout
        if "timeout" in error_lower or "timed out" in message_lower:
            return "timeout"
        
        # Network/connection
        if any(keyword in message_lower for keyword in ["connection", "refused", "unreachable", "network"]):
            return "infrastructure"
        
        # Illegal argument
        if "illegalargument" in error_lower:
            return "runtime"
        
        # Default
        return "runtime"
    
    def _estimate_confidence(self, error_type: str, error_message: str) -> float:
        """Estimate confidence for auto-fix (simplified - will be enhanced)"""
        # High confidence for simple issues
        if "cannot find symbol" in error_message.lower() or "package" in error_message.lower():
            return 0.95
        
        if "nullpointerexception" in error_type.lower():
            return 0.85
        
        if "assertion" in error_type.lower():
            return 0.75
        
        # Medium confidence for runtime errors
        return 0.60
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate summary statistics"""
        total = self.results["total"]
        if total == 0:
            return {
                "passRate": 0.0,
                "failureRate": 0.0,
                "status": "no_tests"
            }
        
        pass_rate = (self.results["passed"] / total) * 100
        failure_rate = (self.results["failed"] / total) * 100
        
        status = "success" if self.results["failed"] == 0 else "failure"
        
        return {
            "passRate": round(pass_rate, 2),
            "failureRate": round(failure_rate, 2),
            "status": status,
            "failureCount": len(self.failures)
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: qa-result-parser.py <results-directory> [output-file]")
        sys.exit(1)
    
    results_dir = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    parser = TestResultParser(results_dir)
    parsed_results = parser.parse()
    
    # Add metadata
    output = {
        "testRun": {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "resultsDirectory": results_dir,
            "parserVersion": "1.0.0"
        },
        "results": parsed_results["results"],
        "failures": parsed_results["failures"],
        "summary": parsed_results["summary"]
    }
    
    # Output JSON
    json_output = json.dumps(output, indent=2)
    
    if output_file:
        with open(output_file, 'w') as f:
            f.write(json_output)
        print(f"[PARSER] Results written to: {output_file}")
    else:
        print(json_output)
    
    # Print summary
    summary = parsed_results["summary"]
    print(f"\n[PARSER] Summary:")
    print(f"  Total: {output['results']['total']}")
    print(f"  Passed: {output['results']['passed']}")
    print(f"  Failed: {output['results']['failed']}")
    print(f"  Pass Rate: {summary['passRate']}%")
    print(f"  Failures: {len(output['failures'])}")


if __name__ == "__main__":
    main()

