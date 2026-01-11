import sys
import warnings

from datetime import datetime

from crewai_stock_picker.crew import CrewaiStockPicker

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    inputs = {
        'sector': 'Technology',
        'current_date': str(datetime.now())
    }

    try:
        result = CrewaiStockPicker().crew().kickoff(inputs=inputs)
        print("\n\n=== FINAL DECISION ===\n\n")
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")