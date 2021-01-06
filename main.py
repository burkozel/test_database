from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#основная часть
performers = ['Markul', 'Скриптонит', 'MACAN', 'Би-2', 'Madonna', 'Louis Armstrong', 'Eric Clapton', 'Bones']
genres = ['Cloud rap', 'Rock', 'Rap', 'Jazz', 'Blues']
albums = [['2004', 2018], ['Scumbag', 2013], ['Great Depression', 2017], ['Moulin Rouge', 2018], ['Powder', 1983], ['Layla and Other Assorted Love Songs', 1970], ['Ella and Louis ', 1956], ['Кино', 2020]]
tracks = [['Москва любит...', 2018, 3.25, 1], ['Цепи', 2018, 3.27, 2], ['Moulin Rouge', 2018, 3.52, 3],
          ['A New Argentina', 1996, 5.17, 4], ['American Life', 2000, 3.35, 5], ['Let You Down', 2017, 4.34, 6],
          ['Серпантин', 2017, 4.35, 7], ['OXYGEN', 2015, 2.58, 8], ['Мой рок-н-ролл', 2001, 6.47, 1],
          ['Пора возвращаться домой', 2001, 8.01, 2], ['Dark Night', 2009, 4.34, 1], ['What A Wonderful World', 1967, 3.56, 3],
          ['If you knew', 2018, 2.32, 3], ['Троллейбус', 1986, 3.26, 5], ['Мультибрендовый', 2017, 4.32, 8], ['Положение', 2017, 4.43, 7]]
collections = [['Нравится', 2020], ['Хиты уходящего года', 2021], ['Классика', 2001], ['Музыка для релакса', 2015],
               ['Радио', 2020], ['Под новый год', 2018], ['ВК одобряет', 2020], ['Моя музыка', 2015]]

#рабочая часть
CT = [[1, 2], [1, 8], [2, 4], [3, 5], [1, 5], [6, 7], [5, 3], [6, 2], [7, 1], [8, 3], [8, 5]]
PA = [[2, 1], [8, 2], [1, 3], [1, 4], [5, 5], [7, 6], [6, 7], [3, 8], [3, 1], [2, 3], [4, 1], [8, 6]]
PG = [[1, 1], [1, 2], [2, 3], [3, 1], [4, 2], [4, 4], [5, 4], [5, 5], [6, 5], [7, 4], [8, 1], [8, 3]]

options = 'postgresql://postgres:admin@localhost:5432/test_database'
db = create_engine(options)
base = declarative_base()

#основная часть
class Track(base):
    __tablename__ = 'Трек'
    trackid = Column(INTEGER, primary_key=True)
    year = Column(NUMERIC(4, 0), nullable=False)
    name = Column(VARCHAR(100), nullable=False)
    duration = Column(NUMERIC(3, 2), nullable=False)
    collection = Column(VARCHAR(100), nullable=False)
    albumid = Column(INTEGER, ForeignKey('album.albumid'), nullable=False)

class Album(base):
    __tablename__ = 'Альбом'
    albumid = Column(INTEGER, primary_key=True)
    year = Column(NUMERIC(4, 0), nullable=False)
    name = Column(VARCHAR(100), nullable=False)

class Genre(base):
    __tablename__ = 'Жанр'
    genreid = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(100), nullable=False)

class Performer(base):
    __tablename__ = 'Исполнитель'
    performerid = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(100), nullable=False, unique=True)
    alias = Column(VARCHAR(100), nullable=False, unique=True)

class Collection(base):
    __tablename__ = 'Коллекции'
    collectionid = Column(INTEGER, primary_key=True)
    year = Column(NUMERIC(4, 0), nullable=False)
    name = Column(VARCHAR(100), nullable=False)
#_____________________________________________________________________________________________

#рабочая часть
class PerformerGenre(base):
    __tablename__ = 'PG'
    performergenreid = Column(INTEGER, primary_key=True)
    performerid = Column(INTEGER, ForeignKey('performer.performerid'), nullable=False)
    genreid = Column(INTEGER, ForeignKey('genre.genreid'), nullable=False)

class PerformersAlbum(base):
    __tablename__ = 'PA'
    performeralbumid = Column(INTEGER, primary_key=True)
    performerid = Column(INTEGER, ForeignKey('performer.performerid'), nullable=False)
    albumid = Column(INTEGER, ForeignKey('album.albumid'), nullable=False)

class CollectionTrack(base):
    __tablename__ = 'CT'
    collectiontrackid = Column(INTEGER, primary_key=True)
    collectionid = Column(INTEGER, ForeignKey('collection.collectionid'), nullable=False)
    trackid = Column(INTEGER, ForeignKey('track.trackid'), nullable=False)
#_____________________________________________________________________________________________

Session = sessionmaker(db)
session = Session()
base.metadata.create_all(db)

for performer1 in performers:
    performer = Performer(name=performer1)
    session.add(performer)

for g in genres:
    genre = Genre(name=g)
    session.add(genre)

for album1 in albums:
    album = Album(name=album1[0], year=album1[1])
    session.add(album)

for collection1 in collections:
    collection = Collection(name=collection1[0], year=collection1[1])
    session.add(collection)

for track1 in tracks:
    track = Track(name=track1[0], year=track1[1], duration=track1[2], albumid=track1[3])
    session.add(track)

for pg in PG:
    perf_genre = PerformerGenre(performerid=pg[0], genreid=pg[1])
    session.add(perf_genre)

for pa in PA:
    perf_album = PerformersAlbum(performerid=pa[0], albumid=pa[1])
    session.add(perf_album)

for ct in CT:
    collection_track = CollectionTrack(collectionid=ct[0], trackid=ct[1])
    session.add(collection_track)

session.commit()

#tracks 2018
for p in session.execute(select([Album.name, Album.year]).where(Album.year == '2018')):
    print(f'{p[0]}, {p[1]}')

#the longest
res = session.execute(select([Track.name, Track.duration]).order_by(Track.duration)).fetchone()
print(f'{res[0]}, {str(res[1])}')

#3,5 - length
for p in session.execute(select([Track.name]).where(Track.duration >= 3.30)):
    print(p[0])

#2018-2020
for p in session.execute(select([Collection.name]).where(and_(Collection.year >= 2018, Collection.year <= 2020))):
    print(p[0])

#performers 1 wordе
for p in session.execute(select([Performer.name]).where((func.length(Performer.name) - func.length(func.replace(Performer.name, ' ', '')) + 1) == 1)):
    print(p[0])

#my
for p in session.execute(select([Track.name]).where(func.lower(Track.name).ilike('%my%'))):
    print(p[0])
