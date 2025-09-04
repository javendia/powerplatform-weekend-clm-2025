CREATE TABLE [dbo].[Store] (

	[StoreKey] int NOT NULL, 
	[StoreCode] int NOT NULL, 
	[GeoAreaKey] int NOT NULL, 
	[CountryCode] varchar(50) NULL, 
	[CountryName] varchar(50) NULL, 
	[State] varchar(100) NULL, 
	[OpenDate] date NULL, 
	[CloseDate] date NULL, 
	[Description] varchar(100) NULL, 
	[SquareMeters] int NULL, 
	[Status] varchar(50) NULL
);