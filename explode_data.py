# User - id, username, firstname, lastname, bio, gender, dob
# Post - id, user, title, paragraph, likes, comments
# Comments - id, user, post, comment_text, replies, likes 
# Replies - id, user, comment, reply_text, likes
# Friends - id, initiator, acceptor, status - ['rejected', 'accepted', 'pending', 'cancelled'], approach_count

# User - id, username, firstname, lastname, bio, gender, dob

from faker import Faker
import random

from pprint import pprint

import psycopg2

from psycopg2.extras import execute_values
from psycopg2.errors import UndefinedTable


db_conf =  {
            'host': 'localhost',
            'port': 5432,
            'database': 'exploded',
            'user': 'postgres',
            'password': 'postgres',
        }

connection = psycopg2.connect(**db_conf)
cursor = connection.cursor()

users_table = '''create table if not exists users(
                id int,
                username varchar(45) NOT NULL,
                firstname varchar(50),
                lastname varchar(50), bio varchar, gender varchar(4), dob date,
                primary key (id)
            )
        '''

# Post - id, user, title, post_text, likes, comments
post_table = ''' create table if not exists post(
               id int,
               users int,
               comments int,
               title varchar(440),
               post_text text,
               likes int,
               primary key (id)
           )
        '''
post_user_constraint = '''
    alter table post
        add foreign key (users)
        references users (id)
    '''
post_comment_constraint = '''
    alter table post
        add foreign key (comments)
        references comment (id)
    '''

# users int references users,
# posts int references post,
# replies int references reply,
# Comments - id, users, posts, comment_text, replies, likes 
comment_table = ''' create table if not exists comment (
               id int,
               users int,
               posts int,
               replies int,
               comment_text text,
               likes int,
               primary key (id)
           )
        '''
comment_user_constraint = ''' 
        alter table comment
        add foreign key (users)
        references users (id)
    '''
comment_post_constraint = '''
        alter table comment
        add foreign key (posts)
        references post (id)
    '''

comment_reply_constraint = '''
        alter table comment
        add foreign key (replies)
        references reply (id)
    '''

reply_table = ''' create table if not exists reply (
               id int,
               users int,
               comments int,
               reply_text text,
               likes int,
               primary key (id)
           )
        '''
reply_user_constraint = '''
        alter table reply
        add foreign key (users)
        references users (id)
    '''

reply_comment_constraint = '''
        alter table reply
        add foreign key (comments)
        references comment (id)
    '''

friend_table = ''' create table if not exists friend (
                       id int,
                       initiator int,
                       acceptor int,
                       status char(20),
                       approach_count int,
                       primary key (id)
                   )
                '''
friend_user_send_constraint = '''
        alter table friend
        add constraint fk_initiator
        foreign key (initiator)
        references users (id)
    '''

friend_user_receive_constraint = '''
        alter table friend
        add constraint fk_acceptor
        foreign key (acceptor)
        references users (id)
    '''


def create_tables():
    cursor.execute(users_table)
    cursor.execute(post_table)
    cursor.execute(reply_table)
    cursor.execute(comment_table)
    cursor.execute(friend_table)
    connection.commit()

def create_constraints():
    cursor.execute(post_user_constraint)
    cursor.execute(post_comment_constraint)
    cursor.execute(comment_user_constraint)
    cursor.execute(comment_post_constraint)
    cursor.execute(comment_reply_constraint)
    cursor.execute(reply_comment_constraint)
    cursor.execute(reply_user_constraint)
    cursor.execute(friend_user_send_constraint)
    cursor.execute(friend_user_receive_constraint)
    connection.commit()

def drop_tables():
    tables = ['users', 'post', 'comment', 'reply', 'friend']
    for table in tables:
        try:
            cursor.execute('drop table %s cascade' % table)
        except UndefinedTable:
            pass
    connection.commit()

faker = Faker()

def get_username():
    return faker.user_name() + str(random.choice(range(1,1000)))

def get_firstname():
    return faker.first_name()

def get_lastname():
    return faker.last_name()

def get_paragraph():
    return '\n'.join(faker.paragraphs())

