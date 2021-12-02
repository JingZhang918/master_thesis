# Automated Single Stock Trading based on DRL

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li> <a href="#About this repository">About this repository</a>
    <li> <a href="#Set up environment">Set up environment</a>
    <li><a href="#Technical Indicator Analysis">Technical Indicator Analysis</a></li>
      <ul>
        <li><a href="#Final Results TI">Final Results</a> </li>
        <li><a href="#Main Functions TI">Main Functions</a> </li>
        <li><a href="#Future Improvements TI">Future Improvements</a> </li>
      </ul>
    <li><a href="#DRL Automated Trading">DRL Automated Trading</a></li>
      <ul>
        <li><a href="#Main Functions DRL">Main Functions</a> </li>
        <li><a href="#Problems and Solutions DRL">Problems and Solutions</a> </li>
        <li><a href="#Future Improvements DRL">Future Improvements</a> </li>
      </ul>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About this repository
This repository contains all required files for chapter 7 of my [master thesis](https://jingzhang.tech/wp-content/uploads/2021/12/thesis_2021_11_30.pdf). It contains two parts: [Technical_Indicator_analysis](https://github.com/JingZhang918/master_thesis/tree/main/Technical_Indicator_Analysis) 
and [DRL_Automated_Trading](https://github.com/JingZhang918/master_thesis/tree/main/DRL_Automated_Trading) 

<!-- 
Abstract from my master thesis:
>In recent years, with the development of technology, the application of deep reinforcement learning has been gradually penetrating every aspect of our life. In this paper, I propose a methodology to deploy the RL framework into fiance. Start with explaining a series of basic concepts, basic RL framework, Markov Decision Process, Bellman Equation, etc., and algorithms to solve RL problems, such as Monte Carlo Control, Temporal Difference Control, Monte Carlo Gradient Policy(REINFORCE), and Proximal Policy Optimization(PPO). Later, seven commonly adopted technical analysis indicators — Moving Average Convergence Divergence(MACD), Relative Strength Index(RSI), Stochastic Oscillator, etc. — are explored, and their profitability is exploited. Finally, by learning from these technical indicators, my trained agent can make lucrative decisions on automated stock trading. -->

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- Set up environment -->
## Set up environment
I **highly** recommend install [Ray](https://www.ray.io/) by the following commands, speaking from my experience, ray is 
relatively unstable. I have read many posts and encountered many problems, and this is the one that works.
```angular2html
conda create -n rllib_test python=3.7
conda activate rllib_test
pip install ray[rllib]
# clone ray repository
git clone https://github.com/ray-project/ray.git
cd ray
pip install -r python/requirements/ml/requirements_rllib.txt
```
Then install the other packages by
```angular2html
pip install yfinance pandas_ta plotly bayesian-optimization openpyxl -U kaleido
```
Then you should be fine :D
<p align="right">(<a href="#top">back to top</a>)</p>


<!-- Technical Indicator Analysis -->
## Technical Indicator Analysis
[Technical_Indicator_analysis](https://github.com/JingZhang918/master_thesis/tree/main/Technical_Indicator_Analysis) project is to calculate, visualize the indicator and use the trading signal emitted by the indicator to trade and evaluate its profitability.
Currently supported indicators include:
 - Moving Average Convergence Divergence (MACD) (period: 12, 26, 9)
 - Relative Strength Indicator (RSI) (threshold: 30/70)
 - Stochastic Oscillator (threshold: 20/80)
 - Average Directional Index (ADX) (period: 14, strength threshold: 25)
 - Aroon Oscillator (period: 25)
For more information about these indicators, check out my blog [here](https://jingzhang.tech/index.php/blog/).

<!-- Finan Results TI -->
### Finan Results

#### Version 1 - 2021-11-30

The trading period is from Nov 1, 2020 to Oct 31, 2021, 1 whole years. The initial balance is 1 Million Euro and the strategy is to fully trust the indicator signal, to wit, when it's a buy signal, I will use all my cash balance to buy as many shares as I can and when it's a sell signal, I will sell all my current owned shares.

The trading signal is lagging. In plain words, at the end of a trading day, use today's price to calculate the indicator and identify the trading signal, if there is one, the trading signal will be implemented tomorrow during the trading hour. The transaction price is randomly draw from a uniform distribution between low price and high price.

| Indicator |          Asset         | Asset(%) |    Transaction Cost   | Transaction Cost(%) |      Total Reward     | Total Reward(%) |
|:---------:|:----------------------:|:--------:|:---------------------:|:-------------------:|:---------------------:|:---------------:|
|    MACD   |          32.860.583 €  |  109,54% |            376.884 €  |        1,26%        |          2.415.289 €  |      8,05%      |
|    RSI    |          31.514.026 €  |  105,05% |             29.009 €  |        0,10%        |          1.840.355 €  |      6,13%      |
|     SO    |          32.984.360 €  |  109,95% |            112.049 €  |        0,37%        |          3.611.424 €  |      12,04%     |
|    ADX    |          32.836.484 €  |  109,45% |            193.068 €  |        0,64%        |          2.543.383 €  |      8,48%      |
|     AO    |          31.966.300 €  |  106,55% |            198.824 €  |        0,66%        |          1.663.497 €  |      5,54%      |
<p align="right">(<a href="#top">back to top</a>)</p>


<!-- Main Functions TI -->
### Main Functions

The main function lies in ```run.py```. And its functions include:
- Trade stocks according to the signals discovered by indicators
- the indicator visualization. For example, Adidas AG, MACD
![MACD ADS visualization](./images/MACD_ADS_visualization.png)
- the monthly return comparison with [iShares Core DAX UCITS ETF (DE)](https://www.justetf.com/en/etf-profile.html?isin=DE0005933931#exposure).
![MACD ADS monthly return comparison with ETF](./images/MACD_monthly_return.png)
- the yearly return comparison with ETF
![MACD ADS yearly return comparison with ETF](./images/MACD_yearly_return.png)
- the trading behavior visualization
![MACD ADS trading behavior visualization](./images/MACD_ADS_trading.png)
- the detailed trading records (under directory trading_records) of each indicator for each stock

>Description of iShares Core DAX UCITS ETF (DE): The iShares Core DAX UCITS ETF (DE) invests in stocks with focus Germany. The dividends in the fund are reinvested (accumulating). The total expense ratio amounts to 0.16% p.a.. The fund replicates the performance of the underlying index by buying all the index constituents (full replication). The iShares Core DAX UCITS ETF (DE) is a very large ETF with 6,937m Euro assets under management. The ETF is older than 5 years and is domiciled in Germany.

To add more indicators, you need to modify two functions:
```angular2html
get_data       from data_process.py
plot_indicator from visualization.py
```
<p align="right">(<a href="#top">back to top</a>)</p>


<!-- Future Improvements TI -->
### Future Improvements:
- add output final results function
- Twitter the indicators' period and threhold 
- Pass some parameters through terminal, prepare for online deployment
- get rid of config.pre_start_date input
- add longer comparison period such as 5 years
- add more technical indicators, such as Percentage Price Oscillator(PPO), Parabolic SAR, Standard Deviation, Bollinger Bands, Fibonacci Retracement, Williams Percent Range, Commodity Channel Index, Ichimoku Cloud
- Deploy and deliver the application to my website, so the user can enter a technical indicator and obtain its profitability, and the corresponding trading strategy.  
<p align="right">(<a href="#top">back to top</a>)</p>



<!-- DRL Automated Trading -->
## DRL Automated Trading

[DRL_Automated_Trading](https://github.com/JingZhang918/master_thesis/tree/main/DRL_Automated_Trading) project is to train a PPO agent to discover lucrative trading signals for the user.


<!-- Final Results DRL -->
### Finan Results

#### Version 1 - 2021-11-30

The annualized return comparison with ETF:
![DRL yearly return comparison with ETF](./DRL_Automated_Trading/image/yearly_asset_comparison.png)

The monthly return comparison with ETF:
 ![DRL yearly return comparison with ETF](./DRL_Automated_Trading/image/heatmap_diff_asset.png)

 The Imformation Ratio: -0.025

 Based on the observation and analysis above, given the negative information ratio and negative reward return, though, in some months DRL performs better than ETF, it is safe to draw a conclusion that this version of PPO agent does not surmount ETF.


<!-- Main Functions DRL -->
### Main Functions
The main function lies in ```run_11_26.py``` and it has the following functions:
- Train model
- Automatically Trading by the agent
- Output the detailed training records for every stock every day (under directory trading_records)
- Output the yearly asset return comparison with ETF return
![DRL yearly return comparison with ETF](./images/yearly_asset_comparison.png)
- Output the monthly asset return difference with ETF return
![DRL yearly return comparison with ETF](./images/heatmap_diff_asset.png)
- Output the detailed trading behavior of a stock of a specific period
![DRL yearly return comparison with ETF](./images/ADS.DE_2021-05-01_2021-11-01_trading_signal.png)
<p align="right">(<a href="#top">back to top</a>)</p>

<!-- Problems and Solutions DRL -->
### Problems and Solutions
- Environment set up. I use M1 apple silicon and the official release doesn't work. => ✅ solution is provided above.
- The result reproducibility => ✅ wrote the solution in my blog [here](https://jingzhang.tech/index.php/2021/11/20/tutorial-for-drl-hyperparameter-tuning-in-a-custom-environment/)
- Custom environment does not take large parameter. For example, if I use 7 years of data to train the agent, it worked. Yet when
I take 8 years data, it shows no parameter is passed into the environment data error. => ❌ workaround solution: did a little work-around, 
changed the logic from using the accumulating data to train the model to using the latest 5 years
- List saving list into Excel(.xlsx). The terminal output and the saved file does not match. Yet the final answer is correct.
=> ❌  workaround solution: instead of saving ```list```, save ```np.sum(list)```
- Parameter assignment problem. Assign the parameter with ```trading_outlay = config.TRADING_OUTLAY```, where ```config.TRADING_OUTLAY = []```
does not work =>  ❌ workaround solution: ```trading_outlay = []``` works.
- No budget for GPU, so the training hour is really long. Every stock needs to be trained for 5 times and there are 30 stocks in
total. => ❌ No hyper-parameter tuning yet.

**IMPORTANT**: I highly recommend checking every output entry while using Ray. You never know what illogic error might happen.
You might say why not just change to another DRL library [Stable Baseline3](https://github.com/DLR-RM/stable-baselines3). 
SB3 does not support custom environment hyper-parameter tuning. Well there is another workaround, to build everything from
rock bottom on Pytorch. That is really time-consuming. 
<p align="right">(<a href="#top">back to top</a>)</p>

<!-- Future Improvements DRL -->
### Future Improvements:
#### Improvements regarding project
- Add compute information ratio function
- Add compute annualized reward function
- Pass some parameters through terminal, prepare for online deployment
- The visualization of DRL is severely subjected to two manually input parameters. In the future, it would be improved to no input at all.
- There is no saving model and reading model function yet. Due to the lengthy training time, hours or tens of hours or days depending on the tuning parameters, these two functions are of vital.

#### Improvements regarding single stock trading model
- Do hyper-parameter tuning. Keep refining the automated single stock trading model.
- Incorporate material and immaterial release. Cooperation release is an essential factor of stock price change.
- Add more technical indicators. Involve more, for instance, Percentage Price Oscillator(PPO), Parabolic SAR, Standard Deviation,
Bollinger Bands, Fibonacci Retracement, Williams Percent Range, Commodity Channel Index, Ichimoku Cloud, etc.
- Use CNN to recognize trading patterns such as (inverse) hammer, bullish engulfing, etc.
- Consider dividends for long-term trading. The dividend is an important part of income. The expectation of a future dividend affects the current stock price.
- Involve fundamentals, such as P/E, P/C, and so on. How well a company operates determines how worth its stock.
- Add material news that might affect the whole industry.
- Experienced traders' comments should be taken into consideration.
- Do sentiment analysis on financial statements and material information through NLP.
- Apply sentiment analysis also on stock commentators' articles, as well as sector-related news.
- Consider dividends for long-term trading. The dividend is an essential part of income. The expectation of a future dividend affects the current stock price. 
- pair the trading stock with another or several other stocks. Set up an automated multi-stock trading model. Multi-stocks from different sectors or industries could positively affect the agent—for example, pair trading. Pair trading happens to two stocks, usually with one stock rise and another with several lag days. Or with one stock rise and the other stock goes down. 
<p align="right">(<a href="#top">back to top</a>)</p>



<!-- Contact -->
## Contact

Any ideas you wanna share with me, send me an email: jingzhang6057@gmail.com :D

<p align="right">(<a href="#top">back to top</a>)</p>








