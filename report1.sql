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

--import caused these values for rating we'd like to see as null
UPDATE google_places_distinct
SET rating=null
WHERE length(rating)<1

UPDATE yelp_shops_distinct
SET rating=null
WHERE rating=0.0 and review_count=0

--
CREATE TABLE "nexthome_master" ( `town` TEXT, `commute_optum` TEXT, `rest_num` INTEGER, `great_rest_num` INTEGER, `rest_avg_rating` REAL, `yelp_vege_avg` REAL, `syn_num` INTEGER, `great_syn_num` INTEGER, `syn_avg_rating` REAL, `cultural_num` INTEGER, `great_cultural_num` INTEGER, `cultural_avg_rating` REAL, `cultural_list` TEXT, `books_num` REAL, `books_list` TEXT, `theatres_num` INTEGER, `galleries_num` INTEGER, `vote_percent_clinton` REAL, `median_housing_singlefam` REAL, `median_housing_condo` REAL )

--DELETE FROM nexthome_master

INSERT INTO nexthome_master (town,commute_optum)
SELECT DISTINCT city, car_time_text
FROM google_travel_times
WHERE car_time_sec<3600

UPDATE nexthome_master
SET rest_num = (
SELECT COUNT(*)
FROM google_places_distinct
--join nexthome_master on google_places_distinct.city=nexthome_master.town
WHERE store_types like '%restaurant%'
GROUP BY city HAVING city=nexthome_master.town
)

UPDATE nexthome_master
SET great_rest_num = (
SELECT COUNT(*)
FROM google_places_distinct
--join nexthome_master on google_places_distinct.city=nexthome_master.town
WHERE store_types like '%restaurant%' and rating>=4.5
GROUP BY city HAVING city=nexthome_master.town
)

UPDATE nexthome_master
SET list_great_rest = (
SELECT  group_concat(name)
FROM google_places_distinct
--join nexthome_master on google_places_distinct.city=nexthome_master.town
WHERE store_types like '%restaurant%' and rating>=4.5
GROUP BY city HAVING city=nexthome_master.town
ORDER BY rating DESC
)


UPDATE nexthome_master
SET rest_avg_rating = (
SELECT round(avg(rating),2)--, city
FROM google_places_distinct
--join nexthome_master on google_places_distinct.city=nexthome_master.town
WHERE store_types like '%restaurant%'
GROUP BY city HAVING city=nexthome_master.town
)

UPDATE nexthome_master
SET yelp_vege_avg = (
SELECT round(avg(rating),2)
FROM yelp_shops_distinct
--LEFT JOIN  nexthome_master on nexthome_master.town=yelp_shops_distinct.city
WHERE categories like '%vege%'
GROUP BY city HAVING city=nexthome_master.town
)
--note that there really aren't a lot of these. Also, yelp uses 0.0 rather than null

UPDATE nexthome_master
SET list_vege_yelp = (
SELECT group_concat(name)
FROM yelp_shops_distinct
--LEFT JOIN  nexthome_master on nexthome_master.town=yelp_shops_distinct.city
WHERE categories like '%vege%'
GROUP BY city HAVING city=nexthome_master.town
)

--synagogue
UPDATE nexthome_master
SET syn_num = (
SELECT COUNT(*)
FROM google_places_distinct
--join nexthome_master on google_places_distinct.city=nexthome_master.town
WHERE store_types like '%synagogue%'
GROUP BY city HAVING city=nexthome_master.town
)
, synagogue_list = (
SELECT group_concat(name)
FROM google_places_distinct
--join nexthome_master on google_places_distinct.city=nexthome_master.town
WHERE store_types like '%synagogue%'
GROUP BY city HAVING city=nexthome_master.town
)
,great_syn_num = (
SELECT COUNT(*)
FROM google_places_distinct
--join nexthome_master on google_places_distinct.city=nexthome_master.town
WHERE store_types like '%synagogue%' and rating>=4.0
GROUP BY city HAVING city=nexthome_master.town
)
,syn_avg_rating = (
SELECT round(avg(rating),2)--, city
FROM google_places_distinct
--join nexthome_master on google_places_distinct.city=nexthome_master.town
WHERE store_types like '%synagogue%'
GROUP BY city HAVING city=nexthome_master.town
)

