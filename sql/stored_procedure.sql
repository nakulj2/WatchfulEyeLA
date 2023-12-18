CREATE DEFINER=`root`@`%` PROCEDURE `data_procedure`()
BEGIN

    DECLARE done INT default 0;
    DECLARE currArea VARCHAR(255);
    DECLARE currDescent VARCHAR(1);
    DECLARE currCount INT;

    DECLARE datacur cursor for SELECT AreaDescent.* 
		FROM (SELECT Area_Name, Descent_Code, COUNT(Record_Number) as Victim_Count FROM Victim NATURAL JOIN Cases NATURAL JOIN Location WHERE Descent_Code <> "X" OR Descent_Code <> "O" GROUP BY Area_Name, Descent_Code) as AreaDescent 
		LEFT OUTER JOIN (SELECT Area_Name, Descent_Code, COUNT(Record_Number) as Victim_Count FROM Victim NATURAL JOIN Cases NATURAL JOIN Location WHERE Descent_Code <> "X" OR Descent_Code <> "O" GROUP BY Area_Name, Descent_Code) as AreaDescentCopy
		ON AreaDescent.Area_Name = AreaDescentCopy.Area_Name AND AreaDescent.Victim_Count < AreaDescentCopy.Victim_Count 
		WHERE AreaDescentCopy.Area_Name IS NULL;
        
	DECLARE continue handler for not found set done = 1;
    
    drop table if exists LocationDescent;
	drop table if exists VictimAge;
    
    create table LocationDescent (
	Location VARCHAR(255) primary key,
        DescentGroup VARCHAR(255),
        VictimCount INT
    );
    
    create table VictimAge (
	CrimeCode INT primary key,
        CrimeCodeDesc VARCHAR(255),
        VictimCount INT
    );
    
    open datacur;
    
    repeat
		fetch datacur into currArea, currDescent, currCount;
        if currDescent = "A" then
			insert ignore into LocationDescent values(currArea, "Other Asian", currCount);
		elseif currDescent = "B" then
			insert ignore into LocationDescent values(currArea, "Black", currCount);
		elseif currDescent = "C" then
			insert ignore into LocationDescent values(currArea, "Chinese", currCount);
		elseif currDescent = "D" then
			insert ignore into LocationDescent values(currArea, "Cambodian", currCount);
		elseif currDescent = "F" then
			insert ignore into LocationDescent values(currArea, "Filipino", currCount);
		elseif currDescent = "G" then
			insert ignore into LocationDescent values(currArea, "Guamanian", currCount);
		elseif currDescent = "H" then
			insert ignore into LocationDescent values(currArea, "Hispanic/Latin/Mexican", currCount);
		elseif currDescent = "I" then
			insert ignore into LocationDescent values(currArea, "American Indian/Alaskan Native", currCount);
		elseif currDescent = "J" then
			insert ignore into LocationDescent values(currArea, "Japanese", currCount);
		elseif currDescent = "K" then
			insert ignore into LocationDescent values(currArea, "Korean", currCount);
		elseif currDescent = "L" then
			insert ignore into LocationDescent values(currArea, "Laotian", currCount);
		elseif currDescent = "P" then
			insert ignore into LocationDescent values(currArea, "Pacific Islander", currCount);
		elseif currDescent = "S" then
			insert ignore into LocationDescent values(currArea, "Samoan", currCount);
		elseif currDescent = "U" then
			insert ignore into LocationDescent values(currArea, "Hawaiian", currCount);
		elseif currDescent = "V" then
			insert ignore into LocationDescent values(currArea, "Vietnamese", currCount);
		elseif currDescent = "W" then
			insert ignore into LocationDescent values(currArea, "White", currCount);
		elseif currDescent = "Z" then
			insert ignore into LocationDescent values(currArea, "Asian Indian", currCount);
		end if;
        
	until
		done
	end repeat;
	
    close datacur;
    
    insert into VictimAge
	select temp.Crime_Code, temp.Crime_Code_Desc, temp.Victim_Count 
    from (
		SELECT Crime_Code, Crime_Code_Desc, COUNT(Victim.Record_Number) as Victim_Count
		FROM Victim JOIN Cases on Victim.Record_Number = Cases.Record_Number NATURAL JOIN CrimeCodes
		WHERE Victim_Age >= 18
		GROUP BY Crime_Code
		ORDER BY COUNT(Victim.Record_Number) DESC
		LIMIT 10
    ) temp;

END

