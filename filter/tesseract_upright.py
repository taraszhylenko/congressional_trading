import argparse, os, pathlib
import multiprocessing as mp

import pdf2image as p2i
import pytesseract
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--input-pdf-dir',          required=True, type=str)
parser.add_argument('--output-pdf-dir',         required=True, type=str)
parser.add_argument('--output-txt-dir',         required=True, type=str)
parser.add_argument('--num-parallel-processes', required=True, type=int)
args = parser.parse_args()

pathlib.Path(args.output_pdf_dir).mkdir(parents=True, exist_ok=True)
pathlib.Path(args.output_txt_dir).mkdir(parents=True, exist_ok=True)

def filter_upright_pdfs(pdf_names_set, input_pdf_dir, output_pdf_dir, output_txt_dir):
    for pdfname in pdf_names_set:
        print(f'Processing {pdfname}')
        pdffullname       = f'{input_pdf_dir}/{pdfname}'
        pdffullnameoutput = f'{output_pdf_dir}/{pdfname}'
        imgs = p2i.convert_from_path(pdffullname)
        if 'PERIODIC TRANSACTION REPORT' in pytesseract.image_to_string(imgs[0], lang='eng'):
            os.system(f'cp "{pdffullname}" "{pdffullnameoutput}"')
            for img_idx, img in enumerate(imgs):
                page_name = '.'.join(pdfname.split('.')[:-1]) + f'_page_{img_idx}.txt'
                with open(f'{output_txt_dir}/{page_name}', 'w') as f:
                    f.write(pytesseract.image_to_string(img, lang='eng'))


pdf_names = os.listdir(args.input_pdf_dir)
set_size = len(pdf_names) // args.num_parallel_processes 
pdf_name_sets = [pdf_names[i:i+set_size] for i in range(0, len(pdf_names) + set_size, set_size)]

processes = [mp.Process(target=filter_upright_pdfs, args=(pdf_names_set,
                                                          args.input_pdf_dir,
                                                          args.output_pdf_dir,
                                                          args.output_txt_dir)) for pdf_names_set in pdf_name_sets]

for p in processes:
    p.start()

for p in processes:
    p.join()
