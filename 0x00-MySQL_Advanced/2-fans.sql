-- SQL script that ranks country origins of bands, ordered by the number of (non-unique) fans

-- Column names must be: origin and nb_fans
SELECT origin, SUM(fans) as total_fans
FROM metal_bands
GROUP BY origin
HAVING COUNT(origin) > 1
ORDER BY total_fans DESC
LIMIT 50;
