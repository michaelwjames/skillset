import argparse
import os
from radon.complexity import cc_visit
from radon.maintainability import mi_visit

def analyze_codebase(path):
    """
    Analyzes a Python codebase and suggests improvements.
    """
    if not os.path.exists(path):
        print(f"Error: Path not found at {path}")
        return

    print(f"Analyzing codebase at {path}...")

    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    code = f.read()

                # Cyclomatic Complexity Analysis
                cc_results = cc_visit(code)
                for result in cc_results:
                    if result.complexity > 10:
                        print(f"  - High Cyclomatic Complexity in {filepath} -> {result.name}: {result.complexity} (Consider refactoring)")

                # Maintainability Index Analysis
                mi_result = mi_visit(code, True)
                if mi_result < 20:
                    print(f"  - Low Maintainability Index in {filepath}: {mi_result:.2f} (Consider refactoring)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze a Python codebase and suggest improvements.")
    parser.add_argument("path", help="The path to the Python codebase to analyze.")
    args = parser.parse_args()

    analyze_codebase(args.path)
