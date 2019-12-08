# Python Cricketer Analysis
### Web scraping, data collection and visualisation of different cricketers

This is an extensive webscraper using `requests`, `BeautifulSoup` and `pandas` that creates a data frame of test match innings for a given cricketer using [ESPN cricinfo](https://www.espncricinfo.com/)'s web pages. 

Functionality has been wrapped inside a `Cricketer` ([found here](/classes/Cricketer.py)) class that allows for the application of methods to produce summary statistics and rolling averages that can be used to analyse the overall performance of the player simply by passing in the link for that player.

Further information can be gained about the performance through subsequently scraping the particular match using `Match` and `Innings` classes allowing for a wider range of metrics to be analysed.  

### Visualisations created using the scraper
Below are some visualisations that were created for an article that I wrote: [Has captaincy ruined Joe Root?](https://medium.com/@willcanniford/has-captaincy-ruined-joe-root-d1a329c4f9ab?source=friends_link&sk=04ad47ca729e4c7f730eff1e48698010) 

The code used to produce them can be found in this [notebook](/article_visualisations.ipynb).

![Top 4](https://github.com/willcanniford/python-cricketer-analysis/blob/master/images/big_4_through_captaincy.jpeg?raw=true)

![Joe Root Test Average Career](https://github.com/willcanniford/python-cricketer-analysis/blob/master/images/joe_root_accumulative_average.jpeg?raw=true)
