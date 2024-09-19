##MSJC Events Scraper##

This is a simple web scraper that scrapes the events from the Mt. San Jacinto College website and outputs them to a JSON and Excel file.
The scraper is written in Python and uses Playwright to bypass the websites' JavaScript rendering.
Then, the data is parsed using BeautifulSoup and Pandas to output the data to a JSON and Excel file.

###Installation###

###Usage###
To run the scraper, run the following command:

```bash
python scraper.py
```

###Output###
The scraper will output the data to a JSON and Excel file in the `output` directory.

###Dependencies###

- [Playwright](https://playwright.dev/python/docs/intro)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Pandas](https://pandas.pydata.org/)
- [openpyxl](https://openpyxl.readthedocs.io/en/stable/)

###License###
This project is licensed under the MIT License - see the LICENSE file for details.

###Author###

- [David Pena Gutierrez](https://daveed.dev)

###Acknowledgements###

- [Mt. San Jacinto College](https://www.msjc.edu)
- [Playwright](https://playwright.dev/python/docs/intro)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Pandas](https://pandas.pydata.org/)
- [openpyxl](https://openpyxl.readthedocs.io/en/stable/)
