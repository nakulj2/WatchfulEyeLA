CREATE DEFINER=`root`@`%` TRIGGER `Location_AFTER_INSERT` AFTER INSERT ON `Location` FOR EACH ROW BEGIN
    SET @longitude = (SELECT Longitude FROM Location WHERE Record_Number = new.Record_Number);
    SET @latitude = (SELECT Latitude FROM Location WHERE Record_Number = new.Record_Number);
    IF @longitude > 180 OR @longitude < -180 THEN
		DELETE FROM Location WHERE Record_Number = new.Record_Number;
	ELSEIF @latitude > 90 OR @latitude < -90 THEN
		DELETE FROM Location WHERE Record_Number = new.Record_Number;
	END IF;
END
