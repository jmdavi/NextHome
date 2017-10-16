WITH books AS (
SELECT City, count(name) AS shop_ct, GROUP_CONCAT(name,',') AS books_nearby, review_count, avg(rating) AS ratings
FROM shops_distinct
GROUP BY City, categories like '%book%' HAVING categories LIKE '%book%'
),
vege AS (
SELECT City, count(name) AS shop_ct, GROUP_CONCAT(name,',') AS vege_nearby, review_count, avg(rating) AS ratings
FROM shops_distinct
GROUP BY City, categories LIKE '%vege%' HAVING categories LIKE '%vege%'
)
SELECT t.city, t.car_time_text, t.transit_time_text, t.car_dis_text
, books.shop_ct, books.books_nearby, books.ratings
, vege.shop_ct, vege.vege_nearby, vege.ratings
FROM travel_times AS t
LEFT OUTER JOIN books ON t.city = books.city
LEFT OUTER JOIN vege ON t.city = vege.city 
WHERE t.car_time_sec < 3600