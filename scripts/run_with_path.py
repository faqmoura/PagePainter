import os
import sys
import subprocess

def run_script(script_name):
    """Run a Python script with the correct Python path"""
    # Get absolute paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    # Add project root to Python path
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    # Run the script
    script_path = os.path.join(current_dir, script_name)
    print(f"Running {script_path} with PYTHONPATH={project_root}")
    
    env = os.environ.copy()
    env["PYTHONPATH"] = project_root
    
    subprocess.run([sys.executable, script_path], env=env)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python run_with_path.py <script_name>")
        print("Example: python run_with_path.py create_book_pdf.py")
        sys.exit(1)
    
    run_script(sys.argv[1])
