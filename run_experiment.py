"""
Executa o experimento Stroop.
Usage: python run_experiment.py
"""
import traceback
import sys

def main():
    try:
        from experiment.experiment import run
        run()
    except Exception as e:
        with open("crash_log.txt", "w") as f:
            traceback.print_exc(file=f)
        raise e

if __name__ == "__main__":
    main()
