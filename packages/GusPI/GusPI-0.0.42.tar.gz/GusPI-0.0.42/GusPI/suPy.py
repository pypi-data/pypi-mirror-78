import math
from datetime import datetime, time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from fbprophet import Prophet

def prep_dataframe(file):
    sales = pd.read_csv(file)
    sales['ref'] = sales['ref'].astype('category')
    sales['date'] = pd.to_datetime(sales['date'],  errors='coerce')
    sales['product_number'] = sales['product_number'].astype('category')
    sales['product_name'] = sales['product_name'].astype('category')
    return sales
    

def EOQ(demand, mean, STD, C, Ce, Cs, Ct):
  Qs=math.sqrt(2*Ct*demand/Ce)
  Ts=Qs/demand
  Ns=1/Ts
  TRC=Ct*(demand/Qs)+Ce*(Qs/2)
  TC=C*demand+TRC

  return TC

  #print("Qs: " + str(Qs))
  #print("Ts: " + str(Ts))
  #print("Ns: " + str(Ns))
  #print("TRC: " + str(TRC))
  #print("TC: " + str(TC))

def POM(TotalOrders, ErrorOrders):
  #Perfect Order Measurement; the percentage of orders that are error-free.

  r=round(((TotalOrders-ErrorOrders)/TotalOrders),4)
  return r
  #print("Perfect Order Measurement: " + str(r))

def FR(TotalItems, ShippedItems):
  #Fill Rate
  #The percentage of a customer’s order that is filled on the first shipment. This can be represented as the percentage of items, SKUs or order value that is included with the first shipment.
  r=round((1-((TotalItems-ShippedItems)/TotalItems)),4)
  return r
  #print("Fill Rate: " + str(r))

def IDS(InventoryOnHand,AvgDailyUsage):
  #Inventory Days of Supply
  #The number of days it would take to run out of supply if it was not replenished.
  r=round(InventoryOnHand/AvgDailyUsage,4)
  return r
  #print("Inventory Days of Supply: " + str(r))

def FCU(TotalFreightCost,NumberOfItems):
  #Freight cost per unit
  #Usually measured as the cost of freight per item or SKU.
  r=round(TotalFreightCost/NumberOfItems,4)
  return r
  #print("Freight cost per unit: " + str(r))

def IT(COGS,AvgInventory):
  #Inventory Turnover
  #The number of times that a company’s inventory cycles per year.
  r=round(COGS/AvgInventory,4)
  return r
  #print("Inventory Turnover: " + str(r))

def DOS(AvgInventory,MonthlyDemand):
  #Days of Supply (DOS)
  #DOS is the most common KPI used by managers in measuring the efficiency in supply chain.
  r=round(AvgInventory/MonthlyDemand,4)*30
  return r
  #print("Days of Supply (DOS): " + str(r))

def GMROI(GrossProfit, OpeningStock, ClosingStock):
  #Gross Margin Return on Investment (GMROI)
  #GMROI represents the amount of gross profit earned for every AED (or $, £, €, ₺) of the average investment made in inventory.
  r=round(GrossProfit/((OpeningStock-ClosingStock)/2),4)*100
  return r
  #print("Gross Margin Return on Investment (GMROI): " + str(r))

def IA(ItemCounts, TotalItemCounts):
  #Inventory Accuracy
  #Inventory accuracy is used to calculate the accuracy of your inventory.
  r=round((ItemCounts/TotalItemCounts),4)
  return r
  #print("Inventory Accuracy: " + str(r))
  
def SUR(InventoryCube, TotalWarehouseCube):
  #Storage Utilization Rate
  #Storage utilization rate reflects how efficiently you are utilizing the amount of available space in your warehouse or distribution center.
  r=round((InventoryCube/TotalWarehouseCube),4)*100
  return r
  #print("Storage Utilization Rate: " + str(r))
  
