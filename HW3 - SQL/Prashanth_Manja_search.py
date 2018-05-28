import sys
import mysql.connector
cnx = mysql.connector.connect(user='root', password='root',host='127.0.0.1',database='sakila')
cursor = cnx.cursor()
keyword1=sys.argv[1].lower();
keyword2=sys.argv[2].lower();
query = "select count(distinct(r.customer_id)) as no_of_customers from rental r join customer c on r.customer_id=c.customer_id join inventory i on r.inventory_id=i.inventory_id join film_category fc on i.film_id=fc.film_id join category ca on fc.category_id=ca.category_id where ca.name='"+keyword1+"' and r.customer_id not in (select r.customer_id from rental r join customer c on r.customer_id=c.customer_id join inventory i on r.inventory_id=i.inventory_id join film_category fc on i.film_id=fc.film_id join category ca on fc.category_id=ca.category_id where ca.name='"+keyword2+"')"
cursor.execute(query)
for name in cursor:
    print name[0]
cursor.close()
cnx.close()
