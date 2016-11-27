SELECT Country.Name FROM Country, City WHERE Country.Code =  City.CountryCode GROUP BY Country.Name HAVING 2 * sum(City.Population) < Country.Population ORDER BY Country.Name;
