import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import plotly.graph_objects as go

def prep_dataframe(file):
    pd.set_option('display.float_format', lambda x: '%.2f' % x)
    statement = pd.read_csv(file)
    statement.Breakdown = statement.Breakdown.str.replace(' ', '_')
    statement.Breakdown = statement.Breakdown.str.replace(',', '')
    statement.Breakdown = statement.Breakdown.str.replace('&', '')
    statement['Breakdown'] = statement['Breakdown'].str.lower()
    statement = statement.set_index('Breakdown')
    statement=statement.abs()
    return statement


def printStatement(file):
    statement = prep_dataframe(file)
    print(statement)


def lineplot(file,category):
    statement = prep_dataframe(file)

    plotData = statement.T
    plotData = plotData.reset_index()
    plotData['index']= pd.to_datetime(plotData['index']) 
    plotData = plotData.sort_values(by='index')
    plotData = plotData[['index',category]]

    plt.figure(figsize=(20,9))
    sns.lineplot(data=plotData, x='index',y=category)

def multiLineplot(file,title):
    statement = prep_dataframe(file)

    plotData = statement.T
    plotData = plotData.reset_index()
    plotData['index']= pd.to_datetime(plotData['index'])
    plotData = plotData.sort_values(by='index')

    columnsList = list(plotData.columns.values)
    graphRowCount=math.ceil(len(plotData.columns)/3)
    fig = plt.figure(figsize=(30,45))
    fig.suptitle(title, fontsize=30)

    for x in range(1, len(columnsList)):
        plotNumber = 'ax'+str(x)
        colname = plotData.columns[x]

        plotNumber = fig.add_subplot(graphRowCount,3,x)
        plotNumber.set_title(colname)
        plotNumber.plot(plotData['index'],
             plotData[colname])
        plt.xticks(rotation=45)

    plt.show()

def calculateMetrics(balanceSheet,incomeStatement):

    balanceSheet = pd.read_csv(balanceSheet)
    incomeStatement = pd.read_csv(incomeStatement)

    balanceSheet.Breakdown = balanceSheet.Breakdown.str.replace(' ', '_')
    balanceSheet.Breakdown = balanceSheet.Breakdown.str.replace(',', '')
    balanceSheet.Breakdown = balanceSheet.Breakdown.str.replace('&', '')
    incomeStatement.Breakdown = incomeStatement.Breakdown.str.replace(' ', '_')
    incomeStatement.Breakdown = incomeStatement.Breakdown.str.replace(',', '')
    incomeStatement.Breakdown = incomeStatement.Breakdown.str.replace('&', '')
    balanceSheet['Breakdown'] = balanceSheet['Breakdown'].str.lower()
    incomeStatement['Breakdown'] = incomeStatement['Breakdown'].str.lower()
    balanceSheet = balanceSheet.set_index('Breakdown')
    incomeStatement = incomeStatement.set_index('Breakdown')
    balanceSheet=balanceSheet.abs()
    incomeStatement=incomeStatement.abs()

    frames = [balanceSheet, incomeStatement]
    Ratio = pd.DataFrame()
    dataframeForRatio = pd.concat(frames)
    dataframeForRatio = dataframeForRatio.drop_duplicates()
    dataframeForRatio = dataframeForRatio.T
    dataframeForRatio['average_inventory'] = dataframeForRatio['inventory'].mean()
    dataframeForRatio['average_accounts_receivable'] = dataframeForRatio['net_receivables'].mean()

    #Liquidity Ratios
    Ratio['quick_ratio'] = (dataframeForRatio['cash_and_cash_equivalents']+dataframeForRatio['net_receivables']+dataframeForRatio['short_term_investments'])/dataframeForRatio['total_current_liabilities']
    Ratio['acid-test_ratio'] = dataframeForRatio['total_current_assets']/dataframeForRatio['total_current_liabilities']
    Ratio['cash_ratio'] = (dataframeForRatio['total_current_assets']-dataframeForRatio['inventory'])/dataframeForRatio['total_current_liabilities']

    #Leverage Financial Ratios
    Ratio['debt_ratio'] = dataframeForRatio['total_liabilities']/(dataframeForRatio['total_assets']-dataframeForRatio['total_liabilities'])
    Ratio['interest_coverage_ratio'] = dataframeForRatio['gross_profit']/dataframeForRatio['interest_expense']
    #Ratio['debt_service_coverage_ratio'] = dataframeForRatio['gross_profit']/dataframeForRatio['']

    #Efficiency Ratios
    Ratio['asset_turnover_ratio'] = dataframeForRatio['total_revenue']/dataframeForRatio['total_assets']
    Ratio['inventory_turnover_ratio'] = dataframeForRatio['cost_of_revenue']/dataframeForRatio['average_inventory']
    Ratio['receivables_turnover_ratio'] = dataframeForRatio['total_revenue']/dataframeForRatio['average_accounts_receivable']
    Ratio['days_sales_in_inventory_ratio'] = 365/Ratio['inventory_turnover_ratio']

    #Profitability Ratios
    Ratio['gross_margin_ratio'] = dataframeForRatio['gross_profit']/dataframeForRatio['total_revenue']
    Ratio['operating_margin_ratio'] = dataframeForRatio['net_income']/dataframeForRatio['total_revenue']
    Ratio['return_on_assets_ratio'] = dataframeForRatio['net_income']/dataframeForRatio['total_revenue']
    Ratio['return_on_equity_ratio'] = dataframeForRatio['net_income']/(dataframeForRatio['total_revenue']-dataframeForRatio['total_liabilities'])

    Ratio = Ratio.T
    Ratio = Ratio.round(4)
    print(Ratio)
    
def bulletChart(file,item):
    statement = prep_dataframe(file)
    
    data = statement.T
    data = data.reset_index()
    data = data.sort_values(by='index', ascending=False)
    avg_item = 'avg_'+item
    data[avg_item] = data[item].mean()
    data = data.round(2)
    data = data.iloc[0]
    
    fig = go.Figure(go.Indicator(
        mode = "number+gauge+delta",
        gauge = {'shape': "bullet"},
        value = data[item],
        delta = {'reference': data[avg_item]},
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': item}))
    fig.update_layout(height = 250)
    
    fig.show()

def horizontalAnalysisLastTwo(file):
    statement = prep_dataframe(file)
    statement = statement.reindex(sorted(statement.columns), axis=1)
    statement_lastPeriods = statement[statement.columns[-2:]]
    statement_lastPeriods_lastColName = statement[statement_lastPeriods.columns[-1:]].columns.values[0]
    statement_lastPeriods_secondLastColName = statement[statement_lastPeriods.columns[-2:-1]].columns.values[0]
    statement_lastPeriods['Amount(Increased/Decreased)'] = statement_lastPeriods[statement_lastPeriods_lastColName]-statement_lastPeriods[statement_lastPeriods_secondLastColName]
    statement_lastPeriods['Percentage(Increased/Decreased)'] = (statement_lastPeriods[statement_lastPeriods_lastColName]/statement_lastPeriods[statement_lastPeriods_secondLastColName])-1
    statement_lastPeriods = statement_lastPeriods.dropna()
    statement_lastPeriods['Percentage(Increased/Decreased)'] = pd.Series(["{0:.2f}%".format(val * 100) for val in statement_lastPeriods['Percentage(Increased/Decreased)']], index = statement_lastPeriods.index)
    statement_lastPeriods.to_csv('horizontalAnalysisLastTwo.csv')
    print("Horizontal Analysis with Last two Periods", statement_lastPeriods, sep='\n')
