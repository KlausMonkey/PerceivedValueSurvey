import argparse
import csv
import datetime
import os
import sys
import time
import string
import random

import MySQLdb


def main():
    # 1 - Log Session - first generate a new session key, then insert into the DB
    sessionkey = id_generator()
    sessionid = insert_session(sessionkey)
    print 'New Session ID : %s' % str(sessionid)

    # 2 - Create User Records
    email = "FRANK." + id_generator(3,"ABCDEFGHIJKLMNOPQRSTUVWXYZ") + "@GMAIL.COM"
    street_address = id_generator(5,"1234567890") + " MAIN ST"
    city = id_generator(10,"ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    state = id_generator(2,"ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    zipcode = id_generator(5,"1234567890")
    firstname = "FRANK" + id_generator(3,"ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    lastname = "JONES"+ id_generator(3,"ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    userid = insert_user(email, street_address, city, state, zipcode, firstname, lastname)
    print 'New User ID : %s' % str(userid)

    # 3 - Create User-Session Record
    user_session_id = insert_user_session(userid, sessionid)
    print 'New User Session ID : %s' % str(user_session_id)

    # 4 - Prompt user for property values for X, Y, Z
    x_empty_value = raw_input('Enter Value for House X (vacant):')
    y_empty_value = raw_input('Enter Value for House Y (vacant):')
    z_empty_value = raw_input('Enter Value for House Z (vacant):')

    # 5 - Store values in memory and in SQL
    x_empty_property_id = select_property('X', 'EMPTY')
    y_empty_property_id = select_property('Y', 'EMPTY')
    z_empty_property_id = select_property('Z', 'EMPTY')
    sql = 'INSERT INTO efurn_marketing.property_value (UserSessionID, PropertyID, PropertyValue) VALUES (%s, %s, %s); ' % (
    user_session_id, x_empty_property_id, x_empty_value)
    # sql += 'INSERT INTO efurn_marketing.property_value (UserSessionID, PropertyID, PropertyValue) VALUES (%s, %s, %s); ' % (
    # user_session_id, y_empty_property_id, y_empty_value)
    # sql += 'INSERT INTO efurn_marketing.property_value (UserSessionID, PropertyID, PropertyValue) VALUES (%s, %s, %s);' % (
    # user_session_id, z_empty_property_id, z_empty_value)
    # print sql
    # insert_property_value(sql)

    # 6 - Get First Question

# 7 - Print Question and Prompt for response
# 5 - Store values in memory and in SQL (list of dicts [{Q1: A}, {Q2: B}, etc.] )
# 8 - Is Correct answer required?  If Yes, and incorrect answer given, exit
# 9 - Is Last Question?  If Yes, GOTO "Done"
# ELSE Get Next Question
# DONE - Calculate final value, store in SQL
# PRINT final value


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def select_property(property_code, staging_status):
    x = conn.cursor()
    sql = "SELECT PropertyID FROM efurn_marketing.property WHERE PropertyCode = "'"%s"'" AND StagingStatus = "'"%s"'"" %(property_code, staging_status)
    x.execute(sql)
    for row in x:
        property_id = row[0]
    return property_id
    conn.close()

def insert_property_value(sql):
    x = conn.cursor()
    try:
        cur.execute(sql)
        conn.commit()
    except:
        conn.rollback()
    conn.close()

def insert_user_session(userid, sessionid):
    x = conn.cursor()
    sql = 'INSERT INTO efurn_marketing.user_session(UserID, SessionID) VALUES (%s, %s)' %(userid, sessionid)
    try:
        x.execute(sql)
        conn.commit()
        return select_user_session(userid, sessionid)
    except:
        conn.rollback()
    conn.close()

def select_user_session(userid, sessionid):
    x = conn.cursor()
    sql = 'SELECT UserSessionID FROM efurn_marketing.user_session WHERE UserID = %s AND SessionID = %s' %(userid, sessionid)
    x.execute(sql)
    for row in x:
        user_session_id = row[0]
    return user_session_id
    conn.close()

def insert_user(email, street_address, city, state, zipcode, firstname, lastname):
    x = conn.cursor()
    sql = \
        "INSERT INTO efurn_marketing.user(Email, StreetAddress, City, State, Zipcode, FirstName, LastName) " \
        "VALUES ("'"{}"'","'"{}"'","'"{}"'","'"{}"'","'"{}"'","'"{}"'","'"{}"'"" \
        ")".format(email, street_address, city, state, zipcode, firstname, lastname)
    try:
        x.execute(sql)
        conn.commit()
        return select_user(email)
    except:
        conn.rollback()
    conn.close()

def select_user(email):
    x = conn.cursor()
    sql = "SELECT UserID FROM efurn_marketing.user WHERE Email = "'"%s"'"" %email
    x.execute(sql)
    for row in x:
        user_id = row[0]
    return user_id
    conn.close()

def insert_session(session_key):
    x = conn.cursor()
    sql = "INSERT INTO efurn_marketing.session (SessionKey, StartTime, EndTime) VALUES ("'"%s"'", NOW(), NULL)" %session_key
    try:
        x.execute(sql)
        conn.commit()
        return select_session(session_key)
    except:
        conn.rollback()
    conn.close()

def select_session(session_key):
    x = conn.cursor()
    sql = "SELECT SessionID FROM efurn_marketing.session WHERE SessionKey = "'"%s"'"" %session_key
    x.execute(sql)
    for row in x:
        session_id = row[0]
    return session_id
    conn.close()

if __name__ == '__main__':
    conn = MySQLdb.connect(host="localhost",
                           user="efurn",
                           passwd="@#$WSDF50sl;msdf",
                           db="efurn_marketing")
    sys.exit(main())
