#!/usr/bin/env python3
"""
Agent Dependency Analysis - Usage Example

This script demonstrates how to use the agent dependency analysis results
to plan and execute agent fixes in the correct order.
"""

import json
from pathlib import Path
from typing import List, Dict


def load_analysis_report(report_path: str = "agent_dependency_analysis.json") -> Dict:
    """Load the dependency analysis report."""
    with open(report_path, 'r') as f:
        return json.load(f)


def print_fix_priority_list(report: Dict):
    """Print agents in the order they should be fixed."""
    print("\n" + "=" * 70)
    print("AGENT FIX PRIORITY LIST")
    print("=" * 70)
    
    # Phase 1: Level 0 - Independent agents
    print("\n📌 PHASE 1: Independent Agents (Fix First)")
    print("-" * 70)
    if report['level_0_agents']:
        for i, agent in enumerate(sorted(report['level_0_agents']), 1):
            deps = report['detailed_dependencies'][agent]
            print(f"{i}. {agent}")
            print(f"   - Internal dependencies: {deps['internal_count']}")
            print(f"   - External dependencies: {deps['external_count']}")
            if deps['external_dependencies']:
                ext_deps = deps['external_dependencies'][:5]  # Show first 5
                print(f"   - Key external libs: {', '.join(ext_deps)}")
    else:
        print("   ✅ No Level 0 agents - all agents have dependencies!")
    
    # Phase 2: Level 1 - Minimal dependencies
    print("\n📌 PHASE 2: Minimal Dependencies (Fix After Level 0)")
    print("-" * 70)
    if report['level_1_agents']:
        for i, agent in enumerate(sorted(report['level_1_agents']), 1):
            deps = report['detailed_dependencies'][agent]
            print(f"{i}. {agent}")
            print(f"   - Internal dependencies: {', '.join(deps['internal_dependencies'])}")
    else:
        print("   No Level 1 agents")
    
    # Phase 3: Level 2 - Moderate dependencies
    print("\n📌 PHASE 3: Moderate Dependencies")
    print("-" * 70)
    if report['level_2_agents']:
        for i, agent in enumerate(sorted(report['level_2_agents']), 1):
            deps = report['detailed_dependencies'][agent]
            print(f"{i}. {agent}")
            print(f"   - Internal dependencies: {', '.join(deps['internal_dependencies'])}")
    else:
        print("   No Level 2 agents")
    
    # Phase 4: Level 3 - Complex dependencies
    print("\n📌 PHASE 4: Complex Dependencies (Fix Last)")
    print("-" * 70)
    if report['level_3_agents']:
        for i, agent in enumerate(sorted(report['level_3_agents']), 1):
            deps = report['detailed_dependencies'][agent]
            print(f"{i}. {agent}")
            print(f"   - Internal dependencies ({len(deps['internal_dependencies'])}): {', '.join(deps['internal_dependencies'][:3])}{'...' if len(deps['internal_dependencies']) > 3 else ''}")
    else:
        print("   ✅ No Level 3 agents - no complex dependencies!")


def find_agents_by_dependency(report: Dict, dependency: str) -> List[str]:
    """Find all agents that depend on a specific module."""
    dependent_agents = []
    
    for agent, info in report['detailed_dependencies'].items():
        # Check if the dependency is in the internal dependencies
        for dep in info['internal_dependencies']:
            if dependency in dep:
                dependent_agents.append(agent)
                break
    
    return sorted(dependent_agents)


def show_dependency_chain(report: Dict):
    """Show which agents depend on base_agent (or other core modules)."""
    print("\n" + "=" * 70)
    print("DEPENDENCY CHAINS")
    print("=" * 70)
    
    # Key modules to check
    key_modules = ['base_agent', 'shared', 'agent_communicator', 'enhanced_base_agent']
    
    for module in key_modules:
        dependent = find_agents_by_dependency(report, module)
        if dependent:
            print(f"\n📦 Agents depending on '{module}': {len(dependent)}")
            for agent in dependent[:5]:  # Show first 5
                print(f"   - {agent}")
            if len(dependent) > 5:
                print(f"   ... and {len(dependent) - 5} more")


