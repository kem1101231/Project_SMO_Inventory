from PyPDF2 import PdfFileMerger, PdfFileReader


if __name__ == '__main__':

	filenames = ['rqtest1.pdf','rqtest3.pdf','rqtest4.pdf']

	merger = PdfFileMerger()
	
	for filename in filenames:

		merger.append(PdfFileReader(file(filename, 'rb')))

	merger.write("document-output.pdf")
	
''' HTML('doc-rqTest.html').write_pdf('rqtest20.pdf',

        stylesheets=[CSS(string='@page {size: Legal; margin:35px;}')])'''
	
