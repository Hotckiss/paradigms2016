SELECT Country.GovernmentForm, sum(Country.SurfaceArea) FROM Country GROUP BY GovernmentForm ORDER BY sum(Country.SurfaceArea) desc limit 1;
