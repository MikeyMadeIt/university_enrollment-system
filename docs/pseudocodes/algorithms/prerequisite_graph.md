BUILD PREREQUISITE GRAPH

    START
    INPUT courses stored by course code
    CREATE an empty graph
    FOR each course code
        ADD the course code to the graph with an empty list of next courses
    END FOR
    FOR each course code and its course information
        FOR each prerequisite listed in the course information
            IF the prerequisite exists in the graph THEN
                ADD this course code to the prerequisite's list of next courses
            END IF
        END FOR
    END FOR
    RETURN the graph
    END
