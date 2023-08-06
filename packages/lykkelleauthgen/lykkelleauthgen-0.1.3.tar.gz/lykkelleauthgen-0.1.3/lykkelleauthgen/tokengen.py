from lykkelleconf.connecteod import connect
import psycopg2 as pgs
import random
import string

class authenticate:
    # randomizer program
    def randomizer(letters_count, digits_count, spl_count):
        val = string.punctuation
        val = val.translate({ord("""'"""): None})
        val = val.translate({ord('"'): None})
        sample_str = ''.join((random.choice(string.ascii_letters) for i in range(letters_count)))
        sample_str += ''.join((random.choice(string.digits) for i in range(digits_count)))
        sample_str += ''.join((random.choice(val) for i in range(spl_count)))

        # Convert string to list and shuffle it to mix letters and digits
        sample_list = list(sample_str)
        random.shuffle(sample_list)
        final_string = ''.join(sample_list)
        return final_string
    def __init__(self, userkey):
 #load all existing keys from table
        conn = connect.create()
        cursor = conn.cursor()
        with conn:
            cursor.execute("select current_database()")
            mydb = cursor.fetchone()
            mydb = mydb[0]
            devdb = ['lykkelledev_db','lykkelleut_db']
            self.mydb = mydb
            try:
                cursor.execute("""select auth_token, user_key from lyk_admin""")
                tokenlist = cursor.fetchall()
            except pgs.Error as e:
                print(e.pgerror)
                tokenlist = None
            if tokenlist is None:
                tokenlist = []
            tokens = []
            userkeys = []
            if len(tokenlist) > 0:
                for i in range(len(tokenlist)):
                    val = tokenlist[i][0]
                    val2 = tokenlist[i][1]
                    tokens.append(val)
                    userkeys.append(val2)
            else:
                print("LYK_ADMIN table is empty")
            print(userkeys)
            if userkey in userkeys:
                lc = 10
                nc = 10
                sc = 10
                is_valid = 0
                while is_valid == 0:
                    newtoken = authenticate.randomizer(lc, nc, sc)
                    if newtoken in tokens:
                        pass
                    else:
                        is_valid = 1
                #updating the table with new token
                updq = """update lyk_admin set auth_token=%s where user_key=%s"""
                try:
                    if mydb in devdb:
                        pass
                        self.newtoken = newtoken
                    else:
                        cursor.execute(updq, (newtoken, userkey))
                        print("update of new token to account of", userkey, " is successful")
                        self.newtoken = newtoken
                except pgs.Error as e:
                    print(e.pgerror)
                    self.newtoken = -999
            else:
                self.newtoken = -899


