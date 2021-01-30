import psycopg2
import data

conn = psycopg2.connect(data.DB_URL)
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS expense (
	                id serial NOT NULL,
	                name TEXT NOT NULL,
	                datetime VARCHAR(10) NOT NULL,
	                type TEXT NOT NULL,
	                amount FLOAT NOT NULL,
	                CONSTRAINT expense_pk PRIMARY KEY (id)
                    ) WITH (
                        OIDS=FALSE
                        )''')


cursor.close()
conn.commit()
conn.close()
