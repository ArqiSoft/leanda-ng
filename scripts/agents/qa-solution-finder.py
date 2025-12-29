#!/usr/bin/env python3
"""
Solution Finder for Autonomous Testing
Finds solutions to test failures by searching codebase and analyzing patterns
"""

import json
import sys
import re
import subprocess
from typing import Dict, List, Any, Optional
from pathlib import Path

class SolutionFinder:
    """Find solutions to test failures"""
    
    def __init__(self, repo_root: str = None):
        if repo_root:
            self.repo_root = Path(repo_root)
        else:
            # Find repo root (3 levels up from scripts/agents)
            self.repo_root = Path(__file__).parent.parent.parent
        
        self.repo_root = self.repo_root.resolve()
    
    def find_solutions(self, failures: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find solutions for all failures"""
        print(f"[SOLUTION FINDER] Finding solutions for {len(failures)} failures...")
        
        solutions = []
        for failure in failures:
            solution = self._find_solution(failure)
            # Embed failure data in solution for auto-fix to use
            solution["failure"] = failure
            solutions.append(solution)
        
        return solutions
    
    def _find_solution(self, failure: Dict[str, Any]) -> Dict[str, Any]:
        """Find solution for a single failure"""
        category = failure.get("category", "runtime")
        error_type = failure.get("errorType", "")
        error_message = failure.get("errorMessage", "")
        # Build context from failure data
        context = {
            "testClass": failure.get("className", ""),
            "testMethod": failure.get("testName", ""),
            "service": failure.get("service", ""),
            "sourceFile": failure.get("sourceFile", failure.get("file", ""))
        }
        # Merge with any existing context
        if failure.get("context"):
            context.update(failure.get("context", {}))
        
        solution = {
            "failureId": failure.get("id"),
            "suggestedFixes": [],
            "confidence": failure.get("confidence", 0.0),
            "strategy": failure.get("fixStrategy", "")
        }
        
        # Find solutions based on category
        if category == "compilation":
            fixes = self._find_compilation_fixes(failure, context)
        elif category == "null-pointer":
            fixes = self._find_null_pointer_fixes(failure, context)
        elif category == "assertion":
            fixes = self._find_assertion_fixes(failure, context)
        elif category == "timeout":
            fixes = self._find_timeout_fixes(failure, context)
        else:
            fixes = self._find_generic_fixes(failure, context)
        
        solution["suggestedFixes"] = fixes
        
        # Update confidence based on found solutions
        if fixes:
            # Increase confidence if we found specific fixes
            max_fix_confidence = max(f.get("confidence", 0.0) for f in fixes)
            solution["confidence"] = min(1.0, failure.get("confidence", 0.0) + (max_fix_confidence * 0.1))
        
        return solution
    
    def _find_compilation_fixes(self, failure: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find fixes for compilation errors"""
        fixes = []
        error_message = failure.get("errorMessage", "")
        stack_trace = failure.get("stackTrace", "")
        test_class = context.get("testClass", "")
        service = context.get("service", "")
        
        # Missing import
        import_match = re.search(r"cannot find symbol.*?class (\w+)", error_message, re.IGNORECASE)
        if import_match:
            class_name = import_match.group(1)
            # Search for where this class is used
            import_path = self._find_import_path(class_name, service)
            if import_path:
                fixes.append({
                    "type": "add_import",
                    "description": f"Add missing import: {import_path}",
                    "file": context.get("sourceFile", ""),
                    "change": f"import {import_path};",
                    "confidence": 0.95,
                    "location": "top_of_file"
                })
        
        # Package does not exist - check both error_message and stackTrace
        package_match = re.search(r"package (\S+) does not exist", error_message, re.IGNORECASE)
        if not package_match:
            # Try stackTrace if not found in error_message
            package_match = re.search(r"package (\S+) does not exist", stack_trace, re.IGNORECASE)
        if package_match:
            package_name = package_match.group(1)
            # Extract file path from error message or context
            file_path = context.get("sourceFile", "")
            if not file_path and "file" in failure:
                file_path = failure.get("file", "")
            
            # If it's a shared models package, add dependency to POM
            if "io.leanda.ng.shared" in package_name:
                # Find the service's pom.xml
                if service and service != "unknown" and service != "build":
                    pom_path = self.repo_root / "services" / service / "pom.xml"
                    if pom_path.exists():
                        fixes.append({
                            "type": "add_dependency",
                            "description": f"Add shared-models dependency to {service}",
                            "file": f"services/{service}/pom.xml",
                            "change": f'    <dependency>\n      <groupId>io.leanda.ng</groupId>\n      <artifactId>shared-models</artifactId>\n      <version>1.0.0-SNAPSHOT</version>\n    </dependency>',
                            "confidence": 0.95,
                            "location": "dependencies_section"
                        })
                    else:
                        # Try to extract service from file path
                        if file_path and "services/" in file_path:
                            service_from_path = file_path.split("services/")[1].split("/")[0]
                            pom_path = self.repo_root / "services" / service_from_path / "pom.xml"
                            if pom_path.exists():
                                fixes.append({
                                    "type": "add_dependency",
                                    "description": f"Add shared-models dependency to {service_from_path}",
                                    "file": f"services/{service_from_path}/pom.xml",
                                    "change": f'    <dependency>\n      <groupId>io.leanda.ng</groupId>\n      <artifactId>shared-models</artifactId>\n      <version>1.0.0-SNAPSHOT</version>\n    </dependency>',
                                    "confidence": 0.95,
                                    "location": "dependencies_section"
                                })
            
            # Also suggest fixing the import
            if file_path:
                fixes.append({
                    "type": "fix_import",
                    "description": f"Fix import for package: {package_name}",
                    "file": file_path,
                    "change": f"Ensure import statement matches package: {package_name}",
                    "confidence": 0.90,
                    "location": "imports_section"
                })
            else:
                # Try to extract service from error message or failure data
                error_details = failure.get("details", "")
                if "services/" in error_details:
                    service_match = re.search(r'services/([^/]+)/', error_details)
                    if service_match:
                        service_from_error = service_match.group(1)
                        pom_path = self.repo_root / "services" / service_from_error / "pom.xml"
                        if pom_path.exists() and "io.leanda.ng.shared" in package_name:
                            fixes.append({
                                "type": "add_dependency",
                                "description": f"Add shared-models dependency to {service_from_error}",
                                "file": f"services/{service_from_error}/pom.xml",
                                "change": f'    <dependency>\n      <groupId>io.leanda.ng</groupId>\n      <artifactId>shared-models</artifactId>\n      <version>1.0.0-SNAPSHOT</version>\n    </dependency>',
                                "confidence": 0.95,
                                "location": "dependencies_section"
                            })
                
                # Fallback fix
                if not fixes:
                    fixes.append({
                        "type": "fix_package",
                        "description": f"Fix package declaration or add dependency for: {package_name}",
                        "file": file_path if file_path else "",
                        "change": f"Check package declaration matches directory structure or add dependency",
                        "confidence": 0.90,
                        "location": "package_declaration"
                    })
        
        return fixes
    
    def _find_null_pointer_fixes(self, failure: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find fixes for null pointer exceptions"""
        fixes = []
        stack_trace = failure.get("stackTrace", "")
        test_method = context.get("testMethod", "")
        
        # Extract variable name from stack trace
        npe_match = re.search(r"NullPointerException.*?(\w+)\.", stack_trace)
        if npe_match:
            var_name = npe_match.group(1)
            fixes.append({
                "type": "add_null_check",
                "description": f"Add null check for variable: {var_name}",
                "file": context.get("sourceFile", ""),
                "change": f"if ({var_name} == null) {{ /* handle null case */ }}",
                "confidence": 0.80,
                "location": f"before_{var_name}_usage"
            })
        
        # Check if it's a test data issue
        if "test" in test_method.lower():
            fixes.append({
                "type": "initialize_test_data",
                "description": "Initialize test data before use",
                "file": context.get("sourceFile", ""),
                "change": "Ensure all test data is properly initialized in @BeforeEach",
                "confidence": 0.75,
                "location": "test_setup"
            })
        
        return fixes
    
    def _find_assertion_fixes(self, failure: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find fixes for assertion failures"""
        fixes = []
        error_message = failure.get("errorMessage", "")
        
        # Expected vs actual
        expected_match = re.search(r"expected:\s*<(.+?)>\s*but was:\s*<(.+?)>", error_message, re.IGNORECASE)
        if expected_match:
            expected = expected_match.group(1)
            actual = expected_match.group(2)
            fixes.append({
                "type": "fix_assertion",
                "description": f"Fix assertion: expected {expected}, got {actual}",
                "file": context.get("sourceFile", ""),
                "change": f"Update assertion to match actual value or fix test data",
                "confidence": 0.70,
                "location": "assertion_line"
            })
        
        return fixes
    
    def _find_timeout_fixes(self, failure: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find fixes for timeout errors"""
        fixes = []
        
        fixes.append({
            "type": "increase_timeout",
            "description": "Increase test timeout",
            "file": context.get("sourceFile", ""),
            "change": "Add @Timeout annotation or increase timeout in test configuration",
            "confidence": 0.65,
            "location": "test_method"
        })
        
        fixes.append({
            "type": "optimize_test",
            "description": "Optimize test performance",
            "file": context.get("sourceFile", ""),
            "change": "Review test for performance bottlenecks",
            "confidence": 0.60,
            "location": "test_method"
        })
        
        return fixes
    
    def _find_generic_fixes(self, failure: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find generic fixes for unknown error types"""
        fixes = []
        
        # Search codebase for similar patterns
        test_class = context.get("testClass", "")
        if test_class:
            similar_tests = self._find_similar_tests(test_class, context.get("service", ""))
            if similar_tests:
                fixes.append({
                    "type": "pattern_match",
                    "description": f"Found {len(similar_tests)} similar tests - review for patterns",
                    "file": context.get("sourceFile", ""),
                    "change": "Apply patterns from similar tests",
                    "confidence": 0.60,
                    "location": "test_class"
                })
        
        return fixes
    
    def _find_import_path(self, class_name: str, service: str) -> Optional[str]:
        """Find import path for a class"""
        # Search in service directory
        service_dir = self.repo_root / "services" / service
        if not service_dir.exists():
            return None
        
        # Search for class file
        for java_file in service_dir.rglob("*.java"):
            if java_file.stem == class_name:
                # Extract package from file
                relative_path = java_file.relative_to(service_dir / "src" / "main" / "java")
                package_path = str(relative_path.parent).replace("/", ".").replace("\\", ".")
                return f"{package_path}.{class_name}"
        
        # Check shared models
        shared_dir = self.repo_root / "shared" / "models"
        for java_file in shared_dir.rglob("*.java"):
            if java_file.stem == class_name:
                return f"io.leanda.ng.shared.models.{class_name}"
        
        return None
    
    def _find_similar_tests(self, test_class: str, service: str) -> List[str]:
        """Find similar test classes"""
        similar = []
        service_dir = self.repo_root / "services" / service
        
        if not service_dir.exists():
            return similar
        
        test_dir = service_dir / "src" / "test"
        if not test_dir.exists():
            return similar
        
        # Find tests with similar names
        for test_file in test_dir.rglob("*Test.java"):
            if test_class.lower() in test_file.stem.lower() or test_file.stem.lower() in test_class.lower():
                similar.append(str(test_file.relative_to(self.repo_root)))
        
        return similar


def main():
    """CLI for solution finder"""
    if len(sys.argv) < 2:
        print("Usage: qa-solution-finder.py <failures-analysis.json> [output-file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Load analysis
    with open(input_file, 'r') as f:
        analysis = json.load(f)
    
    failures = analysis.get("failures", [])
    
    if not failures:
        print("[SOLUTION FINDER] No failures to analyze")
        sys.exit(0)
    
    # Find solutions
    finder = SolutionFinder()
    solutions = finder.find_solutions(failures)
    
    # Combine with original failures
    output = {
        "failures": failures,
        "solutions": solutions,
        "summary": {
            "totalFailures": len(failures),
            "failuresWithSolutions": len([s for s in solutions if s.get("suggestedFixes")]),
            "totalFixes": sum(len(s.get("suggestedFixes", [])) for s in solutions)
        }
    }
    
    # Output
    json_output = json.dumps(output, indent=2)
    
    if output_file:
        with open(output_file, 'w') as f:
            f.write(json_output)
        print(f"[SOLUTION FINDER] Solutions written to: {output_file}")
    else:
        print(json_output)
    
    # Print summary
    summary = output["summary"]
    print(f"\n[SOLUTION FINDER] Summary:")
    print(f"  Total failures: {summary['totalFailures']}")
    print(f"  Failures with solutions: {summary['failuresWithSolutions']}")
    print(f"  Total fixes suggested: {summary['totalFixes']}")


if __name__ == "__main__":
    main()

