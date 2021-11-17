In this repository there is a proyect to backtest forex strategies using rules based in prizes and Investing calendar events.
Default version is used using moving averages on manufacturing pmi and cpi, and sharpe ratio of 0.8 is achieved.
You can change symbols,initial capital, size per order ...
	DATA DIRECTORY
In data directory there is a file with forex symbols names and other files with daily forex data from different symbols since 2010 until 2021.
	MYSQL DATABASE
Despite forex data is saved in files, events data from investing is saved in database. MYSQL table must be created with the script src/investing_strategy/create_tables.sql and data from investing can be saved in the database with src/insert_investing.
Check date since data from investing is saved and date until data from investing is saved. Remember that if data from data directory is used without expanding it only events since 2010 from investing are needed.
MYSQL credentials must be set in src/investing_strategy/bd to connet to database.
	SAVE LINES
With src/save_lines you can choose which lines of events to load from investing from each symbol. Line names would be checked in database between '%' characters, so you dont have to write it exactly. Example: cpi, ism manufacturing pmi ...
Line names will be checked first with high importance in investing and then with medium importance if high fails. To save events with different importance modify src/insert_investing file. In this version yo must save same number of lines for each currency and its against currencies (example, EUR must have same number of lines as USD if you use EUR_USD).
	BACKTRADER
In src/backtrader you can configure which symbols to use in backtesting, which must  be included in src/save_lines and saved in lines.json before backtrader execution. You can also configure dates for simulation, and use optimization or not.
If errors ocurr when changing to optimization be sure that print and log params in strategy params are set to False.
	STRATGY
src/investing/strategy/ is the directory of strategy implementation.
	ANALIZING RESULTS
If you use optimization, you can check results visually using analizeResults (results directory in src/investing_strategy/ must be created).

The good strategy is strategy 5.
