import pdfkit
import pandas as pd
import os

config = {
        'file_dir': 'data/datastmp.csv',
        'pdfkit_config': 'wkhtmltopdf/bin/wkhtmltopdf.exe',
        'pdf_output_dir': 'data/pdf'
    }


def load_from_file(config):
    dataTable = pd.read_csv(config['file_dir'])
    urllist = dataTable['url'].drop_duplicates().values.tolist()
    indexlist = dataTable['url'].drop_duplicates().index.tolist()

    for url, index in zip(urllist, indexlist):
        config_pdf = pdfkit.configuration(wkhtmltopdf=config['pdfkit_config'])
        pdfkit.from_url(url=url,
                        output_path=os.path.join(config['pdf_output_dir'], '{}.pdf'.format(str(index))),
                        configuration=config_pdf)


def load_from_url(url):
    config_pdf = pdfkit.configuration(wkhtmltopdf=config['pdfkit_config'])
    pdfkit.from_url(url=url,
                    output_path=os.path.join(config['pdf_output_dir'], '{}.pdf'.format('file')),
                    configuration=config_pdf)

if __name__ == "__main__":
    #load_from_file(config)
    load_from_url('https://zhuanlan.zhihu.com/p/66048276')