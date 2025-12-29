#!/usr/bin/env python3
"""
Progress Tracker for Autonomous Testing
Tracks fix attempts and detects no-progress scenarios
"""

import json
import sys
from typing import Dict, List, Any
from datetime import datetime

class ProgressTracker:
    """Track progress of test fixes"""
    
    def __init__(self, max_iterations: int = 10, no_progress_threshold: int = 3):
        self.max_iterations = max_iterations
        self.no_progress_threshold = no_progress_threshold
        self.iterations = []
    
    def add_iteration(self, iteration_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add an iteration and check progress"""
        iteration_num = len(self.iterations) + 1
        
        iteration = {
            "iteration": iteration_num,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            **iteration_data
        }
        
        self.iterations.append(iteration)
        
        # Check progress
        progress_status = self._check_progress()
        
        return {
            "iteration": iteration,
            "progress": progress_status,
            "shouldContinue": self._should_continue(progress_status)
        }
    
    def _check_progress(self) -> Dict[str, Any]:
        """Check if progress is being made"""
        if len(self.iterations) < 2:
            return {
                "status": "initial",
                "message": "First iteration - no comparison yet"
            }
        
        current = self.iterations[-1]
        previous = self.iterations[-2]
        
        current_failures = current.get("failureCount", 0)
        previous_failures = previous.get("failureCount", 0)
        
        if current_failures < previous_failures:
            return {
                "status": "improving",
                "message": f"Failures decreased from {previous_failures} to {current_failures}",
                "improvement": previous_failures - current_failures
            }
        elif current_failures > previous_failures:
            return {
                "status": "regressing",
                "message": f"Failures increased from {previous_failures} to {current_failures}",
                "regression": current_failures - previous_failures
            }
        else:
            return {
                "status": "no_change",
                "message": f"Failures unchanged at {current_failures}"
            }
    
    def _should_continue(self, progress_status: Dict[str, Any]) -> bool:
        """Determine if iteration should continue"""
        # Check max iterations
        if len(self.iterations) >= self.max_iterations:
            return False
        
        # Check no-progress threshold
        if len(self.iterations) < self.no_progress_threshold:
            return True
        
        # Check last N iterations for no progress
        recent_iterations = self.iterations[-self.no_progress_threshold:]
        failure_counts = [it.get("failureCount", 0) for it in recent_iterations]
        
        # If all recent iterations have same failure count, stop
        if len(set(failure_counts)) == 1 and failure_counts[0] > 0:
            return False
        
        # If regressing, stop
        if progress_status.get("status") == "regressing":
            return False
        
        return True
    
    def get_summary(self) -> Dict[str, Any]:
        """Get progress summary"""
        if not self.iterations:
            return {
                "iterations": 0,
                "status": "no_iterations"
            }
        
        initial_failures = self.iterations[0].get("failureCount", 0)
        current_failures = self.iterations[-1].get("failureCount", 0)
        improvement = initial_failures - current_failures
        
        # Count improvements
        improvements = 0
        regressions = 0
        no_changes = 0
        
        for i in range(1, len(self.iterations)):
            prev = self.iterations[i-1].get("failureCount", 0)
            curr = self.iterations[i].get("failureCount", 0)
            if curr < prev:
                improvements += 1
            elif curr > prev:
                regressions += 1
            else:
                no_changes += 1
        
        return {
            "iterations": len(self.iterations),
            "initialFailures": initial_failures,
            "currentFailures": current_failures,
            "totalImprovement": improvement,
            "improvementRate": round(improvement / initial_failures * 100, 2) if initial_failures > 0 else 0,
            "improvements": improvements,
            "regressions": regressions,
            "noChanges": no_changes,
            "status": "success" if current_failures == 0 else "in_progress" if improvement > 0 else "stalled"
        }


def main():
    """CLI for progress tracker"""
    if len(sys.argv) < 2:
        print("Usage: qa-progress-tracker.py <command> [args...]")
        print("Commands:")
        print("  add <iteration-data.json> - Add iteration")
        print("  summary - Show summary")
        sys.exit(1)
    
    command = sys.argv[1]
    tracker = ProgressTracker()
    
    if command == "add":
        if len(sys.argv) < 3:
            print("Usage: qa-progress-tracker.py add <iteration-data.json>")
            sys.exit(1)
        
        # Support reading from stdin if '-' is provided
        if sys.argv[2] == "-":
            iteration_data = json.load(sys.stdin)
        else:
            with open(sys.argv[2], 'r') as f:
                iteration_data = json.load(f)
        
        result = tracker.add_iteration(iteration_data)
        print(json.dumps(result, indent=2))
        
        if not result["shouldContinue"]:
            print("\n[PROGRESS TRACKER] Should stop iteration")
            sys.exit(2)  # Exit with code 2 to signal stop
    
    elif command == "summary":
        # Load existing iterations if available
        if len(sys.argv) > 2:
            with open(sys.argv[2], 'r') as f:
                data = json.load(f)
                tracker.iterations = data.get("iterations", [])
        
        summary = tracker.get_summary()
        print(json.dumps(summary, indent=2))
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()

