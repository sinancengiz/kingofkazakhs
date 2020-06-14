# dependencies
import datetime

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *

DATABASE = SqliteDatabase("game_database.db")

class Player(UserMixin, Model):
    player_name = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default = datetime.datetime.now) 
    is_admin = BooleanField(default=False)
    gold = IntegerField(default=1000)
    food = IntegerField(default=1000)
    wood = IntegerField(default=1000)
    stone = IntegerField(default=1000)
    research_point = IntegerField(default=1000)
    game_year = IntegerField(default=650)

    class Meta:
        database = DATABASE
        order_by = ("joined_at",)
    

    @classmethod
    def create_player(cls, player_name, email, password, admin=False):
        try:
            cls.create(
                player_name = player_name,
                email = email,
                password = generate_password_hash(password),
                is_admin = admin
            )
        except IntegrityError:
            raise ValueError("Player is already exist!!!!")


class City(Model):
    city_name = CharField(unique=True)
    king_of_city = ForeignKeyField(Player, to_field="player_name")
    population_max = IntegerField(default=5000)
    city_level = IntegerField(default=1)
    academy = IntegerField(default=1)
    stable_level = IntegerField(default=1)
    barracks = IntegerField(default=1)
    farm = IntegerField(default=1)
    gold_mine = IntegerField(default=1)
    stone_quary = IntegerField(default=1)
    lumberjack = IntegerField(default=1)
    wall_level = IntegerField(default=1)

    class Meta:
        database = DATABASE

    @classmethod
    def create_city(cls , king_of_city, city_name):
        try:
            cls.create(
                king_of_city = king_of_city,
                city_name = city_name
            ) 

        except IntegrityError:
            raise ValueError("Player is already exist!!!!")


class Population(Model):
    king_name = ForeignKeyField(Player, to_field="player_name")
    total_population = IntegerField(default=1000)
    unassingned_population = IntegerField(default=200)
    farmer = IntegerField(default=300)
    stone_worker = IntegerField(default=100)
    gold_miner = IntegerField(default=100)
    lumberjack = IntegerField(default=100)
    spearman = IntegerField(default=100)
    swordsman = IntegerField(default=30)
    archers = IntegerField(default=20)
    ligth_cavalry = IntegerField(default=20)
    heavy_cavalry = IntegerField(default=10)
    mounted_archer = IntegerField(default=20)

    class Meta:
        database = DATABASE
    @classmethod
    def create_population(cls , king_name):
        try:
            cls.create(
                king_name = king_name
            ) 

        except IntegrityError:
            raise ValueError("Player is already exist!!!!")



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Player,City,Population], safe=True)
    DATABASE.close()