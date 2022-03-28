from core.commands import BaseCommand


class Command(BaseCommand):

    def case_1(self):
        """
        1. Să se creeze un declanșator care după adăugarea unei persoane în tabelul Persoane, va adăuga o legătură
            de prietenie dintre persoana dată și Elvia. Să se verifice lucrul declanșatorului prin adăugarea unei
            persoane în tabelul Persoane. Care este efectul declanșatorului?
        """
        self.database.execute(
            """
            drop trigger if exists afterAddPerson;
            create trigger afterAddPerson
                after insert
                on persons
                for each row
            begin
                insert into friends (first_person_id, second_person_id)
                    value (new.id, (select id from persons where name = 'Elvi' limit 1));
            end;
            """
        )
        self.database.insert("insert into persons (name, age) value ('Andrei', 19);")

    def case_2(self):
        """
        2. Să se creeze un declanșator care înainte de adăugare a unei persoane în tabelul Persoane,
            verifică dacă această persoană există deja în tabel. Dacă există deja o persoană cu același nume (ca și cel
            inserat) să se afișeze un mesaj de eroare „Atenție! Așa persoană există!”. Să se verifice lucrul
            declanșatorului prin adăugarea unei persoane în tabelul Persoane cu același nume, cu un nume nou diferit.
            Care este efectul declanșatorului? Obs. Se va folosi următoarea structură pentru afișarea mesajului:
            signal sqlstate '45000' set message_text = 'MESAJ'
        """
        self.database.execute(
            """
            drop trigger if exists checkIfPersonExists;
            create trigger checkIfPersonExists
                before insert
                on persons
                for each row
            begin
                if exists(select * from persons where name = new.name and age = new.age) then
                    signal sqlstate '45001' set message_text = 'Atenție! Așa persoană există!';
                end if;
            end;
            """
        )
        self.database.insert("insert into persons (name, age) value ('Andrei', 19);")

    def case_3(self):
        """
        3. Să se creeze un declanșator care după inserarea a două persoane în tabelul rude creează o legătură de
            prietenie dintre aceste două persoane. Dacă inserăm perechea (x, y) în tabelul Rude, în tabelul Amici se va
            insera aceeași pereche de persoane (x, y). Dacă perechea introdusă există, se va returna un mesaj de eroare.
            Să se verifice lucrul declanșatorului.
        """
        self.database.execute(
            """
            drop trigger if exists afterInsertKin;
            create trigger afterInsertKin
                after insert
                on kin
                for each row
            begin
                if exists(select *
                          from friends
                          where first_person_id = new.first_person_id
                            and second_person_id = new.second_person_id) then
                    signal sqlstate '45001' set message_text = 'Perechea exista!';
                end if;
                insert into friends (first_person_id, second_person_id)
                    value (new.first_person_id, new.second_person_id);
            end;
            """
        )
        self.database.insert("insert into kin (first_person_id, second_person_id) value (1, 2);")

    def case_4(self):
        """
        4. Să se creeze un declanșator care va elimina legătura de prietenie între două persoane, dacă legătura de
            rudenie între ele este eliminată. Dacă perechea (x, y) nu mai este în tabelul Rude, atunci perechea dată
            este eliminată automat din tabelul Amici. Demonstrați lucrul declanșatorului.
        """
        self.database.execute(
            """
            drop trigger if exists deleteRelation;
            create trigger deleteRelation
                before delete
                on kin
                for each row
            begin
                delete from friends 
                where first_person_id = old.first_person_id 
                    and second_person_id = old.second_person_id;
            end;
            """
        )
        self.database.execute(
            """
            delete
            from kin
            where first_person_id = 3
              and second_person_id = 9;
            """
        )

    def case_5(self):
        """
        5. Pentru această sarcină eliminați cheile străine din tabelul Amici. Să se creeze un declanșator care va lucra
            ca cheile străine eliminate. Dacă în tabelul Amici se va adăuga o pereche de persoane (x, y), declanșatorul
            se va asigura că persoanele cu codul x și y există în tabelul Persoane. În caz de depistare a încercării de
            a introduce persoane care nu există în tabelul Persoane se va afișa un mesaj de eroare. Să se demonstreze
            situațiile în care acționează declanșatorul dat.
        """
        self.database.execute(
            """
            alter table friends
                drop foreign key friends_ibfk_1;
            alter table friends
                drop foreign key friends_ibfk_2;
            """
        )
        self.database.execute(
            """
            drop trigger if exists insertFriendsWithValidation;
            create trigger insertFriendsWithValidation
                before insert
                on friends
                for each row
            begin
                if (select count(id) from persons where persons.id in (new.first_person_id, new.second_person_id)) < 2 then
                    signal sqlstate '45001' set message_text = 'One of the people doesn''t exist!';
                end if;
            end;
            """
        )
        self.database.insert("insert into friends (first_person_id, second_person_id) value (2, 1001);")

    def case_6(self):
        """
        6. Să se creeze un declanșator care va implementa modificarea în cascadă a datelor, astfel la modificarea
            datelor din tabelul Persoane (idPersoana) aceste modificări vor fi propagate în tabelul Amici.
            Demonstrați lucrul declanșatorului.
        """
        self.database.execute(
            """
            alter table kin
                drop foreign key kin_ibfk_1;
            alter table kin
                drop foreign key kin_ibfk_2;
            """
        )

        self.database.execute(
            """
            drop trigger if exists syncChangesPersonIdInFriendsTable;
            create trigger syncChangesPersonIdInFriendsTable
                after update
                on persons
                for each row
            begin
                update friends set first_person_id = new.id where first_person_id = old.id;
                update friends set second_person_id = new.id where friends.second_person_id = old.id;
            end;
            """
        )

        self.database.insert("update persons set id = 900 where id = 9;")

    def case_7(self):
        """
        7. Să se creeze un declanșator care va implementa eliminarea în cascadă a datelor, astfel la eliminarea unei
            peroane din tabelul Persoane (idPersoana) va fi eliminată legăturile persoanei date din tabelul Amici.
            Demonstrați lucrul declanșatorului.
        """

        self.database.execute(
            """
            drop trigger if exists cascadeDeletePersonIdInFriendsTable;
            create trigger cascadeDeletePersonIdInFriendsTable
                before delete
                on persons
                for each row
            begin
                delete from friends where first_person_id = old.id or second_person_id = old.id;
            end;
            """
        )

        self.database.insert("delete from persons where id = 5;")