def get_gender():
    return random.choice(['M', 'F', 'NB'])

def get_dob():
    return faker.date_of_birth()

def get_comment_or_reply():
    return faker.paragraph()

def get_title():
    return ' '.join(random.choice(faker.text().split()) for i in range(random.choice(range(1,10))))

# Populate a lac users
def explode_users(count):
    rows = []
    for i in range(count):
        # User - id, username, firstname, lastname, bio, gender, dob
        row = [i, get_username(), get_firstname(), get_lastname(), get_title(), get_gender(), get_dob()]
        rows.append(row)
    execute_values(cursor, "insert into users(id, username, firstname, lastname, bio, gender, dob) values %s", rows)
    connection.commit()
    print('exploded users')

def explode_posts(count, comment_count, user_count):
    rows = []
    for i in range(count):
        # Post - id, users, title, post_text, likes, comments
        row = [
                i, random.choice(range(user_count)), get_title(), get_paragraph(),
                random.choice(range(comment_count)), random.choice(range(10000))
            ] 
        rows.append(row)
    execute_values(cursor, "insert into post (id, users, title, post_text, comments, likes) values %s", rows)
    connection.commit()
    print('exploded posts')

def explode_comment(count, user_count, post_count, reply_count):
    rows = []
    for i in range(count):
        row = [
                i, random.choice(range(user_count)), random.choice(range(post_count)),
                get_comment_or_reply(), random.choice(range(reply_count)), random.choice(range(10000))
            ]
        # Comments - id, users, posts, comment_text, replies, likes 
        rows.append(row)
    execute_values(cursor, "insert into comment (id, users, posts, comment_text, replies, likes) values %s", rows)
    connection.commit()
    print('exploded comment')

def explode_replies(count, user_count, comment_count):
    rows = []
    for i in range(count):
        # Replies - id, user, comment, reply_text, likes
        row = [i, random.choice(range(user_count)), random.choice(range(comment_count)), get_comment_or_reply(), random.choice(range(int(1e4)))]
        rows.append(row)
    execute_values(cursor, "insert into reply (id, users, comments, reply_text, likes) values %s", rows)
    connection.commit()
    print('exploded replies')

def explode_friends(count, user_count):
    rows = []
    for i in range(count):
        initiator, acceptor = random.choice(range(user_count)), random.choice(range(user_count))
        while (initiator == acceptor):
            initiator, acceptor = random.choice(range(user_count)), random.choice(range(user_count))
        status = random.choice(['rejected', 'accepted', 'pending', 'cancelled'])
        approach_count = random.choice(range(100))
        # Friends - id, initiator, acceptor, status - ['rejected', 'accepted', 'pending', 'cancelled'], approach_count
        row = [i, initiator, acceptor, status, approach_count]
        rows.append(row)
    execute_values(cursor, "insert into friend (id, initiator, acceptor, status, approach_count) values %s", rows)
    connection.commit()
    print('exploded friends')


def explode(user_count, post_count, comment_count, reply_count, friend_count):
    # Rollback any pending transaction
    cursor.execute('rollback')

    drop_tables()
    create_tables()

    explode_users(user_count)
    explode_posts(post_count, comment_count, user_count)
    explode_comment(comment_count,user_count,post_count, reply_count)
    explode_replies(reply_count, user_count, comment_count)
    explode_friends(friend_count,user_count)

    create_constraints()
    cursor.close()
    connection.close()


if __name__ == '__main__':
    import time
    start = time.time()
    million = int(1e6)
    user_count = million
    post_count = 2*million # on avg each user has 2 posts
    comment_count = 6*million # on avg each post has 3 comments
    reply_count = 6*million # on avg each comment has a single reply
    friend_count = 10*million # on avg each user has 10 friends

    with open('benched.txt', 'a') as fw:
        explode(user_count, post_count, comment_count, reply_count, friend_count)
        fw.write('inserted %s users-data in %s seconds\n' % (user_count, time.time()-start))
        print('inserted %s users-data in %s seconds' % (user_count, time.time()-start))
