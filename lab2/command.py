from core.commands import BaseCommand


class Command(BaseCommand):
    """
    Formulați interogări pentru fiecare sarcină.
    """
    def case_1(self):
        """
        1. Lista prietenelor Elvirei.
        """
        self.database.dump(
            """
            select persons.*
            from persons
                join friends on persons.id = friends.first_person_id 
                    or persons.id = friends.second_person_id
                join persons as self on self.id = friends.first_person_id 
                    or self.id = friends.second_person_id
            where self.name = 'Elvi' and persons.name <> self.name;
            """
        )

    def case_2(self):
        """
        2. Lista persoanelor cu prietenii mai mici ca ele.
        """
        self.database.dump(
            """
            select persons.*,
                self.*
            from persons
                join friends on persons.id = friends.first_person_id 
                    or persons.id = friends.second_person_id
                join persons as self on self.id = friends.first_person_id 
                    or self.id = friends.second_person_id
            where self.age <> persons.age 
                and self.id > persons.id;
            """
        )

    def case_3(self):
        """
        3. Lista numelor prietenilor de aceeași vârstă. Rezultatele vor fi ordonate după două criterii:
            - După ani;
            - După nume pentru fiecare vârstă.
        """
        self.database.dump(
            """
            select persons.*,
                self.*
            from persons
                join friends on persons.id = friends.first_person_id 
                    or persons.id = friends.second_person_id
                join persons as self on self.id = friends.first_person_id 
                    or self.id = friends.second_person_id
            where self.age = persons.age 
                and self.id < persons.id
            order by persons.age,
                persons.name,
                self.name;
            """
        )

    def case_4(self):
        """
        4. Lista persoanelor ce au cel puțin doi membri ai familiei
        """
        self.database.dump(
            """
            select persons.*,
                count(persons.id) as family_members
            from kin
                join persons on persons.id = kin.first_person_id 
                    or persons.id = kin.second_person_id
            group by persons.id
            having count(persons.id) >= 2;
            """
        )

    def case_5(self):
        """
        5. Lista persoanelor ce nu au familie
        """
        self.database.dump(
            """
            select persons.*
            from persons
               left join kin on kin.first_person_id = persons.id 
                    or kin.second_person_id = persons.id
            where kin.first_person_id is null;
            """
        )

    def case_6(self):
        """
        6. Lista prietenilor împreună cu membrii familiei ce nu sunt prieteni.
        """
        self.database.dump(
            """
            select if(
                        friends.first_person_id <> kin.first_person_id,
                        friends.first_person_id,
                        friends.second_person_id
                    ) as friend,
                   if(
                        friends.first_person_id <> kin.first_person_id,
                        kin.first_person_id,
                        kin.second_person_id
                    ) as kin
            from friends
                join kin
                    on (
                    kin.first_person_id = friends.first_person_id
                        and kin.second_person_id <> friends.second_person_id
                    )
                        or (
                        kin.second_person_id = friends.second_person_id 
                            and kin.first_person_id <> friends.first_person_id
                        );
            """
        )

    def case_7(self):
        """
        7. Diferența între numărul persoanelor în total și numărul persoanelor ce au atins majoratul.
        """
        self.database.dump(
            """
            select count(persons.id) - count(self.age)
            from persons
                join persons as self on self.id = persons.id 
                    and self.age < 18
            """
        )

    def case_8(self):
        """
        8. Lista persoanelor care au cel puțin un prieten și cel puțin un membru al familiei.
        """
        self.database.dump(
            """
            select distinct persons.*
            from persons
                join friends on persons.id = friends.first_person_id 
                    or persons.id = friends.second_person_id
                join kin on persons.id = kin.first_person_id 
                    or persons.id = kin.second_person_id;
            """
        )

    def case_9(self):
        """
        9. Cifra medie de prieteni per persoană
        """
        self.database.dump(
            """
            select count(id) / count(distinct persons.id) as friends_per_person
            from persons
                join friends on friends.first_person_id = persons.id 
                    or friends.second_person_id = persons.id;
            """
        )

    def case_10(self):
        """
        10. Numărul persoanelor ce sunt prieteni sau prietenii prietenilor lui Tiffany.
        """
        self.database.dump(
            """
            select count(self.id) + count(distinct self.name)
            from persons
                join friends on persons.id = friends.first_person_id 
                    or persons.id = friends.second_person_id
                join persons as self on (self.id = friends.second_person_id or self.id = friends.first_person_id) 
                    and self.id <> persons.id
                join friends as friends_copy on self.id = friends_copy.first_person_id 
                    or self.id = friends_copy.second_person_id
            where persons.name = 'Tiany';
            """
        )

    def case_11(self):
        """
        11. Numele și vârsta persoanelor cu cel mai mare număr de prieteni.
        """
        self.database.dump(
            """
            select persons.*,
                count(persons.id) as friends
            from persons
                join friends on persons.id = friends.first_person_id 
                or persons.id = friends.second_person_id
            group by persons.id
            having max(count(*))
                );
            """
        )

    def case_12(self):
        """
        12. Pentru fiecare persoană, lista membrilor familiei sale. Dacă A este membru al familiei B și C este membru
            al familiei B, atunci C trebuie să apară în lista membrilor familiei A.
        """
        self.database.dump(
            """
            select distinct kin.first_person_id as A,
                kin.second_person_id as B,
                if(
                    self.first_person_id <> kin.first_person_id 
                        and self.first_person_id <> kin.second_person_id,
                    self.first_person_id,
                    if(
                        self.second_person_id <> kin.first_person_id 
                            and self.second_person_id <> kin.second_person_id,
                        self.second_person_id,
                        null
                    )
                ) as C
            from kin
                join kin as self on kin.second_person_id = self.first_person_id 
                    or kin.second_person_id = self.second_person_id
            having C is not null;
            """
        )

    def case_13(self):
        """
        13. Lista a trei persoane diferite, de vârstă diferită, astfel în cât prima e cea mai în vârstă,
            a doua e mai mică și a treia e cea mai tânără. Lista interogărilor va conține numele persoanelor și ID – ul.
        """
        self.database.dump(
            """
            select *
            from persons
            where id in (
                (select id from persons order by age desc limit 1),
                (select id from persons order by age desc limit 1 offset 1),
                (select id from persons order by age limit 1)
                )
            order by age desc;
            """
        )

    def case_14(self):
        """
        14. Lista persoanelor ce au un membru de familie, dar nu au nici un prieten
        """
        self.database.dump(
            """
            select persons.*,
                count(persons.id)
            from persons
                join kin on persons.id = kin.first_person_id 
                    or persons.id = kin.second_person_id
                left join friends on persons.id = friends.first_person_id 
                    or persons.id = friends.second_person_id
            where friends.first_person_id is null
            group by persons.id
            having count(persons.id) = 1;
            """
        )

