import pytest
import pdfplumber
import os
from parsers.paths import current_dir, root, data, parsers, kenya_pdfs, ETH_CSV, KSH_CSV, MASTER_CS
from parsers import modules


def test_parser():
    Parser = modules.Parser()
    Parser.kenya()
    assert "kenya-tbills.csv" in os.listdir("../parser") 
