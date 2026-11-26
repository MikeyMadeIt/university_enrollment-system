CREATE STUDENT DICTIONARY

    START
    CREATE an empty collection of students, stored by student ID
    END
 
ADD STUDENT

    START
    INPUT student ID, name
    IF the student ID already exists THEN
        RETURN false
    END IF
    SAVE the student under their ID with:
        the name
        an empty set of completed courses
    RETURN true
    END
 
GET STUDENT

    START
    INPUT student ID
    RETURN the student record, or nothing if the ID does not exist
    END
 
STUDENT EXISTS

    START
    INPUT student ID
    RETURN true if the ID is in the collection, otherwise false
    END
 
ADD COMPLETED COURSE

    START
    INPUT student ID, course code
    FIND the student
    IF the student does not exist THEN
        RETURN false
    END IF
    ADD the course code to the student's completed courses
    RETURN true
    END
 
HAS COMPLETED

    START
    INPUT student ID, course code
    FIND the student
    IF the student does not exist THEN
        RETURN false
    END IF
    RETURN true if the course code is in the student's completed courses,
        otherwise false
    END
 
DELETE STUDENT

    START
    INPUT student ID
    IF the student ID exists THEN
        REMOVE the student record
        RETURN true
    END IF
    RETURN false
    END
 
GET ALL STUDENTS

    START
    RETURN every student record
    END