def TOCT(TimeOrderReceivedbyCustomer, TimeOrderPlaced,TotalNumberofOrdersShipped):
  #Total Order Cycle Time
  #Total order cycle time reflects the average length of time that passes between a customer placing an order and the order being shipped.
  date1 = datetime.strptime(TimeOrderPlaced, '%Y-%m-%d')
  date2 = datetime.strptime(TimeOrderReceivedbyCustomer, '%Y-%m-%d')
  timedelta = date2 - date1
  r=round(timedelta.days/TotalNumberofOrdersShipped,4)
  return r
  #print("Total Order Cycle Time: " + str(r))
  
def IOCT(TimeOrderShipped, TimeOrderReceived, NumberofOrdersShipped):
  #Date format: %Y-%m-%d; "2015-01-05"
  #Internal Order Cycle Time
  #Internal order cycle time reflects the average amount of time that it takes from the moment that a customer order is released into the warehouse for processing and the moment that the order is shipped.
  date1 = datetime.strptime(TimeOrderShipped, '%Y-%m-%d')
  date2 = datetime.strptime(TimeOrderReceived, '%Y-%m-%d')
  timedelta = date2 - date1
  r=round(timedelta.days/NumberofOrdersShipped,4)
  return r
  #print("Internal Order Cycle Time: " + str(r))

def lineplotQtyByMonth(file,product_number):
    sales = prep_dataframe(file)
    sales = sales.loc[sales['product_number'] == product_number]
    sales_qty = sales[['date','quantity']]
    sales_qty = sales_qty.set_index(["date"])
    sales_qty = sales_qty.resample('M').sum()
    sales_qty = sales_qty.reset_index()
    plt.figure(figsize=(20,9))
    sns.lineplot(data=sales_qty, x='date',y='quantity').set_title(product_number)
    
def lineplotTotalCostByMonth(file,product_number):
    sales = prep_dataframe(file)
    sales['total_cost'] = sales['quantity']*sales['cost']
    sales = sales.loc[sales['product_number'] == product_number]
    sales_qty = sales[['date','total_cost']]
    sales_qty = sales_qty.set_index(["date"])
    sales_qty = sales_qty.resample('M').sum()
    sales_qty = sales_qty.reset_index()
    plt.figure(figsize=(20,9))
    sns.lineplot(data=sales_qty, x='date',y='total_cost').set_title(product_number)
    
def lineplotTotalSalesByMonth(file,product_number):
    sales = prep_dataframe(file)
    sales['total_sales'] = sales['quantity']*sales['price']
    sales = sales.loc[sales['product_number'] == product_number]
    sales_qty = sales[['date','total_sales']]
    sales_qty = sales_qty.set_index(["date"])
    sales_qty = sales_qty.resample('M').sum()
    sales_qty = sales_qty.reset_index()
    plt.figure(figsize=(20,9))
    sns.lineplot(data=sales_qty, x='date',y='total_sales').set_title(product_number)

def lineplotAverageCostByMonth(file,product_number):
    sales = prep_dataframe(file)
    sales = sales.loc[sales['product_number'] == product_number]
    sales_qty = sales[['date','cost']]
    sales_qty = sales_qty.set_index(["date"])
    sales_qty = sales_qty.resample('M').mean()
    sales_qty = sales_qty.reset_index()
    plt.figure(figsize=(20,9))
    sns.lineplot(data=sales_qty, x='date',y='cost').set_title(product_number)
    
def lineplotAverageSalesPriceByMonth(file,product_number):
    sales = prep_dataframe(file)
    sales = sales.loc[sales['product_number'] == product_number]
    sales_qty = sales[['date','price']]
    sales_qty = sales_qty.set_index(["date"])
    sales_qty = sales_qty.resample('M').mean()
    sales_qty = sales_qty.reset_index()
    plt.figure(figsize=(20,9))
    sns.lineplot(data=sales_qty, x='date',y='price').set_title(product_number)
    
def basicSafetyStock(file,productNumber,safetyDays,leadTimeinDays):
    sales = prep_dataframe(file)
    sales = sales.loc[sales['product_number'] == productNumber]
    sales_qty = sales.set_index(["date"])
    sales_qty = sales_qty.reset_index()
    avg_sales = sales_qty.quantity.mean()
    safety_stock = avg_sales*safetyDays
    reorder_point = safety_stock+avg_sales*leadTimeinDays
    print("Safety Stock: "+str(safety_stock))
    print("Reorder Point: "+str(reorder_point))
    
