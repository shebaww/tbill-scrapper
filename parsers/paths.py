from pathlib import Path
current_dir = Path(__file__).resolve().parent
root = current_dir.parent
data = root / "data"
kenya_pdfs = data / "kenya-pdfs"
parsers = root / "parsers"
ETH_CSV = data / "ethiopian-tbills.csv"
KSH_CSV = data / "kenyan-tbills.csv"
MASTER_CSV = data / "master.csv"
