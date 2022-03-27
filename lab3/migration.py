from core.migrations import BaseMigration


class Migration(BaseMigration):
    def up(self):
        self.database.execute(
            """
            create table if not exists articles
            (
                id    int unsigned auto_increment primary key,
                title varchar(150)
            );
            """
        )

        self.database.execute(
            """
            create table if not exists universities
            (
                id   int unsigned auto_increment primary key,
                name varchar(150)
            );
            """
        )

        self.database.execute(
            """
            create table if not exists explorers
            (
                id            int unsigned auto_increment primary key,
                name          varchar(150),
                article_id    int unsigned,
                university_id int unsigned,
            
                foreign key (article_id) references articles (id),
                foreign key (university_id) references universities (id),
                unique (article_id, university_id)
            );
            """
        )

    def down(self):
        self.database.execute("drop table if exists articles cascade;")
        self.database.execute("drop table if exists universities cascade;")
        self.database.execute("drop table if exists explorers cascade;")
