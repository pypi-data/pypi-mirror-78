
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as web
from datetime import date, timedelta

class portfolio:
    def __init__(self, tickers, start = date.today() - timedelta(days=5*365) , end=date.today()):
        
        '''
        input:
            tickers: a list of stock tickers to be included in the portfolio
            start: desired start date, default date is 5 years ago
            end : end date, default date is today

        return:
            means: annualized mean return of each stock
            cov_matrix: annualized covariance matrix between the stocks
        '''
        self.tickers = tickers
        # get stock price from yahoo finance
        multpl_stocks = web.get_data_yahoo(tickers,  start = start, end = end)

        # get the monthly return value of each stock
        #multpl_stock_monthly_returns = multpl_stocks['Adj Close'].resample('M').ffill().pct_change()

        #daily
        multpl_stock_daily_returns = multpl_stocks['Adj Close'].pct_change()
        self.means = multpl_stock_daily_returns.mean() * 252
        self.cov_matrix = multpl_stock_daily_returns.cov() * 252

               

    ##  equal allocation portfolio
    def equal_allocation(self):
        n = len(self.means)
        weights=np.ones(n)* 1/ n
        self.get_portfolio_stats( weights )
        return weights

    ##  minimum risk portfolio
    def min_risk(self, show_stats=True):
        ones = np.ones(len(self.means))
        x = np.dot(np.linalg.inv(self.cov_matrix), ones)
        weights= x / sum(x)
        self.get_portfolio_stats( weights, show_stats=show_stats )
        return weights

    ##  optimal portfolio, tangency point
    def opt_portfolio(self, Rf=0.005, show_stats=True):
        z = np.dot(np.linalg.inv(self.cov_matrix), self.means-Rf)
        weights = z/sum(z)
        self.get_portfolio_stats( weights, show_stats=show_stats )
        return weights

    def get_portfolio_stats(self, weights , Rf=0.005, show_stats=True):
        # annual return of the portfolio
        R_p = np.dot(weights.T , self.means)

        # annualized portfolio variance
        port_variance = np.dot( weights.T , np.dot(self.cov_matrix, weights))

        # annualized portfolio volatility 
        port_volatility = np.sqrt(port_variance)

        optimal_port_weights = dict(zip(self.tickers, weights))
        
        if show_stats:

            for key, value in optimal_port_weights.items():
                print(' {:5} : {:.4f}'.format( key, value))

            #Show the expected annual return, volatility or risk, and variance.
            percent_var = round(port_variance, 4) 
            percent_vols = round(port_volatility, 4) 
            percent_ret = round(R_p, 4)
            sharpe_ratio = round((R_p-Rf)/port_volatility, 4)
            print("Expected annual return : {:.2f}%".format(percent_ret*100))
            print('Annual volatility/standard deviation/risk : {:.2f}%'.format(percent_vols*100))
            print('Annual variance : {:.2f}%'.format(percent_var*100))
            print('Sharpe ratio : {:.2f}'.format(sharpe_ratio) )

    def min_risk_given_return(self, expected_return=0.3, show_stats=True):
        ones = np.ones(len(self.means))
        cov_inverse= np.linalg.inv(self.cov_matrix)
        
        #Compute A:
        A = np.dot(ones.T, np.dot(cov_inverse, self.means))

        #Compute B:
        B = np.dot(self.means.T, np.dot(cov_inverse, self.means))

        #Compute C:
        C = np.dot(ones.T, np.dot(cov_inverse, ones))

        #Compute D:
        D = B*C - A**2
        
        E = expected_return
        
        lambda1 = (C*E-A)/D
        lambda2 = (B-A*E)/D

        weights=lambda1* np.dot(cov_inverse, self.means) + lambda2* np.dot(cov_inverse, ones)
        self.get_portfolio_stats( weights, show_stats=show_stats )
        
        return weights, A, B, C, D
    
        ## plot efficient frontier using mutual fund theorem
    def plot_efficient_frontier(self): 
        # get two portfolios on the efficient frontier
        x1 = self.min_risk(show_stats=False) ## the weight of portfolio1
        x2, A, B, C, D = self.min_risk_given_return(show_stats=False) ## the weight of portfolio2
        risk_free_rate =0.05
        x3 =self.opt_portfolio(Rf=risk_free_rate, show_stats=False)
        
        # expected return of minimum risk portfolio ( portfolio1)
        m1= np.dot(x1.T , self.means)
        # variance of minimum risk portfolio
        v1 = np.dot( x1.T , np.dot(self.cov_matrix, x1))

        # expected return of the minimum risk portfolio for a target return of 0.3 ( portfolio2)
        m2= np.dot(x2.T , self.means)
        # variance of the minimum risk portfolio for a target return of 0.3
        v2 = np.dot( x2.T , np.dot(self.cov_matrix, x2))
        
        # expected return of the optimal portfolio with risk free asset
        m3 = np.dot(x3.T , self.means)
        # variance of the optimal portfolio with risk free asset
        v3 = np.dot( x3.T , np.dot(self.cov_matrix, x3))

        ## covariance between the portfolio1 and portfolio2
        cov = np.dot( x1.T , np.dot(self.cov_matrix, x2))

        #Now we have two portfolios on the frontier.  We can combine them to trace out the entire frontier:
        #Let a be the proportion of investor's wealth invested in portfolio 1.
        #Let b be the proportion of investor's wealth invested in portfolio 2.

        a = np.arange(-3, 3, 0.1)
        b = 1-a

        r_ab = a*m1 + b*m2

        var_ab = a**2*v1 + b**2*v2 + 2*a*b*cov
        sd_ab = var_ab**.5


        #Efficient frontier:
        minvar = 1/C
        minE = A/C

        sdeff = np.arange( (minvar)**0.5, 0.6, 0.0001 )


        y1 = (A + np.sqrt(D*(C*sdeff**2 - 1)))*(1/C) 
        y2 = (A - np.sqrt(D*(C*sdeff**2 - 1)))*(1/C) 

        # individual asset risk
        risk = np.sqrt(np.diag(self.cov_matrix))

        fig, ax = plt.subplots(figsize=(16, 10))
        ax.set_xlim([0, 0.7])
        ax.set_xlabel('Risk')
        ax.set_ylabel("Returns")
        ax.set_title("Portfolio optimization and Efficient Frontier")
        plt.scatter(risk , self.means, alpha=0.5, label='Individual stocks')  # plot individual asset risk-return
        
        plt.plot(sdeff, y1, color='black', label='Efficient frontier')
        plt.plot(sdeff, y2, color='black')
        plt.plot(sd_ab, r_ab, color='blue', label='Efficient frontier plotted with Mutual Fund Theorem')
        
        # plot capital allocation line
        x_vals = np.array(ax.get_xlim())
         
        y_vals = risk_free_rate +  x_vals* np.sqrt(C* risk_free_rate ** 2 - 2*risk_free_rate *A+B) 
        plt.plot(x_vals, y_vals, '--', label='Capital allocation line' )

        
        #plt.axline((v3**0.5, m3),(0, risk_free_rate), c='r', label='Capital allocation line')
        
        plt.plot(v1**0.5, m1, "<", color='red', markersize=10, label='Minimum risk portfolio')
        plt.plot(v2**0.5, m2, "s", color='orange', markersize=10, label='Minimum risk portfolio with annual target return of 30%')
        plt.plot(v3**0.5, m3, "*", color='hotpink', markersize=18, label='Optimal portfolio, Risk free asset: '+ str(risk_free_rate))
        
        plt.legend(frameon=False)
        
        for i, ticker in enumerate(self.tickers):
            ax.annotate(ticker, (risk[i], self.means[i] ))
            
        plt.savefig('EfficientFrontier.png')

        plt.show();

        