SELECT Country.Name, LiteracyRate.Rate FROM Country INNER JOIN LiteracyRate ON Country.Code = LiteracyRate.CountryCode 
GROUP BY Country.Name HAVING max(LiteracyRate.Year) ORDER BY LiteracyRate.Rate desc limit 1; 
