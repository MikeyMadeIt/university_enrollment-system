BFS

    START
    INPUT graph, starting course
    CREATE a visited list containing the starting course
    PUT the starting course in the waiting line
    WHILE the waiting line is not empty
        TAKE the first course out of the waiting line
        FOR each next course of this course (none if it has no entry)
            IF the next course has not been visited THEN
                ADD it to the visited list
                PUT it at the end of the waiting line
            END IF
        END FOR
    END WHILE
    RETURN the visited list
    END
 
BFS LEVELS

    START
    INPUT graph, starting course
    SET the starting course's level to 0
    PUT the starting course in the waiting line
    WHILE the waiting line is not empty
        TAKE the first course out of the waiting line
        FOR each next course of this course (none if it has no entry)
            IF the next course has no level yet THEN
                SET its level to the current course's level plus 1
                PUT it at the end of the waiting line
            END IF
        END FOR
    END WHILE
    RETURN the level of every reachable course
    END