def basicSafetyStockList(file,safetyDays,leadTime):
    sales = prep_dataframe(file)
    pd.set_option('display.float_format', lambda x: '%.2f' % x)
    result = pd.DataFrame(columns=['product_number', 'product_name', 'safety_stock', 'reorder_point'])
    for pnum in sales.product_number.unique():
        sales_prep = sales.loc[sales['product_number'] == pnum]
        sales_qty = sales_prep.set_index(["date"])
        sales_qty = sales_qty.reset_index()
        avg_sales = sales_qty.quantity.mean()
        safety_stock = avg_sales*safetyDays
        reorder_point = safety_stock+avg_sales*leadTime
        result = result.append({'product_number': pnum, 'product_name': sales_prep['product_name'].iloc[0], 'safety_stock': safety_stock, 'reorder_point':reorder_point}, ignore_index=True)
    result.to_csv('basicSafetyStock.csv')
    print("Saftey Stock and reorder point with basic method", result, sep='\n')
    
def safetyStockwtServiceRate(file,productNumber,serviceRate,leadTimeInDays):
    sales = prep_dataframe(file)
    sales = sales.loc[sales['product_number'] == productNumber]
    sales_qty = sales.set_index(["date"])
    sales_qty = sales_qty.reset_index()
    sales_qty = sales_qty[['quantity']]
    avg_sales = sales_qty.quantity.mean()
    std = sales_qty.quantity.std()
    servZ = norm.ppf(serviceRate)
    LT_sqrt = math.sqrt(leadTimeInDays/30)
    safety_stock = servZ*std*LT_sqrt
    reorder_point = safety_stock+avg_sales*leadTimeInDays
    print("Safety Stock: "+str(safety_stock))
    print("Reorder Point: "+str(reorder_point))
    
def safetyStockwtServiceRateList(file,serviceRate,leadTimeInDays):
    sales = prep_dataframe(file)
    result = pd.DataFrame(columns=['product_number', 'product_name', 'safety_stock', 'reorder_point'])
    for pnum in sales.product_number.unique():
        sales_prep = sales.loc[sales['product_number'] == pnum]
        sales_qty = sales_prep.set_index(["date"])
        sales_qty = sales_qty.reset_index()
        sales_qty = sales_qty[['quantity']]
        avg_sales = sales_qty.quantity.mean()
        std = sales_qty.quantity.std()
        servZ = norm.ppf(serviceRate)
        LT_sqrt = math.sqrt(leadTimeInDays/30)
        safety_stock = servZ*std*LT_sqrt
        reorder_point = safety_stock+avg_sales*leadTimeInDays
        result = result.append({'product_number': pnum, 'product_name': sales_prep['product_name'].iloc[0], 'safety_stock': safety_stock, 'reorder_point':reorder_point}, ignore_index=True)
    result.to_csv('ServiceRateSafetyStock.csv')
    print("Saftey Stock with service rate method method", result, sep='\n')
    
def cvPerProduct(file,product_number):
    sales = prep_dataframe(file)
    sales = sales.loc[sales['product_number'] == product_number]
    sales_qty = sales[['date','quantity']]
    sales_qty = sales_qty.set_index(["date"])
    sales_qty = sales_qty.resample('D').mean()
    cv = sales_qty.quantity.std()/sales_qty.quantity.mean()
    print('Coefficient of Variation')
    print(cv)
    
