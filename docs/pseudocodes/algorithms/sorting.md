BUBBLE SORT BY NAME

    START
    INPUT list of records
    MAKE a copy of the list
    COUNT how many records are in the copy
    REPEAT once for each record
        FOR each pair of neighboring records up to the part not yet sorted
            IF the first name comes after the second name alphabetically
               (ignore upper/lower case) THEN
                SWAP the two records
            END IF
        END FOR
    END REPEAT
    RETURN the sorted copy
    END
 
BUBBLE SORT COURSES BY CAPACITY

    START
    INPUT list of courses (each course is a code with its information)
    MAKE a copy of the list
    COUNT how many courses are in the copy
    REPEAT once for each course
        FOR each pair of neighboring courses up to the part not yet sorted
            IF the first course's capacity is greater than the second's THEN
                SWAP the two courses
            END IF
        END FOR
    END REPEAT
    RETURN the sorted copy
    END
