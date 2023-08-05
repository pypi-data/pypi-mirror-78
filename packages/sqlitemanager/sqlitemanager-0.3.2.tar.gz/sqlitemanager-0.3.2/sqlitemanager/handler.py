from database import (
    Database,
    Table,
    Record,
)

from helpers import (
    get_localpath,
    check_existance,
)

class SQLiteHandler(object):
    def __init__(self, filename="", path=""):
        
        self.database = None
        if filename != "":
            if path == "":
                path = get_localpath()
            
            self.database_init(filename = filename, path = path)

    def database_init(self, filename, path):
        # try:
        self.database = Database(
            filename=filename,
            path=path,
        )
        
        # except:
        #     print(f"Couldn't initialize database!")

    def database_new(self, filename, path=""):
        """
        initialises database only if it doesnt exist yet
        """
        if path == "":
            path = get_localpath()

        exists = check_existance(filename, path)

        if exists == True:
            print(f"Couldnt create database, database with filename {filename} at directory {path} already exists!")
        else:
            self.database_init(filename=filename, path=path)

    def database_saveas(self, filename, path=""):
        self.database.saveas_database(filename=filename, path=path)

    def database_open(self, filename, path=""):
        """
        initialises database only if it already exists
        """

        if path == "":
            path = get_localpath()

        exists = check_existance(filename, path)

        if exists == True:
            self.database_init(filename=filename, path=path)
        else:
            print(f"Couldnt open database, database with filename {filename} at directory {path} doesn't exist!")

    def database_close(self):

        if self.database != None:
            self.database.close_database()
            self.database = None
        else:
            print(f"Couldn't close database, not connected to one!")

    def database_delete(self):
        
        if self.database != None:
            self.database.delete_database()
            self.database = None
        else:
            print(f"Couldn't delete database, not connected to one!")

    def table_sync(self, tablename):
        
        table = self.database.tables[tablename]
        sqlrecords = self.database.read_records(tablename=tablename, columns=table.column_names)
        table.records = self.transform_sql_to_record(table=table, sqlrecords=sqlrecords)

    def table_add_records(self, tablename, records):

        table = self.database.tables[tablename]
        self.database.add_records(
            table,
            records,
        )

        self.table_sync(tablename)

    def table_update_records(self, tablename, valuepairs, where):
        """
        update specific records of the specified table

        if where is an integer, it will update the row with that primary key.
        otherwise a valuepair is expected in the form 
        [<columnname>, [<values]]
        """

        if isinstance(where, int):
            where = [["id", [where]]]

        self.database.update_records(
            tablename=tablename, 
            valuepairs = valuepairs,
            where=where,
        )

    def table_read_records(self, tablename, where=[]):

        table = self.database.tables[tablename]

        if where == []:
            records = table.records
        else:
            sqlrecords = self.database.read_records(tablename=tablename, columns=table.column_names, where=where)
            records = self.transform_sql_to_record(table=table, sqlrecords=sqlrecords)
            # print(f"{self.name} records retrieved: {self.records}")

        return records

    def table_read_foreign_records(self, tablename, column, where=[]):
        """
        for a particular tableobject and column,
        checks if column is a foreign key
        if so finds the table it points to and gets the records.
        if a where is given, only give the foreign value(s) that are linked to the found rows
        records will be returned as an array of record objects
        """

        table = self.database.tables[tablename]

        # check if the column points to a foreign key
        columnindex = table.column_names.index(column)
        split = table.column_types[columnindex].split(' ', 3)
        if len(split) != 3:
            return
        if split[1].upper() != "REFERENCES":
            return
        
        # get the reference to the foreign table
        foreign_table_name = split[2].split('(',1)[0]
        foreign_table = self.database.tables[foreign_table_name]
        print(f"foreign table {foreign_table}")

        # get the records from the foreign table
        recordobjects = self.table_read_records(foreign_table)
        print(f"record objects of foreign table {recordobjects}")

        # get the foreign keys to filter on
        records = self.table_read_records(tablename=tablename, where=where)
        foreign_keys = []
        for record in records:
            foreign_keys += [record.recorddict[column]]

        return recordobjects

    def crossref_create(self, tablename1, tablename2):
        """
        Creates a crossreference table for tables with given table names.
        Next to the columns that contain the foreign keys, a column for a description is made for additional info.
        """

        crossref_table = handler.database.create_table(
            name = f"CROSSREF_{tablename1}_{tablename2}",
            column_names=[f"{tablename1}_id", f"{tablename2}_id", "description"],
            column_types=[f"INTEGER REFERENCES {tablename1}(id)", f"INTEGER REFERENCES {tablename2}(id)", "TEXT"],
        )

        return crossref_table

    def crossref_get_all(self, tablename):
        """
        loops over all the tables in the database.
        If they start with CROSSREF, checks if the name contains this tablename.
        if they do, find also the table it points to
        get an array of all the found tables and return it
        """

        tables = []

        for key in self.database.tables:
            if ("CROSSREF" in key) and (tablename in key):
                crossrefname = key
                key = key.replace("CROSSREF", '')
                key = key.replace(tablename, '')
                key = key.replace('_', '')

                table = self.database.tables[key]
                tables += [table]

        return tables       

    def crossref_get_one(self, tablename1, tablename2):
        """
        loops over all the tables in the database.
        If they start with CROSSREF and contain both the table names, find the table it points to
        return the found table
        """

        for tablename in self.database.tables:
            if ("CROSSREF" in tablename) and (tablename1 in tablename) and (tablename2 in tablename):
                table = self.database.tables[tablename]
                break

        return table

    def crossref_add_record(self, tablename1, tablename2, where1, where2, description=""):
        """
        adds a crossreference between tables 1 and 2 for the rows given by the where statements.
        Creates links for any combination of the found rows of table1 and table 2. So if the where statements point to multiple rows,
        like 1-3 in table 1 and 5-8 in table 2, it loops over all possible combinations:
        1 - 5
        1 - 6
        1 - 7
        1 - 8

        2 - 5
        2 - 6
        2 - 7
        2 - 8

        3 - 5
        3 - 6
        3 - 7
        3 - 8
        """

        table1 = self.database.tables[tablename1]
        table2 = self.database.tables[tablename2]

        # get the cross reference table
        crossref = self.crossref_get_one(
            tablename1 = tablename1,
            tablename2 = tablename2, 
            )

        # print(f"where1 is {where1}")
        # get record primary keys / row id's
        if isinstance(where1[0], int):
            rowids1 = where1
        else:
            rowids1 = []
            records = self.table_read_records(
                tablename = tablename1,
                where = where1,
            )
            for record in records:
                rowids1 += [record.primarykey]
        # print(f"rowids1 is {rowids1}")

        # print(f"where2 is {where2}")
        if isinstance(where2[0], int):
            rowids2 = where2
        else:
            rowids2 = []
            records = self.table_read_records(
                tablename = tablename2,
                where = where2,
            )
            for record in records:
                rowids2 += [record.primarykey]
        # print(f"rowids2 is {rowids2}")

        # determine if tables need to be switched places
        index1 = crossref.name.find(tablename1)
        index2 = crossref.name.find(tablename2)

        if (index1 == -1) or (index2 == -1):
            print(f"table1 {tablename1} or table2 {tablename2} not found")
            return

        # switch columns
        values1 = rowids1 if index1 < index2 else rowids2
        values2 = rowids2 if index1 < index2 else rowids1

        records = []
        for value1 in values1:
            for value2 in values2:
                # default description
                if description == "":
                    description = f"Cross referenced {where1} to {where2}"

                record = self.record_create(
                    tablename=crossref.name,
                    values=[
                        value1, value2, description
                    ]
                )
                records += [record]

        self.table_add_records(crossref.name, records)

    def crossref_read_records(self, tablename1, tablename2):

        table = self.crossref_get_one(tablename1=tablename1, tablename2=tablename2)
        records = self.table_read_records(table.name)

        return records

    def crossref_read_record(self, tablename1, tablename2, rowid):
        """
        reads the crossreference table and retrieves only elements for the rowid given of table1
        """

        table = self.crossref_get_one(tablename1, tablename2)
        # print(table.name)
        records = self.table_read_records(table.name)
        
        # print(records)

        records_found = []
        for record in records:
            for valuepair in record.valuepairs:
                if valuepair[0] == tablename1 + "_id":
                    if valuepair[1] == rowid:
                        records_found += [record]
                        break

        return records

    def record_create(self, tablename, values=[]):
        """
        creates a draft record that can still be 
        manipulated before making it definitive
        if values are empty, takes default values of the columns

        can be added to the table through
        table_add_records method
        """

        table = self.database.tables[tablename]

        if values == []:
            recordarray = table.defaults
        else:
            recordarray = [-1] + values

        record = Record(
            table.column_names,
            recordarray,
        )
        print(f"created record with recordarray {record.recordarray}")
        return record

    def records_create(self, tablename, recordsvalues):
        """
        creates multiple draft records that can still be 
        manipulated before making it definitive

        can be added to the table through
        table_add_records method
        """

        records = []
        for values in recordsvalues:
            records += [self.record_create(tablename, values)]

        return records

    def transform_sql_to_record(self, table, sqlrecords):
        """
        uses table object as input, as its used privately and not made to be called directly by using application
        """

        # print(sqlrecords)

        records = []
        for record in sqlrecords:

            recordarray = []
            for value in record:
                recordarray += [value]

            recordobject = Record(table.column_names, recordarray)
            # print(f"recordarray: {recordobject.recordarray}")

            records += [recordobject]

        return records

