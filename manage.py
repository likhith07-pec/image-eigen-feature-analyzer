"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

# 1. Automatically load .env if present so user never has to configure environment variables
base_dir = Path(__file__).resolve().parent
env_path = base_dir / '.env'
if env_path.exists():
    try:
        for line in env_path.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))
    except Exception:
        pass

# 2. If running under an interpreter other than Python 3.13 (e.g. system msys64 Python),
# re-execute transparently with the Python 3.13 installation that has Django and NumPy
if sys.version_info[:2] != (3, 13):
    import subprocess
    py313_path = Path.home() / 'AppData' / 'Local' / 'Programs' / 'Python' / 'Python313' / 'python.exe'
    target_cmd = [str(py313_path)] if py313_path.exists() else ['py', '-3.13']
    try:
        ret = subprocess.call(target_cmd + sys.argv)
        sys.exit(ret)
    except Exception:
        pass


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ImageEigenAnalyzer.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
