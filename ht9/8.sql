SELECT Country.Name, Country.Population, Country.SurfaceArea FROM Country
INNER JOIN Capital FindCapitalCity ON Country.Code = FindCapitalCity.CountryCode
INNER JOIN City CompC ON CompC.Id = FindCapitalCity.CityId
INNER JOIN City Oth ON Oth.CountryCode = Country.Code AND Oth.Id <> CompC.Id
GROUP BY Country.Name
HAVING max(Oth.Population) > CompC.Population
ORDER BY (1.0 * Country.Population) / Country.SurfaceArea desc, Country.Name;
