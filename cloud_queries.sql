SELECT 
  operationid,
  boilerid,
  steamtemperature,
  steampressure,
  pressure_to_temp_ratio,
  -- WINDOW FUNCTION: Rank rows based on steam pressure for each specific boiler
  DENSE_RANK() OVER (
    PARTITION BY boilerid 
    ORDER BY steampressure DESC
  ) as pressure_rank
FROM 
  `boiler_analytics.raw_telemetry`
ORDER BY 
  boilerid, 
  pressure_rank ASC;
