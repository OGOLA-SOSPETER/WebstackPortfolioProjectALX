import sqlite3

connection = sqlite3.connect('waitlistdatabase.db')
with open('waitschema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO awaitrecipes (rimage,rname, rdescription,rcategory,ringredients,rprocedure) VALUES (?, ?, ?, ?, ?, ?)",
            ('https://img.freepik.com/premium-photo/tortilla-wrap-with-falafel-fresh-salad-vegan-tacos-vegetarian-healthy-food_2829-6192.jpg?size=626&ext=jpg&ga=GA1.2.1484222175.1666153080&semt=robertav1_2_sidr', 'First Post', 'Content for the first post','breakfast','qwerty','werty')
            )

cur.execute("INSERT INTO awaitrecipes (rimage,rname, rdescription,rcategory,ringredients,rprocedure) VALUES (?, ?, ?, ?, ?, ?)",
            ('https://img.freepik.com/free-photo/penne-pasta-tomato-sauce-with-chicken-tomatoes-wooden-table_2829-19744.jpg?size=626&ext=jpg&ga=GA1.2.1484222175.1666153080&semt=robertav1_2_sidr', 'Second Post', 'Content for the second post','breakfast','qwerty','werty')
            )

connection.commit()
connection.close()