from core.seeds import BaseSeed


class Seed(BaseSeed):

    def run(self):
        self.database.insert(
            """
            insert into articles (id, title)
            values (1, 'Articol1'),
            (2, 'Articol2'),
            (3, 'Articol3'),
            (4, 'Articol4'),
            (5, 'Articol5');
            """
        )

        self.database.insert(
            """
            insert into universities (id, name)
            values (1, 'USARB'),
            (2, 'USM'),
            (3, 'ASEM');
            """
        )

        self.database.insert(
            """
            insert into explorers (id, name, article_id, university_id)
            values (1, 'Dodu Petru', 1, 1),
            (2, 'Lungu Vasile', 2, 2),
            (3, 'Vrabie Maria', 3, 1),
            (4, 'Ombun Bogdan', 4, 3);
            """
        )
