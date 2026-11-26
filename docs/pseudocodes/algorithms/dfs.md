DFS

    START
    INPUT graph, starting course
    CREATE an empty list of visited courses
    PUT the starting course on the stack
    WHILE the stack is not empty
        TAKE the top course off the stack
        IF the course has not been visited THEN
            ADD it to the visited list
            FOR each next course of this course
                IF the next course has not been visited THEN
                    PUT it on the stack
                END IF
            END FOR
        END IF
    END WHILE
    RETURN the visited list
    END
