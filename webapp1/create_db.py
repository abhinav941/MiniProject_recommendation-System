import csv
from App.models import Movie
from App import db

with open('new_movie_data.csv','r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        if line[2]:
            rating=float(line[2])
        else:
            rating=0.0
        movie= Movie(name=line[1],rating=rating,Genre=line[3],image=line[4],
        Action=line[5],Adventure=line[6],Animation=line[7],Comedy=line[8],
        Crime=line[9],Documentary=line[10],Drama=line[11],Family=line[12],
        Fantasy=line[13],Foreign=line[14],History=line[15],Horror=line[16],
        Music=line[17],Mystery=line[18],Romance=line[19],Science_Fiction=line[20],
        Tv_Movie=line[21],Thriller=line[22],War=line[23],Western=line[24])
        db.session.add(movie)
    db.session.commit()