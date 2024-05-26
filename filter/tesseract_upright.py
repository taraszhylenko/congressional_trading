import argparse, os

import pdf2image as p2i
import pytesseract
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--input-pdf-dir',  required=True, type=str)
parser.add_argument('--output-pdf-dir', required=True, type=str)
args = parser.parse_args()

for pdfname in os.listdir(args.input_pdf_dir):
    print(f'Processing {pdfname}')
    pdffullname       = f'{args.input_pdf_dir}/{pdfname}'
    pdffullnameoutput = f'{args.output_pdf_dir}/{pdfname}'
    imgs = p2i.convert_from_path(pdffullname)
    if 'PERIODIC TRANSACTION REPORT' in pytesseract.image_to_string(imgs[0], lang='eng'):
        subprocess.run(["cp", pdffullname, pdffullnameoutput])

