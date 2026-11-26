CREATE COURSE DICTIONARY

    START
    CREATE an empty collection of courses, stored by course code
    END
 
ADD COURSE

    START
    INPUT course code, name, capacity, prerequisites (optional)
    IF the course code already exists THEN
        RETURN false
    END IF
    IF no prerequisites were given THEN
        SET prerequisites to empty
    END IF
    SAVE the course under its course code with:
        the name
        the capacity
        an empty set of enrolled students
        the set of prerequisites
    RETURN true
    END
 
GET COURSE

    START
    INPUT course code
    RETURN the course record, or nothing if the code does not exist
    END
 
COURSE EXISTS

    START
    INPUT course code
    RETURN true if the code is in the collection, otherwise false
    END
 
HAS SLOT

    START
    INPUT course code
    FIND the course
    IF the course does not exist THEN
        RETURN false
    END IF
    RETURN true if the number of enrolled students is less than the capacity,
        otherwise false
    END
 
ENROLL STUDENT

    START
    INPUT course code, student ID
    FIND the course
    IF the course does not exist THEN
        RETURN false
    END IF
    IF the course has no free slot THEN
        RETURN false
    END IF
    ADD the student ID to the course's enrolled students
    RETURN true
    END
 
DROP STUDENT

    START
    INPUT course code, student ID
    FIND the course
    IF the course does not exist THEN
        RETURN false
    END IF
    REMOVE the student ID from the course's enrolled students
        (no error if the student was not enrolled)
    RETURN true
    END
 
MEETS PREREQUISITES

    START
    INPUT course code, student's completed courses
    FIND the course
    IF the course does not exist THEN
        RETURN false
    END IF
    FOR each prerequisite of the course
        IF the prerequisite is not in the completed courses THEN
            RETURN false
        END IF
    END FOR
    RETURN true
    END
 
GET ALL COURSES

    START
    RETURN every course record
    END
