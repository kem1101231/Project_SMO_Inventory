from weasyprint import HTML, CSS


if __name__ == '__main__':
	
    HTML('doc-iarTest22.html').write_pdf('testmultipage.pdf',

        stylesheets=[CSS(string='@page {size: Legal; margin:35px;}')])