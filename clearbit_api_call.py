import json
import clearbit
import sqlite3
import csv

#Place API key in between quotations
clearbit.key = 'sk_1edc5b585fbe8c712f267b1238f9aa66'

#Open connection
conn = sqlite3.connect('leadscoringdb.sqlite')
cur = conn.cursor()

#Initialize the database
cur.execute('''DROP TABLE IF EXISTS company_master''')
cur.execute(
	'''
	CREATE TABLE company_master
	(
		fortune_rank int
		,company_name varchar(128)
		,website varchar(256)
		,sector varchar(256)
	)
	''')

#Read in the Fortune 500 list for the top 30 companies (name + domain)
fhand = open('fortune500list.csv')
data = csv.DictReader(fhand)

for row in data:
	if row['Rank'] < 30:
		cur.execute(
			'''
			INSERT INTO company_master (fortune_rank, company_name, website)
			VALUES (?, ?, ?)
			'''
			,(row['Rank'],row['Title'],row['Website'])
			)
	else:
		continue

conn.commit()
fhand.close()

#Create and populate reference table for tags

fhand = open('tech_tags.csv')
data = csv.DictReader(fhand)

cur.execute('''DROP TABLE IF EXISTS tech_tag_ref''')
cur.execute(
	'''
	CREATE TABLE tech_tag_ref
	(
		tech_name varchar(128)
		,tech_tag varchar(256)
	)
	''')

for row in data:
	cur.execute(
		'''
		INSERT INTO tech_tag_ref
		VALUES (?, ?)
		'''
		, (row['Name'], row['Tech Tag'])
		)

conn.commit()
fhand.close()

#Create look-up/bridge table

cur.execute('''DROP TABLE IF EXISTS tech_tag_lkup''')
cur.execute(
	'''
	CREATE TABLE tech_tag_lkp
	(
		tech_name varchar(128)
		,tech_tag varchar(256)
		,company_name varchar(128)
	)
	''')

conn.commit()
fhand.close()

#Make API call to enrich data

# sqlstr = 'SELECT * FROM company_master ORDER BY fortune_rank'
# cur.execute(sqlstr)
# table = cur.fetchall()

# for row in table:
# 	name = row[1]
# 	website = row[2]
# 	company = clearbit.Company.find(domain=website)

# 	#Extract tags
# 	for item in company['tech']:
# 		cur.execute(
# 			'''
# 			INSERT 
# 			'''
# 			)

# 	#Extract firmographic information
# 	sector = company['category']['sector']
	
# 	if company != None:
# 		cur.execute(
# 			'''
# 			UPDATE company_master SET sector = ? WHERE website = ?
# 			'''
# 			,(sector, website,))
# 	else:
# 		cur.execute(
# 			'''
# 			UPDATE company_master SET sector = 'UNKNOWN' WHERE website = ?
# 			'''
# 			,(website,))

# conn.commit()

# for row in cur.execute(sqlstr):
# 	print(str(row[0]), row[1], row[2], row[3])

# cur.close()