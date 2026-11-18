LINEAR SEARCH BY NAME

    START
    INPUT list of records, name to find
    FOR each record in the list
        IF the record's name matches the name to find (ignore upper/lower case) THEN
            RETURN that record
        END IF
    END FOR
    RETURN nothing (not found)
    END
 
LINEAR SEARCH BY ID

    START
    INPUT records stored by ID, ID to find
    LOOK UP the ID in the records
    RETURN the record if found, otherwise RETURN nothing
    END
 
SEARCH COURSES BY KEYWORD

    START
    INPUT courses stored by course code, keyword
    CREATE an empty list of results
    FOR each course code and its course information
        IF the keyword appears in the course name (ignore upper/lower case) THEN
            ADD the course code and its information to the results
        END IF
    END FOR
    RETURN the results
    END
