#!/usr/bin/env python3
"""
Problem Analyzer for Autonomous Testing
Analyzes test failures, categorizes issues, and calculates confidence scores
"""

import json
import sys
import re
from typing import Dict, List, Any
from pathlib import Path

class ProblemAnalyzer:
    """Analyze test failures and categorize problems"""
    
    def __init__(self):
        self.categories = {
            "compilation": {
                "keywords": ["compilation", "syntax", "cannot find symbol", "package does not exist", 
                            "import", "cannot resolve", "unresolved reference"],
                "confidence_base": 0.95
            },
            "null-pointer": {
                "keywords": ["nullpointerexception", "null", "NPE"],
                "confidence_base": 0.85
            },
            "assertion": {
                "keywords": ["assertion", "expected", "but was", "assertEquals", "assertTrue", "assertFalse"],
                "confidence_base": 0.75
            },
            "timeout": {
                "keywords": ["timeout", "timed out", "deadline exceeded", "execution timeout"],
                "confidence_base": 0.70
            },
            "infrastructure": {
                "keywords": ["connection", "refused", "unreachable", "network", "docker", "container", 
                           "kafka", "mongodb", "opensearch"],
                "confidence_base": 0.60
            },
            "runtime": {
                "keywords": ["illegalargument", "illegalstate", "indexoutofbounds", "classcastexception"],
                "confidence_base": 0.65
            },
            "flaky": {
                "keywords": ["intermittent", "sometimes", "race condition", "timing"],
                "confidence_base": 0.50
            }
        }
    
    def analyze(self, failures: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze all failures"""
        print(f"[ANALYZER] Analyzing {len(failures)} failures...")
        
        analyzed_failures = []
        category_counts = {}
        confidence_scores = []
        
        for failure in failures:
            analyzed = self._analyze_failure(failure)
            analyzed_failures.append(analyzed)
            
            # Count categories
            category = analyzed["category"]
            category_counts[category] = category_counts.get(category, 0) + 1
            
            # Track confidence
            confidence_scores.append(analyzed["confidence"])
        
        # Calculate statistics
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
        
        # Prioritize failures
        prioritized = self._prioritize_failures(analyzed_failures)
        
        return {
            "failures": prioritized,
            "statistics": {
                "total": len(analyzed_failures),
                "byCategory": category_counts,
                "averageConfidence": round(avg_confidence, 2),
                "highConfidence": len([f for f in analyzed_failures if f["confidence"] > 0.90]),
                "mediumConfidence": len([f for f in analyzed_failures if 0.70 <= f["confidence"] <= 0.90]),
                "lowConfidence": len([f for f in analyzed_failures if f["confidence"] < 0.70])
            },
            "recommendations": self._generate_recommendations(prioritized)
        }
    
    def _analyze_failure(self, failure: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single failure"""
        error_type = failure.get("errorType", "").lower()
        error_message = failure.get("errorMessage", "").lower()
        stack_trace = failure.get("stackTrace", "").lower()
        
        # Determine category
        category = self._categorize(error_type, error_message, stack_trace)
        
        # Calculate confidence
        confidence = self._calculate_confidence(failure, category)
        
        # Suggest fix strategy
        fix_strategy = self._suggest_fix_strategy(category, error_type, error_message)
        
        # Extract additional context
        context = self._extract_context(failure)
        
        return {
            **failure,
            "category": category,
            "confidence": confidence,
            "fixStrategy": fix_strategy,
            "context": context,
            "priority": self._calculate_priority(category, confidence)
        }
    
    def _categorize(self, error_type: str, error_message: str, stack_trace: str) -> str:
        """Categorize failure type"""
        combined_text = f"{error_type} {error_message} {stack_trace}"
        
        # Check each category
        best_match = "runtime"  # Default
        best_score = 0
        
        for category, config in self.categories.items():
            score = sum(1 for keyword in config["keywords"] if keyword in combined_text)
            if score > best_score:
                best_score = score
                best_match = category
        
        return best_match
    
    def _calculate_confidence(self, failure: Dict[str, Any], category: str) -> float:
        """Calculate confidence score for auto-fix"""
        base_confidence = self.categories.get(category, {}).get("confidence_base", 0.60)
        
        error_type = failure.get("errorType", "").lower()
        error_message = failure.get("errorMessage", "").lower()
        
        # Adjust based on error characteristics
        adjustments = 0.0
        
        # High confidence indicators
        if "cannot find symbol" in error_message:
            adjustments += 0.10
        if "package" in error_message and "does not exist" in error_message:
            adjustments += 0.10
        if "import" in error_message:
            adjustments += 0.05
        
        # Low confidence indicators
        if len(error_message) > 500:  # Complex error messages
            adjustments -= 0.10
        if "unknown" in error_type:
            adjustments -= 0.15
        if failure.get("stackTrace", "").count("\n") > 50:  # Deep stack traces
            adjustments -= 0.10
        
        confidence = min(1.0, max(0.0, base_confidence + adjustments))
        return round(confidence, 2)
    
    def _suggest_fix_strategy(self, category: str, error_type: str, error_message: str) -> str:
        """Suggest fix strategy based on category"""
        strategies = {
            "compilation": "Add missing imports or fix syntax errors",
            "null-pointer": "Add null checks or initialize variables",
            "assertion": "Fix test expectations or update test data",
            "timeout": "Increase timeout or optimize test performance",
            "infrastructure": "Check service health or network connectivity",
            "runtime": "Fix logic errors or validate inputs",
            "flaky": "Add retries or fix race conditions"
        }
        
        return strategies.get(category, "Review error and apply appropriate fix")
    
    def _extract_context(self, failure: Dict[str, Any]) -> Dict[str, Any]:
        """Extract additional context from failure"""
        context = {
            "service": failure.get("service", "unknown"),
            "testClass": failure.get("testClass", "unknown"),
            "testMethod": failure.get("testMethod", "unknown")
        }
        
        # Extract file path if available
        source_file = failure.get("sourceFile", "")
        if source_file:
            context["sourceFile"] = source_file
        
        # Extract line numbers from stack trace if available
        stack_trace = failure.get("stackTrace", "")
        line_numbers = re.findall(r'\(.*?\.java:(\d+)\)', stack_trace)
        if line_numbers:
            context["suggestedLine"] = int(line_numbers[0])
        
        return context
    
    def _calculate_priority(self, category: str, confidence: float) -> int:
        """Calculate priority (1 = highest, 5 = lowest)"""
        # High priority: compilation errors, high confidence
        if category == "compilation" and confidence > 0.90:
            return 1
        
        # Medium-high: null pointer, assertion with high confidence
        if category in ["null-pointer", "assertion"] and confidence > 0.80:
            return 2
        
        # Medium: runtime errors with medium confidence
        if confidence > 0.70:
            return 3
        
        # Low: infrastructure, flaky, low confidence
        if category in ["infrastructure", "flaky"] or confidence < 0.60:
            return 5
        
        return 4
    
    def _prioritize_failures(self, failures: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sort failures by priority"""
        return sorted(failures, key=lambda f: (
            f.get("priority", 5),
            -f.get("confidence", 0.0)  # Higher confidence first within same priority
        ))
    
    def _generate_recommendations(self, failures: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        # Count by category
        category_counts = {}
        for failure in failures:
            category = failure.get("category", "unknown")
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # High confidence fixes
        high_confidence = [f for f in failures if f.get("confidence", 0) > 0.90]
        if high_confidence:
            recommendations.append(
                f"Found {len(high_confidence)} failures with high confidence (>90%) - good candidates for auto-fix"
            )
        
        # Compilation errors
        if category_counts.get("compilation", 0) > 0:
            recommendations.append(
                f"Found {category_counts['compilation']} compilation errors - should be fixed first"
            )
        
        # Infrastructure issues
        if category_counts.get("infrastructure", 0) > 0:
            recommendations.append(
                f"Found {category_counts['infrastructure']} infrastructure issues - may require manual intervention"
            )
        
        # Flaky tests
        if category_counts.get("flaky", 0) > 0:
            recommendations.append(
                f"Found {category_counts['flaky']} potentially flaky tests - consider adding retries"
            )
        
        return recommendations


def main():
    """CLI for problem analyzer"""
    if len(sys.argv) < 2:
        print("Usage: qa-problem-analyzer.py <test-results.json> [output-file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Load test results
    with open(input_file, 'r') as f:
        test_results = json.load(f)
    
    failures = test_results.get("failures", [])
    
    if not failures:
        print("[ANALYZER] No failures to analyze")
        sys.exit(0)
    
    # Analyze
    analyzer = ProblemAnalyzer()
    analysis = analyzer.analyze(failures)
    
    # Output
    json_output = json.dumps(analysis, indent=2)
    
    if output_file:
        with open(output_file, 'w') as f:
            f.write(json_output)
        print(f"[ANALYZER] Analysis written to: {output_file}")
    else:
        print(json_output)
    
    # Print summary
    stats = analysis["statistics"]
    print(f"\n[ANALYZER] Summary:")
    print(f"  Total failures: {stats['total']}")
    print(f"  High confidence: {stats['highConfidence']}")
    print(f"  Medium confidence: {stats['mediumConfidence']}")
    print(f"  Low confidence: {stats['lowConfidence']}")
    print(f"  Average confidence: {stats['averageConfidence']}")


if __name__ == "__main__":
    main()