def estimate_fix_effort(report: Dict):
    """Estimate the effort required to fix all agents."""
    print("\n" + "=" * 70)
    print("FIX EFFORT ESTIMATION")
    print("=" * 70)
    
    summary = report['summary']
    
    # Rough estimates based on complexity
    level_0_hours = summary['level_0_independent'] * 2  # 2 hours each
    level_1_hours = summary['level_1_minimal'] * 3      # 3 hours each
    level_2_hours = summary['level_2_moderate'] * 5     # 5 hours each
    level_3_hours = summary['level_3_complex'] * 8      # 8 hours each
    
    total_hours = level_0_hours + level_1_hours + level_2_hours + level_3_hours
    
    print(f"\nEstimated effort (assuming no major blockers):")
    print(f"  - Level 0 ({summary['level_0_independent']} agents): ~{level_0_hours} hours")
    print(f"  - Level 1 ({summary['level_1_minimal']} agents): ~{level_1_hours} hours")
    print(f"  - Level 2 ({summary['level_2_moderate']} agents): ~{level_2_hours} hours")
    print(f"  - Level 3 ({summary['level_3_complex']} agents): ~{level_3_hours} hours")
    print(f"\n  TOTAL: ~{total_hours} hours (~{total_hours / 8:.1f} working days)")
    print(f"\n  At 2-3 agents per day: ~{summary['total_agents'] / 2.5:.0f} days")


def show_summary_stats(report: Dict):
    """Show summary statistics about the agents."""
    print("\n" + "=" * 70)
    print("SUMMARY STATISTICS")
    print("=" * 70)
    
    summary = report['summary']
    
    print(f"\nTotal Agents: {summary['total_agents']}")
    print(f"\nBy Complexity Level:")
    print(f"  - Level 0 (Independent):  {summary['level_0_independent']:3d} ({summary['level_0_independent']/summary['total_agents']*100:5.1f}%)")
    print(f"  - Level 1 (Minimal):      {summary['level_1_minimal']:3d} ({summary['level_1_minimal']/summary['total_agents']*100:5.1f}%)")
    print(f"  - Level 2 (Moderate):     {summary['level_2_moderate']:3d} ({summary['level_2_moderate']/summary['total_agents']*100:5.1f}%)")
    print(f"  - Level 3 (Complex):      {summary['level_3_complex']:3d} ({summary['level_3_complex']/summary['total_agents']*100:5.1f}%)")
    
    # Calculate average dependencies
    total_internal_deps = sum(
        info['internal_count'] 
        for info in report['detailed_dependencies'].values()
    )
    avg_deps = total_internal_deps / summary['total_agents'] if summary['total_agents'] > 0 else 0
    
    print(f"\nAverage internal dependencies per agent: {avg_deps:.2f}")


def main():
    """Main entry point."""
    print("=" * 70)
    print("AGENT DEPENDENCY ANALYSIS - USAGE EXAMPLE")
    print("=" * 70)
    
    # Check if report exists
    report_path = Path("agent_dependency_analysis.json")
    if not report_path.exists():
        print(f"\n❌ Error: Report file not found: {report_path}")
        print("\nPlease run the analysis first:")
        print("  python3 analyze_agent_dependencies.py")
        return
    
    # Load the report
    print(f"\n✅ Loading report from: {report_path}")
    report = load_analysis_report(str(report_path))
    
    # Show various analyses
    show_summary_stats(report)
    print_fix_priority_list(report)
    show_dependency_chain(report)
    estimate_fix_effort(report)
    
    # Final recommendations
    print("\n" + "=" * 70)
    print("RECOMMENDED NEXT STEPS")
    print("=" * 70)
    print("""
1. Start with Level 0 agents (independent, no internal dependencies)
   - Fix ModuleNotFoundError issues
   - Fix ImportError issues
   - Test each agent individually
   
2. Once Level 0 agents pass tests, move to Level 1
   - Ensure dependencies on Level 0 are working
   - Apply the same fix patterns
   
3. Continue through levels sequentially
   - Don't skip ahead to higher levels
   - Document patterns that work
   
4. Track progress
   - Mark agents as fixed in a tracking sheet
   - Re-run analysis periodically to verify
   - Celebrate small wins!

5. Common fixes needed:
   - Update import paths (from X import Y -> from .X import Y)
   - Add __init__.py files if needed
   - Fix circular dependencies with lazy imports
   - Add missing default values in Pydantic models
""")


if __name__ == "__main__":
    main()
