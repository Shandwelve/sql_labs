from core.seeds import BaseSeed


class Seed(BaseSeed):

    def run(self):
        self.database.insert(
            """
            insert into persons (id, name, age)
            values (1, 'Elvi', 19),
            (2, 'Farouk', 19),
            (3, 'Sam', 19),
            (4, 'Tiany', 19),
            (5, 'Nadia', 14),
            (6, 'Chris', 12),
            (7, 'Kris', 10),
            (8, 'Bethany', 16),
            (9, 'Louis', 17),
            (10, 'Austin', 22),
            (11, 'Gabriel', 21),
            (12, 'Jessica', 20),
            (13, 'John', 16),
            (14, 'Alfred', 19),
            (15, 'Samantha', 17),
            (16, 'Craig', 17);
            """
        )

        self.database.insert(
            """
            insert into friends
            values (1, 2),
            (1, 3),
            (2, 4),
            (2, 6),
            (3, 9),
            (4, 9),
            (7, 5),
            (5, 8),
            (6, 10),
            (13, 6),
            (7, 6),
            (8, 7),
            (9, 11),
            (12, 9),
            (10, 15),
            (12, 11),
            (12, 15),
            (13, 16),
            (15, 13),
            (16, 14);
            """
        )

        self.database.insert(
            """
            insert into kin
            values (4, 6),
            (2, 4),
            (9, 7),
            (7, 8),
            (11, 9),
            (13, 10),
            (14, 5),
            (12, 13);
            """
        )