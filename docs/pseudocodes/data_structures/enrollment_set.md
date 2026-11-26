CREATE ENROLLMENT SET

    START
    CREATE an empty set of (student ID, course code) pairs
    END
 
IS DUPLICATE

    START
    INPUT student ID, course code
    RETURN true if the pair is already in the set, otherwise false
    END
 
ADD ENROLLMENT

    START
    INPUT student ID, course code
    IF the pair is already in the set THEN
        RETURN false
    END IF
    ADD the pair to the set
    RETURN true
    END
 
REMOVE ENROLLMENT

    START
    INPUT student ID, course code
    IF the pair is in the set THEN
        REMOVE the pair from the set
        RETURN true
    END IF
    RETURN false
    END
 
GET COURSES OF STUDENT

    START
    INPUT student ID
    CREATE an empty set of course codes
    FOR each pair in the set
        IF the pair's student ID matches THEN
            ADD the pair's course code to the results
        END IF
    END FOR
    RETURN the results
    END
 
GET STUDENTS OF COURSE

    START
    INPUT course code
    CREATE an empty set of student IDs
    FOR each pair in the set
        IF the pair's course code matches THEN
            ADD the pair's student ID to the results
        END IF
    END FOR
    RETURN the results
    END
