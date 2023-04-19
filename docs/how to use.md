# Guide to Use ScraFSY

## Before the Scrape

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

### 2. Get Dataframe of Financial Statement
There are two option in way to getting financial statement dataframe.
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

### 3. Get Dataframe of Key Features Combination in each Statements

After you get financial statement dataframe, you can generated Dataframe of Key Features Combination in each Statements using method `important_dataframe()`.
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

### 4. Get Dataframe of Financial Metrics

If your Key Features Dataftame already built, you can make financial metrics dataframe by using method `metric_dataframe()`.
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
Please see the [References](reference.md) for further details.
