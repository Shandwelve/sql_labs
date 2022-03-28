from core.commands import BaseCommand


class Command(BaseCommand):
    """
    3. Formulați următoarele interogări
    """
    def case_a(self):
        """
        a. Afișați lista filmelor unde a jucat Johnny Deep.
        """
        self.database.dump(
            """
            select films.*,
                actors.name as actor_name
            from films
                join filmography on films.id = filmography.film_id
                join actors on filmography.actor_id = actors.id
            where actors.name = 'Johnny Deep';
            """
        )

    def case_b(self):
        """
        b. Afișați lista anilor unde Johnny Deep a jucat într-un film și rolul său în acest film.
        """
        self.database.dump(
            """
            select films.age,
                filmography.role,
                actors.name as actor_name
            from films
                join filmography on films.id = filmography.film_id
                join actors on filmography.actor_id = actors.id
            where actors.name = 'Johnny Deep';
            """
        )

    def case_c(self):
        """
        c. Afișați lista tuturor filmelor realizate de autorul filmului „Le parrain”. Interogarea nu trebuie
           să conțină numele autorului.
        """
        self.database.dump(
            """
            select self.*
            from films
                join films as self on films.director = self.director
            where films.title = 'Le parrain';
            """
        )

    def case_d(self):
        """
        d. Afișați lista filmelor ce încep cu lanțul de caractere ”Le” sau conține lanțul de caractere ”de”.
        """
        self.database.dump(
            """
            select *
            from films
            where title like 'Le%' 
                or title like '%de%';
            """
        )

    def case_e(self):
        """
        e. Afișați lista filmelor ordonate după anii realizării, în ordine descrescătoare.
        """
        self.database.dump(
            """
            select *
            from films
            order by age desc;
            """
        )

    def case_f(self):
        """
        f. Afișați numărul actorilor ce au jucat în filmul ”Odiseea lui Pi".
        """
        self.database.dump(
            """
            select count(filmography.actor_id) as author_count
            from filmography
                join films on filmography.film_id = films.id
            where films.title = "L'odyssee de Pi";
            """
        )

    def case_g(self):
        """
        g. Lista actorilor ce au jucat în oarecare film.
        """
        self.database.dump(
            """
            select distinct actors.*
            from filmography
                join actors on filmography.actor_id = actors.id;
            """
        )

    def case_h(self):
        """
        h. Lista actorilor ce au jucat cel puțin într-un film cu salariile medii pe care le-au avut pentru toate rolurile
            jucate. Denumiți coloana „Mediu”.
        """
        self.database.dump(
            """
            select actors.*,
                avg(salary) as Mediu
            from filmography
                join actors on filmography.actor_id = actors.id
            group by filmography.actor_id;
            """
        )

    def case_i(self):
        """
        i. Lista perechilor de actori cu același salariu. O pereche de actori nu trebuie să se afle de două ori
            în rezultatul dumneavoastră.
        """
        self.database.dump(
            """
            select actors.*,
                actors_copy.*,
                self.salary
            from filmography
                inner join filmography as self on filmography.salary = self.salary 
                    and self.actor_id <> filmography.actor_id
                left join actors on filmography.actor_id = actors.id
                left join actors as actors_copy on self.actor_id = actors_copy.id
            where actors.id < actors_copy.id;
            """
        )

    def case_j(self):
        """
        j. Salariile din baza de date sunt în dolari. Afișați salariile în valuta națională, calculați reieșind
            din cursul oficial.
        """
        self.database.dump(
            """
            select salary * 18.38 as salary_mdl
            from filmography;
            """
        )
