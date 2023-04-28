''' This module providing class represent a session in scrapping process.
 
This module is used for scrape financial statement data from Yahoo Finance.
In one session, you can only scrape financial statement data from one company.
The data consist of balance sheet, income statement, and cashflow statement. 
Those are tabulated for each statement. You can also get one table that contain
selected features from each statement, and one table that contain selected
financial metrics from the selected features.

This module require selenium and beautifoul soup 4 for scrapping and crawling,
pandas for making dataframe, and numpy for numerical manipulation.
Please install required library before use it!

'''

#Import Necessary Library
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as soup
import pandas as pd
import time as waktu
import numpy as np

#Scrape session object construcor
class YFinanceScrapper():
    '''
    A class that represent one scrape session

    Examples:
        >>> bca=YFinanceScrapper('BBCA.JK')

    Args:
        company_code (str): The company code that
            you want to scrape 
            
    Attributes:
        address (dict): Dictionary that contain statement as key and
            yahoo adress as value.
        balance_sheet (pandas.Dataframe): A pandas Dataframe that contain
            balance sheet statement data.
        cash_flow (pandas.Dataframe): A pandas Dataframe that contain
            cash flow statement data.
        company_code (str): The company code that you want to scrape.
        collect (list): A list that contain all name of features and their value.
        content (bs4.BeautifulSoup): BeautifulSoup object that contain Yahoo Finance
            HTML file in Pythonic idioms.
        features (list): A list that contain name of features those are collected.
        headers (list): A list that contain name of headers in Yahoo Finance
            financial statements table.
        imp_dataframe (pandas.Dataframe): A pandas Dataframe that contain
            selected features from each statement. 
        income_statement (pandas.Dataframe): A pandas Dataframe that contain
            income statement data.
        metric (pandas.Dataframe): A pandas Dataframe that contain
            selected financial metrics from selected features.
        note (list): A list that contain note that explain value (Ex:Currency).
        path (str): Location of chromedriver.
        table_choice (list): List of statement that can be chosen.
        time (list): List of periodic of collected data.
    '''
    #Function for initialization of object
    def __init__(self,company_code):
        self.income_statement=None
        self.note=[]
        self.metric=None
        self.balance_sheet=None
        self.cash_flow=None
        self.imp_dataframe=None
        self.path='/usr/local/bin/chromedriver'
        self.content=None
        self.features=['Company','Time']
        self.collect=[]
        self.time=[]
        self.headers=[]
        self.company_code=company_code
        self.table_choice=['Income Statement','Balance Sheet','Cash Flow']
        self.address={
            'Income Statement': 'https://finance.yahoo.com/quote/'
                +self.company_code+'/financials?p='+self.company_code,
            'Balance Sheet': 'https://finance.yahoo.com/quote/'
                +self.company_code+'/balance-sheet?p='+self.company_code, 
            'Cash Flow' : 'https://finance.yahoo.com/quote/'
                +self.company_code+'/cash-flow?p='+self.company_code
        }
      
    #Function for get html data  
    def get_html_data(self, statement):
        '''Retrieve a Beautifulsoup object that contains JSON file from Yahoo Finance.

        Examples:
            >>> bca = YFinanceScrapper('BBCA.JK')
            >>> content= bca.get_html_data('Income Statement')

        Args:
            statement (str): The selected statement that is gonna be scraped.

        Returns:
            content (bs4.BeautifulSoup): BeautifulSoup object that contain Yahoo Finance 
                HTML file in Pythonic idioms.
        '''
        try:
            #Initiate web driver
            driver=webdriver.Chrome(self.path)
            if statement in self.table_choice:
                #Access link
                driver.get(self.address[statement])
            else :
                print('Your statement input is wrong')
            #Wait until web appear and then select period of data
            WebDriverWait(driver,20).until(
                EC.element_to_be_clickable((By.XPATH,'//span[text()="Quarterly"]'))).click()
            #Wait until web appear and then select period of data
            WebDriverWait(driver,20).until(
                EC.element_to_be_clickable((By.XPATH,'//span[text()="Expand All"]'))).click()
            #Wait until web appear and ready take the html
            waktu.sleep(10)
            #Create html element
            html = driver.execute_script('return document.body.innerHTML;')
            #Connect to Beautiful Soup for Parsing
            self.content = soup(html,'lxml')
            #Close the wesite
            driver.quit()
            return self.content
        except:
            print('There is change in html structure, Please inform this error to us!')

    def parse_data(self,content,statement):
        '''Parse JSON file from Yahoo Finance to get data in Financial Statements.

        Examples:
            >>> bca = YFinanceScrapper('BBCA.JK')
            >>> collect= bca.parse_data(self.content,'Income Statement')

        Args:
            content (bs4.BeautifulSoup): BeautifulSoup object that contain Yahoo Finance
                HTML file in Pythonic idioms.
            statement (str): The selected statement that is gonna be scraped.

        Returns:
            collect (list): A list that contain all name of features and their value.
            headers (list): A list that contain name of headers in the table.
            time (list): List of periodic of collected data.
        '''
        try:
            #Find note of the currency
            notes = content.find_all('span', class_='Fz(xs)')
            for noted in notes:
                if noted not in self.note:
                    self.note.append(noted.text)
            #Find all div that contain class D(tbr)
            rows = content.find_all('div', class_='D(tbr)')
            #create time of data
            for header in rows[0].find_all('span'):
                self.headers.append(header.text)
            #Create list of time
            if statement != 'Balance Sheet':
                self.time=self.headers[2:]
            elif statement == 'Balance Sheet':
                self.time=self.headers[1:]
            #create features of data
            for row in rows:
                columns=row.find_all('span',class_='Va(m)')
                for column in columns:
                    self.features.append(column.text)
            #Get data in all features
            data=[]
            index=1
            while index <= len(rows)-1:
                span=rows[index].find_all('div')
                for a in span:
                    data.append(a.text) 
                self.collect.append(data)
                data=[]
                index += 1
            for item in self.collect:
                del item[1:3]
            return self.collect, self.headers, self.time
        except:
            print('There are change in table format of financial statements, Please inform this error to us!')

    def create_dataframe(self,collect,headers,time,statement):
        '''Create dataframe from data that already collected from parsing process.

        Examples:
            >>> bca = YFinanceScrapper('BBCA.JK')
            >>> df= bca.create_dataframe(self.collect,self.headers,self.time,'Income Statement')
        
        Args:
            collect (list): A list that contain all name of features and their value.
            headers (list): A list that contain name of headers in Yahoo Finance
                financial statements table.
            time (list): List of periodic of collected data.
            statement (str): The selected statement that is gonna be scraped.

        Returns:
            df2 (pandas.Dataframe): Dataframe that contain data from selected statement.
        '''
        try:
            df=pd.DataFrame(collect,columns=headers)
            df2=df.T
            new_col=[]
            for i in df2.iloc[0]:
                new_col.append(i)
            df2.columns=new_col
            df2=df2.reset_index(drop=True)
            if statement != 'Balance Sheet':
                df2=df2.drop([0,1]).reset_index(drop=True)
            elif statement =='Balance Sheet':
                df2=df2.drop([0]).reset_index(drop=True)
            df2=df2.applymap(self.value_to_num)
            df2['Time']=pd.to_datetime(time)
            df2['Company']=self.company_code
            df2=df2[self.features]
            return df2
        except:
            print('There are change in structure of financial statement table, please inform us this error!')

    def get_finance_data(self, statement):
        '''Retrieve dataframe that contains all data in selected statement.

        Examples:
            >>> bca = YFinanceScrapper('BBCA.JK')
            >>> df= bca.get_finance_data('Income Statement')
        
        Args:
            statement (str): The selected statement that is gonna be scraped.

        Returns:
            balance_sheet (pandas.Dataframe): A pandas Dataframe that contain
                balance sheet statement data.
            cash_flow (pandas.Dataframe): A pandas Dataframe that contain
                cash flow statement data.
            income_statement (pandas.Dataframe): A pandas Dataframe that contain
                income statement data.
        '''
        self.content=self.get_html_data(statement=statement)
        self.collect, self.headers, self.time = self.parse_data(
            content=self.content,statement=statement)
        if statement=='Income Statement':
            self.income_statement=self.create_dataframe(
                collect=self.collect,headers=self.headers,time=self.time,statement=statement)
            return self.income_statement
        elif statement=='Balance Sheet':
            self.balance_sheet=self.create_dataframe(
                collect=self.collect,headers=self.headers,time=self.time,statement=statement)
            return self.balance_sheet
        elif statement=='Cash Flow':
            self.cash_flow=self.create_dataframe(
                collect=self.collect,headers=self.headers,time=self.time,statement=statement)
            return self.cash_flow
    
    def reset_data(self,param1=None):
        '''Reset variable content, features, collect, time, and headers so it can use for scrape again.

        Examples:
            >>> bca = YFinanceScrapper('BBCA.JK')
            >>> df= bca.get_finance_data('Income Statement')
            >>> bca.reset_data()
            >>> df_new= bca.get_finance_data('Balance Sheet')
        
        Args:
            param1 (:obj:`str`, optional): The first parameter. 
                Defaults to None.

        Returns:
            collect (list): Empty list for store collected data.
            content (NoneType): Variable content set to None for collected 
                BeautifulSoup JSON data.
            features (list): Set features to default for storing features.
            headeres (list): Empty list for storing headers of financial
                statements table headers.
            time (list): Empty list for storing periodic of
                financial statements data.
        '''
        self.content=None
        self.features=['Company','Time']
        self.collect=[]
        self.time=[]
        self.headers=[]

    def get_alldata(self,param1=None):
        '''Retrieve all statement in 3 dataframe of selected company.

        Examples:
            >>> bca = YFinanceScrapper('BBCA.JK')
            >>> bca.get_alldata()

        Args:
            param1 (:obj:`str`, optional): The first parameter. 
                Defaults to None.

        Returns:
            balance_sheet (pandas.Dataframe): A pandas Dataframe that contain
                balance sheet statement data.
            cash_flow (pandas.Dataframe): A pandas Dataframe that contain
                cash flow statement data.
            income_statement (pandas.Dataframe): A pandas Dataframe that contain
                income statement data.
        '''
        for statement in self.table_choice:
            self.get_finance_data(statement=statement)
            self.reset_data()

    def convert_to_csv(self,name_of_table):
        '''Convert selected statements table to csv.

        Examples:
            >>> bca = YFinanceScrapper('BBCA.JK')
            >>> df= bca.get_finance_data('Income Statement')
            >>> bca.convert_to_csv(income_statement)

        Args:
            name_of_table (str): Name of table.

        Returns:
            csv file of selected dataframe.

        '''
        if name_of_table == 'income_statement':
            self.income_statement.to_csv(f'csv_files/{self.company_code}_{name_of_table}.csv')
        elif name_of_table == "balance_sheet":
            self.balance_sheet.to_csv(f'csv_files/{self.company_code}_{name_of_table}.csv')
        elif name_of_table == "cash_flow":
            self.cash_flow.to_csv(f'csv_files/{self.company_code}_{name_of_table}.csv')
        elif name_of_table == "imp_dataframe":
            self.imp_dataframe.to_csv(f'csv_files/{self.company_code}_{name_of_table}.csv')
        elif name_of_table == "metric":
            self.metric.to_csv(f'csv_files/{self.company_code}_{name_of_table}.csv')
        else:
            print('your input is false')

    def value_to_num(self,x):
        '''Data manipulation that convert '-' to nan, convert ',' to '',
            convert 'K' to 1000.

        Args:
            x (optional): Selected value that want to change.

        Returns:
            x (float): New value with type float.

        '''
        if x == '-':
            return np.nan
        if type(x) != float or type(x)!=int:
            if '.' not in x:
                return int(float(x.replace(',','')))
            elif '.' in x :
                return float(x.replace(',',''))
        if 'K' in x:
            if len(x) > 1:
                return int(float(x.replace('K',''))* 1000)
            return 1000.0
    
    def important_dataframe(self,param1=None):
        '''Create dataframe that contain selected features from all statements table.

        Examples:
            >>> goto = YFinanceScrapper('GOTO.JK')
            >>> goto.get_alldata()
            >>> goto.important_dataframe()
        
         Args:
            param1 (:obj:`str`, optional): The first parameter. 
                Defaults to None.

        Returns:
            imp_dataframe (pandas.Dataframe): A pandas Dataframe that contain
                selected features from each statement.
        '''
        try:
            important_header=['time','company','current_assets','current_liabilities',
                            'inventories','cash&cashequiv','total_assets',
                            'total_liabilities','shareholder_equity',
                            'operating_cashflow','gross_profit','investing_cashflow',
                            'financing_cashflow','end_cash',
                            'operating_income','total_revenue','net_income',
                            'interest_expense','cost_of_good_sold','EBIT','EPS','EBITDA']
            df=pd.DataFrame(None, columns=important_header)
            df['time']=self.income_statement.get('Time')
            df['company']=self.income_statement.get('Company')
            df['current_assets']=self.balance_sheet.get('Current Assets')
            df['current_liabilities']=self.balance_sheet.get('Current Liabilities')
            df['inventories']=self.balance_sheet.get('Inventory')
            df['cash&cashequiv']=self.balance_sheet.get('Cash And Cash Equivalents')
            df['total_assets']=self.balance_sheet.get('Total Assets')
            df['total_liabilities']=self.balance_sheet.get('Total Liabilities Net Minority Interest')
            df['shareholder_equity']=self.balance_sheet.get("Stockholders' Equity")
            df['operating_cashflow']=self.cash_flow.iloc[:,2]
            df['investing_cashflow']=self.cash_flow.get('Investing Cash Flow')
            df['financing_cashflow']=self.cash_flow.get('Financing Cash Flow')
            df['end_cash']=self.cash_flow.get('End Cash Position')
            df['gross_profit']=self.income_statement.get('Gross Profit')
            df['operating_income']=self.income_statement.get('Operating Income')
            df['total_revenue']=self.income_statement.get('Total Revenue')
            df['interest_expense']=self.income_statement.get('Interest Expense')
            df['net_income']=self.income_statement.get('Net Income')
            df['cost_of_good_sold']=self.income_statement.get('Cost of Revenue')
            df['EBIT']=self.income_statement.get('EBIT')
            df['EPS']=self.income_statement.get('Basic EPS')
            df['EBITDA']=self.income_statement.get('Normalized EBITDA')
            self.imp_dataframe = df
            return self.imp_dataframe
        except(KeyError):
            print('There are data that unavailable')

    def metric_dataframe(self,param1=None):
        '''Create dataframe that contain selected financial metrics
            from important dataframe.

        Examples:
            >>> bca = YFinanceScrapper('BBCA.JK')
            >>> bca.get_alldata()
            >>> bca.important_dataframe()
            >>> bca.metric_dataframe()
        
         Args:
            param1 (:obj:`str`, optional): The first parameter. 
                Defaults to None.

        Returns:
            metric (pandas.Dataframe): A pandas Dataframe that contain
                selected financial metrics from selected features.
        '''
        metric_header=['time','company','net_profit_margin','current_ratio','acidtest_ratio',
                          'cash_ratio','operating_cash_flow_ratio','debt_ratio',
                          'return_on_asset_ratio','debt_to_equity_ratio',
                          'interest_coverage_ratio','return_on_equity_ratio',
                          'gross_margin_ratio','operating_margin_ratio']
        df=pd.DataFrame(None, columns=metric_header)
        df['time']=self.income_statement.get('Time')
        df['company']=self.income_statement.get('Company')
        df['net_profit_margin']=self.imp_dataframe.get('net_income')/self.imp_dataframe.get('total_revenue')
        df['current_ratio']=self.imp_dataframe.get('current_assets')/self.imp_dataframe.get('current_liabilities')
        df['acidtest_ratio']=(self.imp_dataframe.get('current_assets')-self.imp_dataframe.get('inventories'))/self.imp_dataframe.get('current_liabilities')
        df['cash_ratio']=self.imp_dataframe.get('cash&cashequiv')/self.imp_dataframe.get('current_liabilities')
        df['operating_cash_flow_ratio']=self.imp_dataframe.get('operating_cashflow')/self.imp_dataframe.get('current_liabilities')
        df['debt_ratio']=self.imp_dataframe.get('total_liabilities')/self.imp_dataframe.get('total_assets')
        df['debt_to_equity_ratio']=self.imp_dataframe.get('total_liabilities')/self.imp_dataframe.get('shareholder_equity')
        df['interest_coverage_ratio']=self.imp_dataframe.get('EBIT')/self.imp_dataframe.get('interest_expense')
        df['gross_margin_ratio']=self.imp_dataframe.get('gross_profit')/self.imp_dataframe.get('total_revenue')
        df['operating_margin_ratio']=self.imp_dataframe.get('operating_income')/self.imp_dataframe.get('total_revenue')
        df['return_on_asset_ratio']=self.imp_dataframe.get('net_income')/self.imp_dataframe.get('total_assets')
        df['return_on_equity_ratio']=self.imp_dataframe.get('net_income')/self.imp_dataframe.get('shareholder_equity')
        self.metric = df
        return self.metric