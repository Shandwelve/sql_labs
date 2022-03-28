from core.commands import BaseCommand


class Command(BaseCommand):

    def case_1(self):
        """
        1. Creați o procedură care preia id cercetătorului ca parametru și returnează lista
            articolelor acestui în ordinea alfabetică.
        """

        self.database.create_procedure(
            """
            drop procedure if exists articleList;
            delimiter $$
            create procedure articleList(in explorer_id int unsigned)
            begin
                select articles.*
                from explorers
                        join articles on explorers.article_id = articles.id
                where explorers.id = explorer_id
                order by articles.title;
            end$$
            delimiter ;
            """
        )
        self.database.call_procedure('articleList', [2])

    def case_2(self):
        """
        2. Creați o procedură care preia id universității ca parametru și returnează lista cercetătorilor împreună cu
            articolele acestora care activează în universitatea respectivă. Dacă un cercetător nu are articole el nu
            trebuie să apară în listă
        """
        self.database.create_procedure(
            """
            drop procedure if exists explorersWithArticles;
            delimiter $$
            create procedure explorersWithArticles(in university_id int unsigned)
            begin
                select *
                from explorers
                         inner join articles on explorers.article_id = articles.id
                where explorers.university_id = university_id;
            end $$
            delimiter ;
            """
        )
        self.database.call_procedure('explorersWithArticles', [1])

    def case_3(self):
        """
        3. Creați o procedură care preia id universității și returnează lista cercetătorilor împreună cu articolele
            acestora care activează în universitatea respectivă. Dacă un cercetător nu are articole el oricum trebuie să
            apară în listă, în dreptul lui se va afișa null pentru denumirea articolului.
        """
        self.database.create_procedure(
            """
            drop procedure if exists allExplorersWithArticles;
            delimiter $$
            create or replace procedure allExplorersWithArticles(in university_id int unsigned)
            begin
                select *
                from explorers
                         left join articles on explorers.article_id = articles.id
                where explorers.university_id = university_id;
            end $$
            delimiter ;
            """
        )
        self.database.call_procedure('allExplorersWithArticles', [1])

    def case_4(self):
        """
        4. Creați o procedură care va determina pentru fiecare cercetător reitingul general și pe universitate.
            Reitingul general se va determina după formula: numărul de articole a cercetătorului/numărul total de
            articole*100. Reitingul pe universitate se va determina după formula: numărul de articole a
            cercetătorului/numărul total de articole pe universitate*100.
        """
        self.database.create_procedure(
            """
            drop procedure if exists calculateRating;
            delimiter $$
            create procedure calculateRating()
            begin
                select explorers.name as name,
                       count(explorers.article_id) / (select count(*) from articles) * 100 as general,
                       count(explorers.article_id) /
                       (select count(*)
                       from explorers e
                       where e.university_id = explorers.university_id) * 100 as university
                from explorers
                group by explorers.name;
            
            end $$
            delimiter ;
            """
        )
        self.database.call_procedure('calculateRating')

    def case_5(self):
        """
        5. Adăugați în tabelul Cercetători un atribut nou – Calificativ. Creați o procedură care completa valorile
            pentru atributul Calificativ în felul următor: „foarte bine” – dacă numărul de articole este mai mare de 25;
            „bine” – dacă numărul de articole este în intervalul 15-25, „suficient” dacă numărul de articole este
            în intervalul 5-15 și „insuficient” dacă numărul de articole este mai mic de 5.
        """
        self.database.create_procedure(
            """
            drop procedure if exists setQualifying;
            delimiter $$
            create procedure setQualifying()
            begin
                alter table explorers
                    add column if not exists qualifying varchar(50) null;
            
                update explorers
                set qualifying = (
                    select case
                        when count(article_id) > 25 then 'foarte bine'
                        when count(article_id) between 15 and 25 then 'bine'
                        when count(article_id) between 5 and 15 then 'suficient'
                        when count(article_id) < 5 then 'insuficient'
                        end as _qualifying
                    from explorers e
                    where e.article_id = explorers.article_id
                )
                where article_id is not null;
            
            end $$
            delimiter ;
            """
        )
        self.database.call_procedure('setQualifying')

    def case_6(self):
        """
        6. Creați o procedură care va verifica posibilitatea de ștergere a unui cercetător: dacă cercetătorul există,
            dacă nu sunt articole legate cu el, atunci operația de eliminare este validă și se returnează true,
            în caz contrar se afișează un mesaj de eroare personalizat.
        """
        self.database.create_procedure(
            """
            drop procedure if exists isSafeToDelete;
            delimiter $$
            create procedure isSafeToDelete(in explorer_id int unsigned)
            begin
                select case
                           when count(id) < 1 then 'Explorer not exists'
                           when article_id is not null then 'Explorer has one or more articles'
                           else true
                           end
                from explorers
                where explorers.id = explorer_id;
            
            end $$
            delimiter ;
            """
        )
        self.database.call_procedure('isSafeToDelete', [1])

    def case_7(self):
        """
        7. Creați o funcție care ar returna după id cercetator dat ca parametru denumirea universității în care
            activează.
        """
        self.database.create_procedure(
            """
            drop function if exists getUniversityNameByExplorer;
            delimiter $$
            create function getUniversityNameByExplorer(explorer_id int unsigned)
                returns varchar(150)
            begin
                declare university_name varchar(150);
            
                select universities.name
                into university_name
                from explorers
                         inner join universities on explorers.university_id = universities.id
                where explorers.id = explorer_id;
            
                return university_name;
            end $$
            
            delimiter ;
            """
        )
        self.database.call_procedure('getUniversityNameByExplorer', [1])

    def case_8(self):
        """
        8. Creați o funcție care ar returna după id cercetator dat ca parametru calificativul acestuia.
        """
        self.database.create_procedure(
            """
            drop function if exists getQualifyingByExplorerId;
            delimiter $$
            create function getQualifyingByExplorerId(explorer_id int unsigned)
                returns varchar(50)
            begin
                declare qualifying varchar(50);
            
                select explorers.qualifying
                into qualifying
                from explorers
                where explorers.id = explorer_id;
            
                return qualifying;
            end $$
            
            delimiter ;
            """
        )
        self.database.call_procedure('getQualifyingByExplorerId', [1])

    def case_9(self):
        """
        9. Creați o funcție care ar returna după denumirea universității date ca parametru numărul de cercetători
            care activează în universitatea dată.
        """
        self.database.create_procedure(
            """
            drop function if exists getExplorersNumberFromUniversity;
            delimiter $$
            create or replace function getExplorersNumberFromUniversity(university_id int unsigned)
                returns bigint
            begin
                declare explorersNumber bigint;
            
                select count(distinct explorers.name)
                into explorersNumber
                from explorers
                where explorers.university_id = university_id;
            
                return explorersNumber;
            end $$
            
            delimiter ;
            """
        )
        self.database.call_procedure('getExplorersNumberFromUniversity', [1])

    def case_10(self):
        """
        10. Creați o funcție care ar returna după id universității date ca parametru numărul de articole scrise
            de colaboratorii acestei universități.
        """
        self.database.create_procedure(
            """
            drop function if exists getArticlesNumberByUniversity;
            delimiter $$
            create function getArticlesNumberByUniversity(university_id int unsigned)
                returns bigint
            begin
                declare articlesNumber bigint;
            
                select count(distinct explorers.article_id)
                into articlesNumber
                from explorers
                where explorers.university_id = university_id and explorers.article_id is not null;
            
                return articlesNumber;
            end $$
            
            delimiter ;
            """
        )
        self.database.call_procedure('getArticlesNumberByUniversity', [1])

    def case_11(self):
        """
        11. Creați o funcție care ar returna după numele cercetatorului dat ca parametru numărul de articole scrise
            de el.
        """
        self.database.create_procedure(
            """
            drop function if exists getArticlesNumberByExplorerName;
            delimiter $$
            create function getArticlesNumberByExplorerName(explorer_name varchar(150))
                returns bigint
            begin
                declare articlesNumber bigint;
            
                select count(explorers.article_id)
                into articlesNumber
                from explorers
                where explorers.name = explorer_name and explorers.article_id is not null;
            
                return articlesNumber;
            end $$
            
            delimiter ;
            """
        )
        self.database.call_procedure('getArticlesNumberByExplorerName', ['Dodu Petru'])

    def case_12(self):
        """
        12. Creați o funcție care returnează True sau False în dependență de faptul dacă un cercetător
            (numele și prenumele) lucrează în universitatea dată (id universitate) date ca parametri.
        """
        self.database.create_procedure(
            """
            drop function if exists doesExplorerWorkAtUniversity;
            delimiter $$
            create function doesExplorerWorkAtUniversity(explorer_name varchar(150), university_id int unsigned)
                returns varchar(5)
            begin
                declare articlesNumber varchar(5);
                select if(count(*) < 1, 'False', 'True')
                into articlesNumber
                from explorers
                where explorers.name = explorer_name and explorers.university_id = university_id
                limit 1;
            
                return articlesNumber;
            end $$
            
            delimiter ;
            """
        )
        self.database.call_procedure('getArticlesNumberByExplorerName', ['Dodu Petru', 1])











