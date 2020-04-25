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
    load_from_url('http://mp.weixin.qq.com/s?__biz=MzA4MTY0NTYwMA==&amp;mid=2651182121&amp;idx=1&amp;sn=e12407837970ce236dab0f0700cd0794&amp;chksm=8460ad66b317247033a24d8ba8759ecd442dcbfb05864676dd69c0d81c1ec72108793f81fd8f&amp;scene=27#wechat_redirect')