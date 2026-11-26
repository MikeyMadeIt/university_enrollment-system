TOPOLOGICAL SORT

    START
    INPUT graph
    CREATE an empty visited list
    CREATE an empty result list
    FOR each course in the graph
        VISIT the course
    END FOR
    RETURN the result list
    END
 
VISIT a course

    IF the course is already visited THEN
        STOP
    END IF
    ADD the course to the visited list
    FOR each next course of this course (none if it has no entry)
        VISIT the next course
    END FOR
    PLACE the course at the FRONT of the result list
    END
