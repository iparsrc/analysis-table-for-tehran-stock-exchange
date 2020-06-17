# analysis-table-for-tehran-stock-exchange
A table that contains beta, covariance, standard deviation, total return and cv values for different periods for all stocks in Tehran's stock exchange.<br/><br/>
This is a web based application made with django web framework.<br/>
It contains a control page for the admin user that is used to update different parts of the table.<br/>
All updates for table data can be done with only one button by admin user, and application will go through below steps:<br/>
**1. Catching updated daily data** for all stocks in the list and index from [tsetmc.com](http://tsetmc.com)<br/>
**2. Syncing stocks with index values.**<br/>
**3. Calculating beta, cov, sd, toatl return, cv values for differnet periods.**<br/>
**4. Exporting calculated values to csv files.**<br/>
**5. Building and serving the table using csv files for that day.**<br/><br/>
This programme is made with: **python, django, pandas, html, css, js, d3.js**<br/>
