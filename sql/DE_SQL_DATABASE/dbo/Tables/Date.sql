CREATE TABLE [dbo].[Date] (

	[Date] date NOT NULL, 
	[DateKey] varchar(50) NOT NULL, 
	[Year] int NOT NULL, 
	[YearQuarter] varchar(30) NOT NULL, 
	[YearQuarterNumber] int NOT NULL, 
	[Quarter] varchar(2) NOT NULL, 
	[YearMonth] varchar(30) NOT NULL, 
	[YearMonthShort] varchar(30) NOT NULL, 
	[YearMonthNumber] int NOT NULL, 
	[Month] varchar(30) NOT NULL, 
	[MonthShort] varchar(30) NOT NULL, 
	[MonthNumber] int NOT NULL, 
	[DayofWeek] varchar(30) NOT NULL, 
	[DayofWeekShort] varchar(30) NOT NULL, 
	[DayofWeekNumber] int NOT NULL, 
	[WorkingDay] bit NOT NULL, 
	[WorkingDayNumber] int NOT NULL
);