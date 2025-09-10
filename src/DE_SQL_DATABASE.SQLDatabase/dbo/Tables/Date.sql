CREATE TABLE [dbo].[Date] (
    [Date]              DATE         NOT NULL,
    [DateKey]           VARCHAR (50) NOT NULL,
    [Year]              INT          NOT NULL,
    [YearQuarter]       VARCHAR (30) NOT NULL,
    [YearQuarterNumber] INT          NOT NULL,
    [Quarter]           VARCHAR (2)  NOT NULL,
    [YearMonth]         VARCHAR (30) NOT NULL,
    [YearMonthShort]    VARCHAR (30) NOT NULL,
    [YearMonthNumber]   INT          NOT NULL,
    [Month]             VARCHAR (30) NOT NULL,
    [MonthShort]        VARCHAR (30) NOT NULL,
    [MonthNumber]       INT          NOT NULL,
    [DayofWeek]         VARCHAR (30) NOT NULL,
    [DayofWeekShort]    VARCHAR (30) NOT NULL,
    [DayofWeekNumber]   INT          NOT NULL,
    [WorkingDay]        BIT          NOT NULL,
    [WorkingDayNumber]  INT          NOT NULL
);


GO

