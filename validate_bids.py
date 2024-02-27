from bids_validator import BIDSValidator
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--dir", "-s", type=str, default="data/sub-COL")
args = parser.parse_args()

out = BIDSValidator().is_bids(args.dir)
print(out)