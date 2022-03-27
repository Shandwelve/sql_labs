from core.seeds import BaseSeed


class Seed(BaseSeed):

    def run(self):
        self.database.insert(
            """
            insert into actors (id, name)
            values (1, 'Johnny Deep'),
            (2, 'Al Pacino'),
            (3, 'Suraj Sharma'),
            (4, 'Brad Pitt'),
            (5, 'Edward Norton');
            """
        )

        self.database.insert(
            """
            insert into films (id, title, director, age)
            values (1, 'Les evades', 'Darabont', 1994),
            (2, 'Rango', 'Verbinski', 2015),
            (3, 'Le parrain', 'Coppola', 1972),
            (4, 'Le parrain 2', 'Coppola', 1974),
            (5, 'Chocolat', 'Hallstrom', 2013),
            (6, 'Scarface', 'De palma', 1983),
            (7, "L'odyssee de Pi", 'Ang Lee', 2011);
            """
        )

        self.database.insert(
            """
            insert into filmography (actor_id, film_id, role, salary)
            values (1, 5, 'Roux', 5000),
            (1, 7, 'Rango', 10000),
            (2, 2, 'Michael Corleone', 10000),
            (2, 3, 'Michael Corleone', 20000),
            (2, 6, 'Tony Montana', 15000),
            (3, 4, 'Pi', 20000);
            """
        )

