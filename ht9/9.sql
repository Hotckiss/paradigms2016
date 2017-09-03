SELECT A.Year, B.Year, Country.Name, (A.Rate - B.Rate) / (A.Year - B.Year) FROM Country
INNER JOIN LiteracyRate A ON Country.Code = A.CountryCode
INNER JOIN LiteracyRate B ON Country.Code = B.CountryCode
GROUP BY Country.Name, A.Year, B.Year
HAVING min(B.Year) > A.Year 
ORDER BY (A.Rate - B.Rate) / (A.Year - B.Year) desc;
