import base64
import json
import time
from io import BytesIO
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions


class PdfGenerator:
    """
     Simple use case:
        pdf_file = PdfGenerator(['https://google.com']).main()
        with open('new_pdf.pdf', "wb") as outfile:
            outfile.write(pdf_file[0].getbuffer())
    """
    driver = None
    # https://chromedevtools.github.io/devtools-protocol/tot/Page#method-printToPDF
    print_options = {
        'landscape': False,
        'displayHeaderFooter': False,
        'printBackground': True,
        'preferCSSPageSize': True,
        'paperWidth': 6.97,
        'paperHeight': 16.5,
    }

    def __init__(self, urls: List[str]):
        self.urls = urls

    def _get_pdf_from_url(self, url, *args, **kwargs):
        self.driver.get(url)

        time.sleep(0.3)  # allow the page to load, increase if needed

        print_options = self.print_options.copy()
        result = self._send_devtools(self.driver, "Page.printToPDF", print_options)
        return base64.b64decode(result['data'])

    @staticmethod
    def _send_devtools(driver, cmd, params):
        """
        Works only with chromedriver.
        Method uses cromedriver's api to pass various commands to it.
        """
        resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
        url = driver.command_executor._url + resource
        body = json.dumps({'cmd': cmd, 'params': params})
        response = driver.command_executor._request('POST', url, body)
        return response.get('value')

    def _generate_pdfs(self):
        pdf_files = []

        for url in self.urls:
            result = self._get_pdf_from_url(url)
            file = BytesIO()
            file.write(result)
            pdf_files.append(file)

        return pdf_files

    def main(self) -> List[BytesIO]:
        webdriver_options = ChromeOptions()
        webdriver_options.add_argument('--headless')
        webdriver_options.add_argument('--disable-gpu')

        try:
            self.driver = webdriver.Chrome(
                options=webdriver_options
            )
            result = self._generate_pdfs()
        except Exception as e:
            print(self.driver, e)
            self.driver.close()
        finally:
            self.driver.close()

        return result

def convert_to_pdf(url, filename):
    print(url +  "----" + filename)
    try : 
        pdf_file = PdfGenerator([url]).main()
        with open(filename, "wb") as outfile:
            outfile.write(pdf_file[0].getbuffer())
        return { "success" : True }
    except Exception as e:
        return {"success" : False , "error" : e }

# adi = convert_to_pdf("https://stackoverflow.com/questions/5998245/how-do-i-get-the-current-time-in-milliseconds-in-python", "new.pdf")
# print(adi)