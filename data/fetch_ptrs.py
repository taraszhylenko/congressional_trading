import datetime
import os
import pandas as pd
import random
import time
import urllib.request


fix_date = lambda raw_: datetime.datetime.strptime(raw_, "%m/%d/%Y").strftime("%Y%m%d")

doc_index = pd.read_csv('/home/steganopus/Documents/TAoS/misc/20240521/scratch/congressional_trading/data/index/csv/all_years_index.csv')

ptr_dir = '/home/steganopus/Documents/TAoS/misc/20240521/scratch/congressional_trading/data/ptr/pdf'

ptr_index = doc_index[doc_index.FilingType == 'P']

for _, ptr_row in ptr_index.iterrows():
    last = ptr_row.Last
    first = ptr_row.First
    state_dst = ptr_row.StateDst
    date_raw = ptr_row.FilingDate
    date = fix_date(date_raw) 
    doc_id = ptr_row.DocID
    record_name = f"{date}_{first}{last}{doc_id}.pdf"
    year = ptr_row.Year
    output_file = f"{ptr_dir}/{record_name}"
    if not os.path.isfile(output_file):
        urllib.request.urlretrieve(f"https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{year}/{doc_id}.pdf", output_file)
        print(f"Fetched {record_name}")
        time.sleep(30 + random.randint(0, 10))
    else:
        print(f"{record_name} is present")
