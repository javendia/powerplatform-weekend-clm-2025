CREATE TABLE [dbo].[Product] (
    [ProductKey]      INT             NOT NULL,
    [ProductCode]     VARCHAR (255)   NOT NULL,
    [ProductName]     VARCHAR (500)   NULL,
    [Manufacturer]    VARCHAR (50)    NULL,
    [Brand]           VARCHAR (50)    NULL,
    [Color]           VARCHAR (20)    NULL,
    [WeightUnit]      VARCHAR (20)    NULL,
    [Weight]          FLOAT (53)      NULL,
    [Cost]            DECIMAL (10, 2) NULL,
    [Price]           DECIMAL (10, 2) NULL,
    [CategoryKey]     INT             NULL,
    [CategoryName]    VARCHAR (30)    NULL,
    [SubCategoryKey]  INT             NULL,
    [SubCategoryName] VARCHAR (50)    NULL
);


GO

