#!/usr/bin/env python3
"""
Result Storage System for Autonomous Testing
Manages storage and indexing of test run results
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class ResultStorage:
    """Manage test result storage and indexing"""
    
    def __init__(self, base_dir: str = None):
        if base_dir:
            self.base_dir = Path(base_dir)
        else:
            # Default to docs/testing/autonomous-runs
            repo_root = Path(__file__).parent.parent.parent
            self.base_dir = repo_root / "docs" / "testing" / "autonomous-runs"
        
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.base_dir / "index.json"
        self._load_index()
    
    def _load_index(self):
        """Load or create index file"""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r') as f:
                    self.index = json.load(f)
            except:
                self.index = {"runs": [], "lastUpdated": None}
        else:
            self.index = {"runs": [], "lastUpdated": None}
    
    def _save_index(self):
        """Save index file"""
        self.index["lastUpdated"] = datetime.utcnow().isoformat() + "Z"
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f, indent=2)
    
    def create_run_directory(self, run_id: str) -> Path:
        """Create directory for a test run"""
        run_dir = self.base_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        return run_dir
    
    def store_results(self, run_id: str, results: Dict[str, Any]) -> Path:
        """Store test results for a run"""
        run_dir = self.create_run_directory(run_id)
        
        # Store test results
        results_file = run_dir / "test-results.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Update index
        run_entry = {
            "runId": run_id,
            "timestamp": results.get("testRun", {}).get("timestamp", datetime.utcnow().isoformat() + "Z"),
            "testType": results.get("testRun", {}).get("type", "unknown"),
            "status": results.get("summary", {}).get("status", "unknown"),
            "passRate": results.get("summary", {}).get("passRate", 0.0),
            "failureCount": results.get("summary", {}).get("failureCount", 0),
            "totalTests": results.get("results", {}).get("total", 0),
            "directory": str(run_dir.relative_to(self.base_dir.parent.parent.parent))
        }
        
        # Add to index (prepend to keep recent first)
        self.index["runs"].insert(0, run_entry)
        
        # Keep only last 100 runs in index
        if len(self.index["runs"]) > 100:
            self.index["runs"] = self.index["runs"][:100]
        
        self._save_index()
        
        return run_dir
    
    def store_analysis(self, run_id: str, analysis: Dict[str, Any]) -> Path:
        """Store failure analysis"""
        run_dir = self.base_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        
        analysis_file = run_dir / "failures-analysis.json"
        with open(analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        return analysis_file
    
    def store_fixes(self, run_id: str, fixes: List[Dict[str, Any]]) -> Path:
        """Store applied fixes"""
        run_dir = self.base_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        
        fixes_file = run_dir / "fixes-applied.json"
        with open(fixes_file, 'w') as f:
            json.dump({"fixes": fixes, "count": len(fixes)}, f, indent=2)
        
        return fixes_file
    
    def store_progress(self, run_id: str, progress: List[Dict[str, Any]]) -> Path:
        """Store progress log"""
        run_dir = self.base_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        
        progress_file = run_dir / "progress-log.json"
        with open(progress_file, 'w') as f:
            json.dump({"iterations": progress, "count": len(progress)}, f, indent=2)
        
        return progress_file
    
    def store_report(self, run_id: str, report: str) -> Path:
        """Store human-readable report"""
        run_dir = self.base_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        
        report_file = run_dir / "final-report.md"
        with open(report_file, 'w') as f:
            f.write(report)
        
        return report_file
    
    def store_pr_description(self, run_id: str, pr_description: str) -> Path:
        """Store PR description"""
        run_dir = self.base_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        
        pr_file = run_dir / "pr-description.md"
        with open(pr_file, 'w') as f:
            f.write(pr_description)
        
        return pr_file
    
    def get_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Get run information from index"""
        for run in self.index["runs"]:
            if run["runId"] == run_id:
                return run
        return None
    
    def list_runs(self, limit: int = 10) -> List[Dict[str, Any]]:
        """List recent runs"""
        return self.index["runs"][:limit]


def main():
    """CLI for storage operations"""
    if len(sys.argv) < 2:
        print("Usage: qa-storage.py <command> [args...]")
        print("Commands:")
        print("  create <run-id>  - Create run directory")
        print("  store <run-id> <file> <data> - Store data")
        print("  list [limit] - List recent runs")
        sys.exit(1)
    
    command = sys.argv[1]
    storage = ResultStorage()
    
    if command == "create":
        if len(sys.argv) < 3:
            print("Usage: qa-storage.py create <run-id>")
            sys.exit(1)
        run_id = sys.argv[2]
        run_dir = storage.create_run_directory(run_id)
        print(f"Created run directory: {run_dir}")
    
    elif command == "list":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        runs = storage.list_runs(limit)
        print(json.dumps(runs, indent=2))
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()

