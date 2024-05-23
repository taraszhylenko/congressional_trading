import pandas as pd
import xml.etree.ElementTree as ET

years = list(range(2008, 2025))

output_dir = '/home/steganopus/Documents/TAoS/misc/20240521/scratch/congressional_trading/data/index/csv' 

members = list()
for year in years:
    tree = ET.parse(f'xml/{year}FD.xml')
    root = tree.getroot()
    for member in root:
        member_dict = dict()
        for attr in member:
            member_dict[attr.tag] = attr.text
        members.append(member_dict)

member_frame = pd.DataFrame(members)
breakpoint()
print('Done')