def print_records(records):
    for record in records:
        print(f"primarykey: {record.primarykey}, recordpairs: {record.recordpairs}")

if __name__ == "__main__":

    # opening a database
    handler = SQLiteHandler()
    handler.database_open(filename="science")
    handler.database_delete()
    handler.database_new(filename="science")

    # adding a table
    table_scientists = handler.database.create_table(
        name="scientists",
        column_names = ["ordering", "name", "age", "nobelprizewinner"],
        column_types = ["INTEGER", "Text", "Integer", "Bool"],
    )
    print(f"Database contains {handler.database.tables}")

    # adding multiple records
    records = []
    records += [handler.record_create(
        tablename="scientists",
        values=[1, "Hawking", 68, True],
        )]
    records += [handler.record_create(
        tablename="scientists",
        values=[2, "Edison's child said \"Apple!\"", 20, True],
        )]
    handler.table_add_records(tablename="scientists", records=records)
    print(f"creating multiple records")
    print_records(handler.table_read_records(tablename="scientists"))
    
    # adding single records
    records = []
    records += [handler.record_create(
        tablename="scientists",
        values=[3, "Einstein", 100, False],
        )]
    handler.table_add_records(tablename="scientists", records=records)
    print(f"creating single records")
    print_records(handler.table_read_records(tablename="scientists"))

    # adding multiple records
    records = []
    records += [handler.record_create(
        tablename="scientists",
        values=[4, "Rosenburg", 78, False],
        )]
    records += [handler.record_create(
        tablename="scientists",
        values=[5, "Neil dGrasse Tyson", 57, True],
        )]
    handler.table_add_records(tablename="scientists", records=records)
    print(f"creating multiple records")
    print_records(handler.table_read_records(tablename="scientists"))

    # conditional read with where statement
    where = [["nobelprizewinner", [True]]]
    records = handler.table_read_records(tablename="scientists", where=where)
    print(f"read where")
    print_records(records)

    # update with where statement
    valuepairs = [["nobelprizewinner", False]]
    where = [["nobelprizewinner", [True]], ["name", ["Hawking"]]]
    handler.table_update_records(tablename="scientists", valuepairs=valuepairs, where=where)
    records = handler.table_read_records(tablename="scientists")
    print(f"update true to false")
    print_records(records)

    valuepairs = [["name", "Neil de'Grasse Tyson"], ["age", 40]]
    rowid = 5
    handler.table_update_records(tablename="scientists", valuepairs=valuepairs, where=rowid)
    records = handler.table_read_records(tablename="scientists")
    print(f"update record 'id = 5'")
    print_records(records)

    # get records without table object, but with tablename
    records = handler.table_read_records(tablename="scientists")
    print(f"read all records")
    print_records(records)

    # adding a table
    table_nobel = handler.database.create_table(
        name = "nobelprizes",
        column_names=["ordering", "name", "description"],
        column_types=["INTEGER", "VARCHAR(255)", "TEXT"],
    )
    table_papers = handler.database.create_table(
        name = "papers",
        column_names=["ordering", "name", "description"],
        column_types=["INTEGER", "VARCHAR(255)", "TEXT"],
    )
    
    # adding multiple records in one go
    records = handler.records_create(
        tablename="nobelprizes",
        recordsvalues=[
            [1, "Peace", "Peace nobel prize"],
            [2, "Economy", "Economy nobel prize"],
            [3, "Physics", "Physics nobel prize"],
            [4, "Sociology", "Sociology nobel prize"],
            ]
        )
    handler.table_add_records(tablename="nobelprizes", records=records)
    print(f"creating multiple records")
    print_records(handler.table_read_records(tablename="nobelprizes"))

    # adding multiple records in one go
    records = handler.records_create(
        tablename="papers",
        recordsvalues=[
            [1, "Palestine", "Extrapolation on the palestinian cause"],
            [2, "Wealth", "On the Wealth of Nations"],
            [3, "Time", "A brief history of time"],
            [4, "Fear", "Controlling your fear"],
            ]
        )
    handler.table_add_records(tablename="papers", records=records)
    print(f"creating multiple records")
    print_records(handler.table_read_records(tablename="papers"))

    # adding a crossref table
    crossref_table = handler.crossref_create(
        tablename1="scientists",
        tablename2="nobelprizes",
    )
    print(f"Database contains {handler.database.tables}")

    # adding a crossref table
    crossref_table = handler.crossref_create(
        tablename1="scientists",
        tablename2="papers",
    )
    print(f"Database contains {handler.database.tables}")

    # get crossreferences
    crossreferences = handler.crossref_get_all(tablename="scientists")
    print(f"Table scientists has links to:")
    for crossreference in crossreferences:
        print(f"- {crossreference.name}")

    # adding a crossref
    handler.crossref_add_record(
        tablename1="scientists",
        tablename2="nobelprizes",
        where1=[
            ["name", ["Hawking"]]
            ],
        where2=[
            ["name", ["Economy"]]
            ],
    )

    # adding a crossref
    handler.crossref_add_record(
        tablename1="scientists",
        tablename2="nobelprizes",
        where1=[
            ["name", ["Einstein"]]
            ],
        where2=[
            ["name", ["Physics", "Peace"]]
            ],
        description="Einstein wins both peace and physics nobel prizes"
    )

    # adding crossreff based upon primary keys
    handler.crossref_add_record(
        tablename1="scientists",
        tablename2="papers",
        where1=[1],
        where2=[3, 4],
        description="Hawking wrote papers about time and fear of time"
    )

    # reading crossreferences of all scientists and nobelprizes
    records = handler.crossref_read_records(
        tablename1="scientists",
        tablename2="nobelprizes",
        )
    print_records(records)

    # reading crossreferences of a single scientist and papers
    records = handler.crossref_read_record(
        tablename1="scientists",
        tablename2="papers",
        rowid=1,
    )
    print(f"looking up Hawkings papers:")
    print_records(records)





    # gathering all records of all tables
    recordset = []
    for tablename in handler.database.tables:
        records = handler.table_read_records(tablename)
        recordset += [records]
    
    # printing all the records of all tables
    for records in recordset:
        print("")
        print_records(records)
  



    # records = reltbl.readForeignValues('charid1')

    # db.saveas_database(filename="backup")
    # db.close_database()

    # filename = "science"

    # db = Database(filename=filename)

    # teachertbl = db.create_table(
    #     name="teachers",
    #     column_names = ["ordering", "name", "age", "active"],
    #     column_types = ["INTEGER", "Text", "Integer", "Bool"],
    # )

    # db.delete_table(teachertbl)

    # table_scientists = db.get_table("scientists")

    # where = [["nobelprizewinner", [True]]]
    # records = table_scientists.readRecords(where=where)

    # table_scientists.deleteRecords(records)

    # for table in db.tables:
    #     print(f"printing for table: {table.name}")
    #     print_records(table.records)