--cultural = IN(museum, movie_theater book_store, art_gallery)
UPDATE nexthome_master
SET cultural_num = (
SELECT COUNT(*)
FROM google_places_distinct
--join nexthome_master on google_places_distinct.city=nexthome_master.town
WHERE store_types like '%museum%' or store_types like '%movie_theater%' or store_types like '%book_store%' or store_types like '%art_gallery%'
GROUP BY city HAVING city=nexthome_master.town
)
,cultural_list = (
SELECT group_concat(name)
FROM google_places_distinct
--join nexthome_master on google_places_distinct.city=nexthome_master.town
WHERE store_types like '%museum%' or store_types like '%movie_theater%' or store_types like '%book_store%' or store_types like '%art_gallery%'
GROUP BY city HAVING city=nexthome_master.town
)
,great_cultural_num = (
SELECT COUNT(*)
FROM google_places_distinct
--join nexthome_master on google_places_distinct.city=nexthome_master.town
WHERE (store_types like '%museum%' or store_types like '%movie_theater%' or store_types like '%book_store%' or store_types like '%art_gallery%') and rating>=4.0
GROUP BY city HAVING city=nexthome_master.town
)
,cultural_avg_rating = (
SELECT round(avg(rating),2)--, city
FROM google_places_distinct
--join nexthome_master on google_places_distinct.city=nexthome_master.town
WHERE store_types like '%museum%' or store_types like '%movie_theater%' or store_types like '%book_store%' or store_types like '%art_gallery%'
GROUP BY city HAVING city=nexthome_master.town
)

--book_store
UPDATE nexthome_master
SET books_num = (
SELECT COUNT(*)
FROM google_places_distinct
--join nexthome_master on google_places_distinct.city=nexthome_master.town
WHERE store_types like '%book%'
GROUP BY city HAVING city=nexthome_master.town
)
, books_list = (
SELECT group_concat(name)
FROM google_places_distinct
WHERE store_types like '%book%'
GROUP BY city HAVING city=nexthome_master.town
)

--movie theatres and art galleries
UPDATE nexthome_master
SET theatres_num = (
SELECT COUNT(*)
FROM google_places_distinct
WHERE store_types like '%movie%'
GROUP BY city HAVING city=nexthome_master.town
)
, galleries_num = (
SELECT COUNT(*)
FROM google_places_distinct
WHERE store_types like '%art_gallery%'
GROUP BY city HAVING city=nexthome_master.town
)

--percent of city voted for Clinton in 2016 presidential
UPDATE nexthome_master
SET vote_percent_clinton = (SELECT clinton_percent
FROM ma_2016_pres_voting
WHERE ma_2016_pres_voting.town = nexthome_master.town)
--note: Manchester-by-the-sea is just Manchester in ma_2016_pres_voting, hence this second statement
UPDATE nexthome_master
SET vote_percent_clinton = 64.9
WHERE town like '%Manchester%'

--for zillow
UPDATE  zillow_condo
SET price = NULL
WHERE price = '---'

UPDATE  zillow_condo
SET median_price = NULL
WHERE median_price = '---'

UPDATE zillow_condo
SET median_per_foot = null
WHERE median_per_foot = '---'

--last columns
UPDATE nexthome_master
SET median_housing_singlefam = (
SELECT price
FROM zillow_single_family
WHERE region = nexthome_master.town
)
UPDATE nexthome_master
SET median_housing_condo = (
SELECT price
FROM zillow_condo
WHERE region = nexthome_master.town
)


--MORE ANALYSIS
select * from nexthome_master
where great_rest_num > 5 and yelp_vege_avg > 0 and books_num > 0  and   syn_num > 0
order by rest_avg_rating desc
