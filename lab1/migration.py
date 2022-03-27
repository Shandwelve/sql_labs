from core.migrations import BaseMigration


class Migration(BaseMigration):
    def up(self):
        self.database.execute(
            """
            create table if not exists films
            (
                id       int unsigned primary key,
                title    varchar(100),
                director varchar(100),
                age      year(4)
            );
            """
        )

        self.database.execute(
            """
            create table if not exists actors
            (
                id   int unsigned primary key,
                name varchar(100)
            );
            """
        )

        self.database.execute(
            """
            create table if not exists filmography
            (
                actor_id int unsigned,
                film_id  int unsigned,
                role     varchar(100),
                salary   smallint unsigned,

                primary key (actor_id, film_id),
                foreign key (actor_id) references actors (id),
                foreign key (film_id) references films (id)
            );
            """
        )

    def down(self):
        self.database.execute("drop table if exists filmography cascade;")
        self.database.execute("drop table if exists actors cascade;")
        self.database.execute("drop table if exists films cascade;")

