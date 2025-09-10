CREATE TABLE [dbo].[Store] (
    [StoreKey]     INT           NOT NULL,
    [StoreCode]    INT           NOT NULL,
    [GeoAreaKey]   INT           NOT NULL,
    [CountryCode]  VARCHAR (50)  NULL,
    [CountryName]  VARCHAR (50)  NULL,
    [State]        VARCHAR (100) NULL,
    [OpenDate]     DATE          NULL,
    [CloseDate]    DATE          NULL,
    [Description]  VARCHAR (100) NULL,
    [SquareMeters] INT           NULL,
    [Status]       VARCHAR (50)  NULL
);


GO

