CREATE TABLE [dbo].[Product] (

	[ProductKey] int NOT NULL, 
	[ProductCode] varchar(255) NOT NULL, 
	[ProductName] varchar(500) NULL, 
	[Manufacturer] varchar(50) NULL, 
	[Brand] varchar(50) NULL, 
	[Color] varchar(20) NULL, 
	[WeightUnit] varchar(20) NULL, 
	[Weight] float NULL, 
	[Cost] decimal(10,2) NULL, 
	[Price] decimal(10,2) NULL, 
	[CategoryKey] int NULL, 
	[CategoryName] varchar(30) NULL, 
	[SubCategoryKey] int NULL, 
	[SubCategoryName] varchar(50) NULL
);