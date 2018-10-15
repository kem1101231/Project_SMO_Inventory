from weasyprint import HTML, CSS


if __name__ == '__main__':
	
    HTML('doc-rqTest.html').write_pdf('rqtest6.pdf',

        stylesheets=[CSS(string='@page {size: legal landscape; margin:35px;}')])