def linearRegressionPerProduct(file,product_number):
    sales = prep_dataframe(file)
    sales = sales.loc[sales['product_number'] == product_number]
    X = sales['quantity'].values.reshape(-1,1)
    y = sales['price'].values.reshape(-1,1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    regressor = LinearRegression()  
    regressor.fit(X_train, y_train)
    #To retrieve the intercept:
    print('Intercept:', regressor.intercept_)
    #For retrieving the slope:
    print('Slope:', regressor.coef_)
    y_pred = regressor.predict(X_test)
    print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
    print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
    print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
    plt.scatter(X_test, y_test,  color='gray')
    plt.plot(X_test, y_pred, color='red', linewidth=2)
    plt.show()
    
def eoqPerProduct(file,product_number,setupCost,holdingCost):
    sales = prep_dataframe(file)
    sales = sales.loc[sales['product_number'] == product_number]
    sales_qty = sales[['date','quantity']]
    sales_qty = sales_qty.set_index(["date"])
    sales_qty = sales_qty.resample('Y').sum()
    avg_qty = sales_qty.quantity.mean()
    EOQ = math.sqrt(2*avg_qty*setupCost/holdingCost)
    print('EOQ :', EOQ)
    
def avgQtySoldList(file):
    sales = prep_dataframe(file)
    sales = sales.dropna()
    pd.set_option('display.float_format', lambda x: '%.2f' % x)
    result = pd.DataFrame(columns=['product_number', 'product_name', 'QTY Sold by Year'])
    for pnum in sales.product_number.unique():
        sales_prep = sales.loc[sales['product_number'] == pnum]
        sales_qty = sales_prep[['date','quantity']]
        sales_qty = sales_qty.set_index(["date"])
        sales_qty = sales_qty.resample('Y').sum()
        avg_qty = sales_qty.quantity.mean()
        result = result.append({'product_number': pnum, 'product_name': sales_prep['product_name'].iloc[0], 'QTY Sold by Year': avg_qty}, ignore_index=True)
    result.to_csv('avgQtySoldList.csv')
    print("Average Quantity Sold Per Year", result, sep='\n')
    
# def purchasingMetricList(salesData,eoqCost,serviceRate):
#     sales = pd.read_csv(salesData)
#     eoqCost = pd.read_csv(eoqCost)
#     sales['ref'] = sales['ref'].astype('category')
#     sales['date'] = pd.to_datetime(sales['date'],  errors='coerce')
#     sales['product_number'] = sales['product_number'].astype('category')
#     sales['product_name'] = sales['product_name'].astype('category')
#     sales = sales.dropna()
#     result = pd.DataFrame(columns=['product_number', 'product_name', 'avg_qty_sold', 'setup_cost', 'holding_cost', 'leadtimeInDays', 'safety_stock', 'reorder_point', 'EOQ'])
#     for pnum in eoqCost.product_number.unique():
#         sales_prep = sales.loc[sales['product_number'] == pnum]
#         sales_qty = sales_prep[['date','quantity']]
#         sales_qty = sales_qty.set_index(["date"])
#         sales_qty = sales_qty.resample('Y').sum()
#         avg_qty = sales_qty.quantity.mean()
#         mergedDF = sales_prep.merge(eoqCost, on='product_number', how='right')
#         safety_stock = norm.ppf(serviceRate)*np.std(sales_qty.quantity)*np.sqrt(mergedDF.leadtimeInDays.mean()/30)
#         reorder_point = safety_stock+avg_qty*mergedDF.leadtimeInDays.mean()
#         EOQ = math.sqrt(2*avg_qty*mergedDF.setup_cost.mean()/mergedDF.holding_cost.mean())
#         result = result.append({'product_number': pnum, 'product_name': sales_prep['product_name'].iloc[0], 'avg_qty_sold': avg_qty, 'setup_cost': mergedDF['setup_cost'].iloc[0], 'holding_cost': mergedDF['holding_cost'].iloc[0], 'leadtimeInDays': mergedDF['leadtimeInDays'].iloc[0], 'safety_stock': safety_stock, 'reorder_point': reorder_point, 'EOQ': EOQ}, ignore_index=True)
#     result.to_csv('PurchasingMetrics.csv')
#     print("Purchasing Metrics", result, sep='\n')
    
def seasonalityIndexPerProduct(file,product_number,year):
    sales = prep_dataframe(file)
    sales['total_amount'] = sales['quantity']*sales['price']
    sales = sales.loc[sales['product_number'] == product_number]
    sales['year'] = pd.DatetimeIndex(sales['date']).year
    sales['month'] = pd.DatetimeIndex(sales['date']).month
    sales_amount = sales.set_index(["date"])
    sales_amount = sales_amount.reset_index()
    sales_amount = sales_amount[['year','month','total_amount']]
    sales_amount_year = sales_amount.loc[sales_amount['year'] == year]
    seationality_index_year = sales_amount_year.groupby(['month']).sum()
    seationality_index_year['seasonality_index'] = seationality_index_year['total_amount']/seationality_index_year.total_amount.sum()
    seationality_index_year['year'] = year
    seationality_index_year.reset_index()
    seationality_index_year.to_csv('SeasonalityIndexPerProduct.csv')
    print("Seasonality Index Per Product", seationality_index_year, sep='\n')
    
def forecastQtyMonthlySales(file,product_number,months):
    sales = prep_dataframe(file)
    forecastDF = sales.loc[sales['product_number'] == product_number]
    forecastDF['sales'] = forecastDF['price']*forecastDF['quantity']
    forecastDF = forecastDF[['date','sales']]
    forecastDF['index'], forecastDF['month_year'] = pd.to_datetime(forecastDF['date']).dt.to_period('M'), pd.to_datetime(forecastDF['date']).dt.to_period('M')
    forecastDF = forecastDF[['index','month_year','sales']]
    forecastDF.set_index('index', inplace=True)
    forecastDF = forecastDF.groupby('month_year', as_index=False).agg({"sales": "sum"})
    forecastDF = forecastDF.rename(index=str, columns={"sales": "y", "month_year": "ds"})
    forecastDF['ds'] = forecastDF.ds.values.astype('datetime64[M]')
    bev_model = Prophet(interval_width=0.95)
    bev_model.fit(forecastDF)
    future_dates = bev_model.make_future_dataframe(periods=months, freq='M')
    forecast = bev_model.predict(future_dates)
    print('Forecast Metrics: ')
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(months))
    print('Forecast Graph: ')
    bev_model.plot(forecast, uncertainty=True);
    
