SELECT City.Name FROM Country, City, Capital WHERE City.Id = Capital.CityId AND City.CountryCode = Country.Code AND Country.Name LIKE "Malaysia";
