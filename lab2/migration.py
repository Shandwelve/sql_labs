from core.migrations import BaseMigration


class Migration(BaseMigration):

    def up(self):
        self.database.execute(
            """
            create table if not exists persons
            (
                id   int unsigned auto_increment primary key,
                name varchar(100),
                age  smallint
            );
            """
        )

        self.database.execute(
            """
            create table if not exists friends
            (
                first_person_id  int unsigned,
                second_person_id int unsigned,
            
                foreign key (first_person_id) references persons (id),
                foreign key (second_person_id) references persons (id),
                primary key (first_person_id, second_person_id)
            );
            """
        )

        self.database.execute(
            """
            create table if not exists kin
            (
                first_person_id  int unsigned,
                second_person_id int unsigned,
            
                foreign key (first_person_id) references persons (id),
                foreign key (second_person_id) references persons (id),
                primary key (first_person_id, second_person_id)
            );
            """
        )

    def down(self):
        self.database.execute("drop table if exists kin cascade;")
        self.database.execute("drop table if exists friends cascade;")
        self.database.execute("drop table if exists persons cascade;")


