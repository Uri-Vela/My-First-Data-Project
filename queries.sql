SELECT
    d.OperationID,
    d.OperationDate,
    d.Shift,
    d.BoilerID AS OperationBoilerID,
    b.BoilerName,
    sp.BoilerID AS SteamBoilerID,
    sp.ProductionHour,
    sp.SteamTPH,
    sp.SteamTemperature,
    sp.SteamPressure
FROM DailyOperations d
LEFT JOIN Boilers b
    ON d.BoilerID = b.BoilerID
LEFT JOIN SteamProduction sp
    ON d.OperationID = sp.OperationID
ORDER BY d.OperationID;