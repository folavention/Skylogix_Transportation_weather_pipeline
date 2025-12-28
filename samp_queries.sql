-- Weather trends per city
SELECT
    city AS location,
    DATE(observed_at) AS date,
    AVG(temp_c) AS avg_temp_c,
    AVG(rain_1h_mm) AS avg_rainfall,
    AVG(humidity_pct) AS avg_humidity,
    AVG(wind_speed_ms) AS avg_wind_speed,
    AVG(snow_1h_mm) AS avg_snowfall
FROM weather_readings
WHERE city IN ('Lagos NG', 'Johannesburg ZA', 'Nairobi KE', 'Accra GH')
GROUP BY city, DATE(observed_at)
ORDER BY city, date;





-- Extreme weather events
SELECT
    city,
    observed_at,
    temp_c,
    wind_speed_ms,
    rain_1h_mm,
    snow_1h_mm,
    weather_description
FROM weather_readings
WHERE wind_speed_ms > 15          -- wind > 15 m/s (~54 km/h)
   OR rain_1h_mm > 20             -- heavy rain > 20 mm/hr
   OR snow_1h_mm > 10             -- heavy snow > 10 mm/hr
ORDER BY observed_at DESC;




--~~ HOW WEATHER DATA CAN JOIN WITH LOGISTICS DATA --~~

--Samle logistics data table
    --Table: logistics_shipments
    --Columns:
        --shipment_id SERIAL PRIMARY KEY,
        --origin_city VARCHAR(100),
        --destination_city VARCHAR(100),
        --departure_time TIMESTAMP,
        --arrival_time TIMESTAMP,
        --delay BOOLEAN,
        --distance_km VARCHAR(50)

-- Weather table
    --Table: weather_readings
    --Columns:
        --id SERIAL PRIMARY KEY,
        --city VARCHAR(100),
        --observed_at TIMESTAMP,
        --temp_c FLOAT,
        --rain_1h_mm FLOAT,
        --humidity_pct FLOAT,
        --wind_speed_ms FLOAT,
        --snow_1h_mm FLOAT,
        --weather_description VARCHAR(255)




--SQL example to join weather with logistics data
SELECT
    ls.shipment_id,
    ls.origin_city,
    ls.destination_city,
    ls.departure_time,
    ls.arrival_time,
    ls.delay,
    wr.city AS weather_city,
    wr.observed_at AS weather_time,
    wr.temp_c,
    wr.rain_1h_mm,
    wr.humidity_pct,
    wr.wind_speed_ms,
    wr.snow_1h_mm,
    wr.weather_description
    from logistics_shipments ls
    JOIN weather_readings wr
      ON ls.origin_city = wr.city
     AND DATE(ls.departure_time) = DATE(wr.observed_at)