def forecastMonthlyPrice(file,product_number,months):
    sales = prep_dataframe(file)
    forecastDF = sales.loc[sales['product_number'] == product_number]
    forecastDF = forecastDF[['date','price']]
    forecastDF['index'], forecastDF['month_year'] = pd.to_datetime(forecastDF['date']).dt.to_period('M'), pd.to_datetime(forecastDF['date']).dt.to_period('M')
    forecastDF = forecastDF[['index','month_year','price']]
    forecastDF.set_index('index', inplace=True)
    forecastDF = forecastDF.groupby('month_year', as_index=False).agg({"price": "mean"})
    forecastDF = forecastDF.rename(index=str, columns={"price": "y", "month_year": "ds"})
    forecastDF['ds'] = forecastDF.ds.values.astype('datetime64[M]')
    bev_model = Prophet(interval_width=0.95)
    bev_model.fit(forecastDF)
    future_dates = bev_model.make_future_dataframe(periods=months, freq='M')
    forecast = bev_model.predict(future_dates)
    print('Forecast Metrics: ')
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(months))
    print('Forecast Graph: ')
    bev_model.plot(forecast, uncertainty=True);
    
def forecastMonthlyCost(file,product_number,months):
    sales = prep_dataframe(file)
    forecastDF = sales.loc[sales['product_number'] == product_number]
    forecastDF = forecastDF[['date','cost']]
    forecastDF['index'], forecastDF['month_year'] = pd.to_datetime(forecastDF['date']).dt.to_period('M'), pd.to_datetime(forecastDF['date']).dt.to_period('M')
    forecastDF = forecastDF[['index','month_year','cost']]
    forecastDF.set_index('index', inplace=True)
    forecastDF = forecastDF.groupby('month_year', as_index=False).agg({"cost": "mean"})
    forecastDF = forecastDF.rename(index=str, columns={"cost": "y", "month_year": "ds"})
    forecastDF['ds'] = forecastDF.ds.values.astype('datetime64[M]')
    bev_model = Prophet(interval_width=0.95)
    bev_model.fit(forecastDF)
    future_dates = bev_model.make_future_dataframe(periods=months, freq='M')
    forecast = bev_model.predict(future_dates)
    print('Forecast Metrics: ')
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(months))
    print('Forecast Graph: ')
    bev_model.plot(forecast, uncertainty=True);