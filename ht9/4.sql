SELECT Country.Name, count(CASE WHEN Country.Code = City.CountryCode AND City.Population >= 1000000 THEN 1 ELSE NULL END) cnt
FROM Country, City
GROUP BY Country.Name
ORDER BY cnt desc, Country.Name;
