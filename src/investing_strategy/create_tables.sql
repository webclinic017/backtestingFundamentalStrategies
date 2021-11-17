create table resultadosBacktestingStocks(
metodo varchar(100),
per1 double,
fecha date,
exchange varchar(100),
ratio varchar(100),
parametro double,
profit double,
numFechasEntrada int,
numFechasSalida int,
numFechasTotales int,
PRIMARY KEY (metodo,fecha, exchange, ratio, parametro)
)
