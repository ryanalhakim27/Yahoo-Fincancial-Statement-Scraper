# Guide to Use ScraFSY

## Before the Scrape
### Install ChromeDriver
This module require chrome driver for web-crawling. Make sure you have alreadu installed chromedriver and note the location of your ChromeDriver in your PC.

### Install Required Library

This module require some library such as BeautifulSoup4, Selenium, time, Pandas, and Numpy.
<br>1. BeautifulSoup4 is used for parse HTML from Yahoo Finance. This parse process is needed to collect the important information from the HTML file. 
<br>2. Selenium is used for web crawling. This is needed because some data need document object model from javascript to be generated. And it active when there are interaction with pages.
<br>3. time is used for delaying in process block code. This is needed because the pages has to be fully loaded before HTML collection process.
<br>4. Pandas is used to make dataframe
<br>5. Numpy is used for manipulate data type.

### Import Module
<pre>
    <code>from ScraFSY import YFinanceScrapper </code> 
</pre>

## Scrape Journey

### 1. Instances a Scrape Session Object

You must instance a Scrape Session Object in each scrape session.

<h4>For example:</h4>
<pre>
    <code>bca = YFinanceScrapper('BBCA.JK) 
    <br>bmri = YFinanceScrapper('BMRI.JK) 
    <br>aali = YFinanceScrapper('AALI.JK) </code> 
</pre>
There are 3 session of scrape.
<br><br>Notes: Before you start to collect data, make sure you already defined your path location of your ChromeDriver in attribute path.
<h4>For example:</h4>
<pre>
    <code>bca = YFinanceScrapper('BBCA.JK) 
    <br>bca.path = '/usr/local/bin/chromedriver'
     </code> 
</pre>

### 2. Get OneState Dataframe 
There are two option in way to getting OneState Dataframe.
You can get all 3 separated financial statement dataframe in one function using `get_alldata()` or get one statement dataframe using `get_finance_data(statement)`.
<h4>For example:</h4>
<pre>
    <code>bca.get_finance_data('Income Statement') 
    <br>bca.income_statement </code> 
</pre>
You will get income statement dataframe in attribute income_statement.
<br>or
<pre>
    <code>bca.get_alldata() 
    <br>bca.income_statement
    <br>bca.cash_flow
    <br>bca.balance_sheet </code> 
</pre>
You will get income statement dataframe in attribute income_statement, balance sheet dataframe in balance_sheet, and cash flow dataframe in cash_flow

### 3. Get KeyFeat Dataframe 

After you get OneState Dataframe, you can generated KeyFeat Dataframe in  using method `important_dataframe()`.
<h4>For example:</h4>
<pre>
    <code>goto=YFinanceScrapper('GOTO.JK)
    <br>goto.get_alldata() 
    <br>goto.important_dataframe()
     </code> 
</pre>
<br>It will give you dataframe like this:
<br>
<br>
![Image title](important_dataframe.png)
Note: It is not work in Bank financial statements because different format of financial statements.

### 4. Get Metric Dataframe 

If your KeyFeat Dataframe has been already built, you can make Metric Dataframe by using method `metric_dataframe()`.
<h4>For example:</h4>
<pre>
    <code>goto=YFinanceScrapper('GOTO.JK)
    <br>goto.get_alldata() 
    <br>goto.important_dataframe()
    <br>goto.metric_dataframe()
     </code> 
</pre>
<br>It will give you dataframe like this:
<br>
<br>
![Image title](metric_dataframe.png)

### 5. Convert Dataframe to CSV Files

You can convert dataframe to csv files by using method `convert_to_csv(table)`
<h4>For example:</h4>
<pre>
    <code>goto=YFinanceScrapper('GOTO.JK)
    <br>goto.get_finance_data('Income Statement') 
    <br>goto.convert_to_csv(self.income_statement)
     </code> 
</pre>
<br>
Please see the [References](references.md) for further details.

## About the Dataframe
### OneState Dataframe
One state dataframe is dataframe that represent each statement in financial statement (Income Statement, Balance Sheet, and Cash Flow Statement). The feature of this dataframe is vary depend on company financial statement format in Yahoo Finance. You can get this dataframe in all company that is provided by Yahoo FInance

### KeyFeat Dataframe
KeyFeat dataframe is dataframe that contain feature combination in each statement. The following are list of features in this dataframe:
<ol>
  <li>Company</li>
  <li>Time</li>
  <li>Current Assets</li>
  <li>Current Liabilities</li>
  <li>Inventories</li>
  <li>Cash and Cash Equivalent</li>
  <li>Total Assets</li>
  <li>Total Liabilitites</li>
  <li>Shareholder Equity</li>
  <li>Operating Cashflow</li>
  <li>Investing Cashflow</li>
  <li>Financing Cashflow</li>
  <li>End Cash </li>
  <li>ross Profit</li>
  <li>Operating Income</li>
  <li>Total Revenue</li>
  <li>Net Income</li>
  <li>Interest Expense</li>
  <li>Cost of Good Sold</li>
  <li>EBIT </li>
  <li>EPS </li>
  <li>EBITDA </li>
</ol>

### Metric Dataframe
Metric dataframe is dataframe that contain selected financial metrics that are calculated from KeyFeat Dataframe. The following are list of features in this dataframe:
<ol>
  <li>Company</li>
  <li>Time</li>
  <li>Current Ratio</li>
  <li>Acid Test Ratio</li>
  <li>Cash Ratio</li>
  <li>Operating Cashflow Ratio</li>
  <li>Debt Ratio</li>
  <li>Return on Asset Ratio</li>
  <li>Debt to Equity Ratio</li>
  <li>Interest Coverage Ratio</li>
  <li>Return on Equity Ratio</li>
  <li>Gross Margin Ratio</li>
  <li>Operating Margin Ratio</li>
</ol>











