CREATE ENROLLMENT LIST

    START
    CREATE an empty list of records
    END
 
ADD RECORD

    START
    INPUT student ID, course code, timestamp (optional)
    CREATE a record containing the student ID, course code and timestamp
    ADD the record to the end of the list
    RETURN the record
    END
 
GET ALL RECORDS

    START
    RETURN the whole list of records
    END
 
FILTER BY STUDENT

    START
    INPUT student ID
    CREATE an empty list of results
    FOR each record in the list
        IF the record's student ID matches THEN
            ADD the record to the results
        END IF
    END FOR
    RETURN the results
    END
 
FILTER BY COURSE

    START
    INPUT course code
    CREATE an empty list of results
    FOR each record in the list
        IF the record's course code matches THEN
            ADD the record to the results
        END IF
    END FOR
    RETURN the results
    END
