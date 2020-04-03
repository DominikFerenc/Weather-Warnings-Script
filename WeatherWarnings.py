import urllib.request
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileReader
import io

class WeatherWarnings:
    pathWarnings = "https://dane.imgw.pl/data/current/ost_meteo"
    def openFile(self):
        try:
            with urllib.request.urlopen(self.pathWarnings) as urlNameFile:
                self.getUrlNameFile(urlNameFile)
        except ConnectionError:
            print("Err")



    def getUrlNameFile(self, urlNameFile):
        html_warnings_name_file = urlNameFile.read()
        if html_warnings_name_file == ' ':
            print("Not warnings.")
        else:
            self.parseHTML(html_warnings_name_file)


    def parseHTML(self, html_warnings_data):
        parse_html_warnings_data = BeautifulSoup(html_warnings_data, "html.parser")
        self.setDataInTab(parse_html_warnings_data)

    def setDataInTab(self, parse_html_warnings_data):
        tab_name_file = []
        for element in parse_html_warnings_data.find_all('a'):
            tab_name_file.append(''.join(element.findAll(text=True)))

        self.removeGarbageHTML(tab_name_file)
    def removeGarbageHTML(self, tab_name_file):
        tab_name_file.remove('Name')
        tab_name_file.remove("Last modified")
        tab_name_file.remove("Size")
        tab_name_file.remove("Description")
        tab_name_file.remove("Parent Directory")
        if not tab_name_file:
            print("Brak plików do otwarcia")
        else:
            self.getNameFiles(tab_name_file)

    def getNameFiles(self, tab_name_file):
        fileName = ''
        for i in range(len(tab_name_file)):
            fileName = tab_name_file[i]
            self.setPathToFile(fileName)


    def setPathToFile(self, fileName):
            path = self.pathWarnings + "/" + fileName
            self.showPath(path)
            self.openpdfFiles(path)


    
    def showPath(self, path):
        print(path)

    def openpdfFiles(self, path):
        try:
            with urllib.request.urlopen(path) as UrlPDF:
                self.readUrlPdf(UrlPDF)
        except ConnectionError:
            print("")

    def readUrlPdf(self, UrlPDF):
        pdf_data = UrlPDF.read()
        self.readPagesPdf(pdf_data)

    def readPagesPdf(self, pdf_data):
        memoryFIle = io.BytesIO(pdf_data)
        datafromPdfPages = PdfFileReader(memoryFIle)
        self.showAllData(datafromPdfPages)

    def showAllData(self, dataFromPdfPages):
        num_pages = dataFromPdfPages.numPages
        for i in range(num_pages):
            print(dataFromPdfPages.getPage(i).extractText())


def main():
    warnings = WeatherWarnings()
    warnings.openFile()


if (__name__ == '__main__'):
    main()