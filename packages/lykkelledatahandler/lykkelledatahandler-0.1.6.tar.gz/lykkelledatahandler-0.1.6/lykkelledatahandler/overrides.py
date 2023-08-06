#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Program to assign overriden values to master and close the corresponding exceptions
@author: debmishra
"""
# modules used to in Overrides
import psycopg2 as pgs
import datetime as dt


# First find out the list of open exceptions in the ticker that are eligible for a override. Also if it's stock or benchmark
# This is main __init__ function which will have the ticker, exception type, is_valid and override values as input)
class overrides:
    def __init__(self, cursor, symbol, exptyp, expfield, exptbl, ovrvalnum, ovrvaltxt, isvalid):
        ovrdate = dt.datetime.today().date()
        if 'stock' in exptbl:
            category = 'S'
            print(symbol, " symbol is a stock so stock specific exception handling are to be performed")
            # function to haandle exceptions where is valid is = True
            self.validFn(cursor, symbol, exptyp, ovrdate, expfield, exptbl, isvalid)
            self.verticalFn(cursor,symbol,exptyp,ovrvalnum,expfield,exptbl, category,isvalid)
            self.staleFn(cursor, symbol, exptyp, ovrvalnum, expfield, exptbl, category,isvalid)
            self.missingdataFn(cursor,symbol,exptyp,expfield,exptbl,ovrvalnum,ovrvaltxt,category,isvalid)
        elif 'benchmark' in exptbl:
            category = 'B'
            print(symbol, " symbol is a benchmark so benchmark specific exception handling are to be performed")
            # function to haandle exceptions where is valid is = True
            self.validFn(cursor, symbol, exptyp, ovrdate, expfield, exptbl, isvalid)
            self.verticalFn(cursor, symbol, exptyp, ovrvalnum, expfield, exptbl, category,isvalid)
            self.staleFn(cursor, symbol, exptyp, ovrvalnum, expfield, exptbl, category,isvalid)
            self.missingdataFn(cursor, symbol, exptyp, expfield, exptbl, ovrvalnum, ovrvaltxt, category,isvalid)
        else:
            print("This is not a stock or benchmark. Raise a system issue for", symbol)

    # Find out the list of entries that have is_valid=true and Push those entries
    # to ref_ignore_symsbol_list with corresponding exception types. Once done delete them rom list of exceptions.
    def validFn(self, cursor, symbol, exptyp, ovrdate, expfield, exptbl, isvalid):
        scrpt = """insert into ref_ignore_symbol_list (symbol, ignore_date, exception_type,exception_field,exception_table)
        values (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"""
        dscrpt = """update exception_master set status='closed' where symbol=%s and exception_type=%s
        and exception_field=%s and exception_table=%s"""
        if isvalid is True:
            try:
                cursor.execute(scrpt, (symbol, ovrdate, exptyp, expfield, exptbl))
                print("successful insert to ref_symbol_ignore_list for symbol-exception pair:", symbol, "-", exptyp)
                cursor.execute(dscrpt, (symbol, exptyp, expfield, exptbl))
                print("successful status update from exception_master for symbol-exception pair:", symbol, "-", exptyp)
            except pgs.Error as e:
                print(e.pgerror)
        else:
            print(symbol, " has valid exception for exception type:",
                  exptyp, "in field-table pair ", expfield, "-", exptbl, "and should be fixed via override")

    # handling overrides on vertical>10% and auto closing the exception for this ticker exception type pair
    def verticalFn(self, cursor, symbol, exptyp, ovrvalnum, expfield, exptbl, category,isvalid):
        if exptyp == 'vertical>10%' and isvalid==False:
            updfiller = 'where symbol=%s'
            if category == 'S':
                updscrpt = """update stock_master set price=%s where symbol=%s"""
                updscpth = """update stock_history set price =%s where symbol=%s and
                price_date=(select max(price_date) from stock_history sh  where symbol =%s)"""
                updscrptst = """update stock_statistics set price=%s where symbol=%s"""
            else:
                updscrpt = """update benchmark_master set price=%s where symbol=%s"""
                updscpth = """update benchmark_history set price =%s where symbol=%s and
                price_date=(select max(price_date) from benchmark_history sh  where symbol =%s)"""
            dscrpt = """update exception_master set status='closed' where symbol=%s and exception_type=%s
            and exception_field=%s and exception_table=%s and status <>'closed'"""
            try:
                if category =='S' and ovrvalnum is not None:
                    cursor.execute(updscrpt,(ovrvalnum, symbol))
                    print("vertical override sucessful insert of overriden values to price.stock_master for symbol ", symbol)
                    cursor.execute(updscpth,(ovrvalnum, symbol, symbol))
                    print("vertical override sucessful insert of overriden values to price.stock_history for symbol ", symbol)
                    cursor.execute(updscrptst,(ovrvalnum, symbol))
                    print("vertical override sucessful insert of overriden values to price.stock_statistics for symbol ", symbol)
                    cursor.execute(dscrpt, (symbol, exptyp, expfield, exptbl))
                    print("successful status update from exception_master for symbol-exception pair:", symbol, "-", exptyp)
                elif category == 'B' and ovrvalnum is not None:
                    cursor.execute(updscrpt,(ovrvalnum, symbol))
                    print("vertical override sucessful insert of overriden values to price.benchmark_master for symbol ", symbol)
                    cursor.execute(updscpth,(ovrvalnum, symbol, symbol))
                    print("vertical override sucessful insert of overriden values to price.benchmark_history for symbol ", symbol)
                    cursor.execute(dscrpt, (symbol, exptyp, expfield, exptbl))
                    print("successful status update from exception_master for symbol-exception pair:", symbol, "-",
                          exptyp)
                else:
                    print(symbol, " has no overrides yet available for handling vertical exceptions")
            except pgs.Error as e:
                print(e.pgerror)
        else:
            print(symbol, " has no vertical exception for exception type:",
                  exptyp, "in field-table pair ", expfield, "-", exptbl)

# handling the stale>=5 days and auto closing the exception for this ticker exception type pair
    def staleFn(self, cursor, symbol, exptyp, ovrvalnum, expfield, exptbl, category,isvalid):
        if exptyp == 'stale>=5days' and isvalid==False:
            updfiller = 'where symbol=%s'
            if category == 'S':
                updscrpt = """update stock_master set price=%s where symbol=%s"""
                updscpth = """update stock_history set price =%s where symbol=%s and
                price_date=(select max(price_date) from stock_history sh  where symbol =%s)"""
                updscrptst = """update stock_statistics set price=%s where symbol=%s"""
            else:
                updscrpt = """update benchmark_master set price=%s where symbol=%s"""
                updscpth = """update benchmark_history set price =%s where symbol=%s and
                price_date=(select max(price_date) from benchmark_history sh  where symbol =%s)"""
            dscrpt = """update exception_master set status='closed' where symbol=%s and exception_type=%s
            and exception_field=%s and exception_table=%s and status <>'closed'"""
            try:
                if category =='S' and ovrvalnum is not None:
                    cursor.execute(updscrpt,(ovrvalnum, symbol))
                    print("Stale override sucessful insert of overriden values to price.stock_master for symbol ", symbol)
                    cursor.execute(updscpth,(ovrvalnum, symbol, symbol))
                    print("Stale override sucessful insert of overriden values to price.stock_history for symbol ", symbol)
                    cursor.execute(updscrptst,(ovrvalnum, symbol))
                    print("Stale override sucessful insert of overriden values to price.stock_statistics for symbol ", symbol)
                    cursor.execute(dscrpt, (symbol, exptyp, expfield, exptbl))
                    print("successful status update from exception_master for symbol-exception pair:", symbol, "-", exptyp)
                elif category == 'B' and ovrvalnum is not None:
                    cursor.execute(updscrpt,(ovrvalnum, symbol))
                    print("Stale override sucessful insert of overriden values to price.benchmark_master for symbol ", symbol)
                    cursor.execute(updscpth,(ovrvalnum, symbol, symbol))
                    print("Stale override sucessful insert of overriden values to price.benchmark_history for symbol ", symbol)
                    cursor.execute(dscrpt, (symbol, exptyp, expfield, exptbl))
                    print("successful status update from exception_master for symbol-exception pair:", symbol, "-",
                          exptyp)
                else:
                    print(symbol, " has no overrides yet available for handling stale exceptions")
            except pgs.Error as e:
                print(e.pgerror)
        else:
            print(symbol, " has no stale exception for exception type:",
                  exptyp, "in field-table pair ", expfield, "-", exptbl)

# handling missing data and auto closing the exceptions for this ticker exception type pair.
    def missingdataFn(self, cursor, symbol, exptyp, expfield, exptbl, ovrvalnum, ovrvaltxt,category,isvalid):
        if exptyp =='missing value' and isvalid==False:
            if category == 'S':
                if expfield == 'price':
                    if ovrvalnum is not None:
                        updscrpt = """update stock_master set price=%s where symbol=%s"""
                        updscpth = """update stock_history set price =%s where symbol=%s and
                        price_date=(select max(price_date) from stock_history sh  where symbol =%s)"""
                        updscrptst = """update stock_statistics set price=%s where symbol=%s"""
                        dscrpt = """update exception_master set status='closed' where symbol=%s and exception_type=%s
                        and exception_field=%s and exception_table=%s and status <>'closed'"""
                        try:
                            cursor.execute(updscrpt, (ovrvalnum, symbol))
                            print( "Missing price override sucessful insert of overriden values"
                                " to price.stock_master for symbol ", symbol)
                            cursor.execute(updscpth, (ovrvalnum, symbol, symbol))
                            print( "Missing price override sucessful insert of overriden values"
                                " to price.stock_history for symbol ", symbol)
                            cursor.execute(updscrptst, (ovrvalnum, symbol))
                            print( "Missing price override sucessful insert of overriden values"
                                " to price.stock_statistics for symbol ", symbol)
                            cursor.execute(dscrpt, (symbol, exptyp, expfield, exptbl))
                            print("successful status update from exception_master for symbol-exception pair:", symbol,
                                  "-",exptyp)
                        except pgs.Error as e:
                            print(e.pgerror)
                    else:
                        print(symbol, " doesn't have stock price field's override populated to be eligble for exception handling")
                elif expfield == 'currency':
                    if ovrvaltxt is not None and len(ovrvaltxt) > 0:
                        updscrpt = """update stock_master set currency=%s where symbol=%s"""
                        updscrptst = """update stock_statistics set currency=%s where symbol=%s"""
                        dscrpt = """update exception_master set status='closed' where symbol=%s and exception_type=%s
                        and exception_field=%s and exception_table=%s and status <>'closed'"""
                        try:
                            cursor.execute(updscrpt, (ovrvaltxt, symbol))
                            print("Missing currency override sucessful insert of overriden values"
                                  " to price.stock_master for symbol ", symbol)
                            cursor.execute(updscrptst, (ovrvaltxt, symbol))
                            print("Missing currency override sucessful insert of overriden values"
                                  " to price.stock_statistics for symbol ", symbol)
                            cursor.execute(dscrpt, (symbol, exptyp, expfield, exptbl))
                            print("successful status update from exception_master for symbol-exception pair:", symbol,
                                  "-",exptyp)
                        except pgs.Error as e:
                            print(e.pgerror)
                    else:
                        print(symbol, " doesn't have stock currency field's override populated to be eligble for exception handling")
                elif expfield == 'name':
                    if ovrvaltxt is not None and len(ovrvaltxt) > 0:
                        updscrpt = """update stock_master set name=%s where symbol=%s"""
                        updscrptst = """update stock_statistics set name=%s where symbol=%s"""
                        dscrpt = """update exception_master set status='closed' where symbol=%s and exception_type=%s
                        and exception_field=%s and exception_table=%s and status <>'closed'"""
                        try:
                            cursor.execute(updscrpt, (ovrvaltxt, symbol))
                            print("Missing name override sucessful insert of overriden values"
                                  " to price.stock_master for symbol ", symbol)
                            cursor.execute(updscrptst, (ovrvaltxt, symbol))
                            print("Missing name override sucessful insert of overriden values"
                                  " to price.stock_statistics for symbol ", symbol)
                            cursor.execute(dscrpt, (symbol, exptyp, expfield, exptbl))
                            print("successful status update from exception_master for symbol-exception pair:", symbol,
                                  "-",exptyp)
                        except pgs.Error as e:
                            print(e.pgerror)
                    else:
                        print(symbol, " doesn't have stock currency field's override populated to be eligble for exception handling")
                elif expfield == 'volume':
                    if ovrvalnum is not None:
                        updscrpt = """update stock_master set volume=%s where symbol=%s"""
                        updscpth = """update stock_history set volume =%s where symbol=%s and
                        price_date=(select max(price_date) from stock_history sh  where symbol =%s)"""
                        dscrpt = """update exception_master set status='closed' where symbol=%s and exception_type=%s
                        and exception_field=%s and exception_table=%s and status <>'closed'"""
                        try:
                            cursor.execute(updscrpt, (ovrvalnum, symbol))
                            print( "Missing volume override sucessful insert of overriden values"
                                " to price.stock_master for symbol ", symbol)
                            cursor.execute(updscpth, (ovrvalnum, symbol, symbol))
                            print( "Missing volume override sucessful insert of overriden values"
                                " to price.stock_history for symbol ", symbol)
                            cursor.execute(dscrpt, (symbol, exptyp, expfield, exptbl))
                            print("successful status update from exception_master for symbol-exception pair:", symbol,
                                  "-",exptyp)
                        except pgs.Error as e:
                            print(e.pgerror)
                    else:
                        print(symbol, " doesn't have stock volume field's override populated to be eligble for exception handling")
                else:
                    if ovrvalnum is not None:
                        updscrpt = 'update '+exptbl+' set '+expfield+' = %s where symbol=%s'
                        dscrpt = """update exception_master set status='closed' where symbol=%s and exception_type=%s
                        and exception_field=%s and exception_table=%s and status <>'closed'"""
                        try:
                            cursor.execute(updscrpt, (ovrvalnum, symbol))
                            print( "Missing ",expfield ," override sucessful insert of overriden values"
                                " to ",exptbl," for symbol ", symbol)
                            cursor.execute(dscrpt, (symbol, exptyp, expfield, exptbl))
                            print("successful status update from exception_master for symbol-exception pair:", symbol,
                                  "-",exptyp)
                        except pgs.Error as e:
                            print(e.pgerror)
                    elif ovrvaltxt is not None and len(ovrvaltxt)>1:
                        updscrpt = 'update '+exptbl+' set '+expfield+' = %s where symbol=%s'
                        dscrpt = """update exception_master set status='closed' where symbol=%s and exception_type=%s
                        and exception_field=%s and exception_table=%s and status <>'closed'"""
                        try:
                            cursor.execute(updscrpt, (ovrvalnum, symbol))
                            print( "Missing ",expfield ," override sucessful insert of overriden values"
                                " to ",exptbl," for symbol ", symbol)
                            cursor.execute(dscrpt, (symbol, exptyp, expfield, exptbl))
                            print("successful status update from exception_master for symbol-exception pair:", symbol,
                                  "-",exptyp)
                        except pgs.Error as e:
                            print(e.pgerror)
                    else:
                        print(symbol, " doesn't have stock ",expfield," field's override populated to be eligble for exception handling")
            elif category == 'B':
                if expfield == 'price':
                    if ovrvalnum is not None:
                        updscrpt = """update benchmark_master set price=%s where symbol=%s"""
                        updscpth = """update benchmark_history set price =%s where symbol=%s and
                        price_date=(select max(price_date) from benchmark_history sh  where symbol =%s)"""
                        dscrpt = """update exception_master set status='closed' where symbol=%s and exception_type=%s
                        and exception_field=%s and exception_table=%s and status <>'closed'"""
                        try:
                            cursor.execute(updscrpt, (ovrvalnum, symbol))
                            print("Missing price override sucessful insert of overriden values"
                                  " to price.benchmark_master for symbol ", symbol)
                            cursor.execute(updscpth, (ovrvalnum, symbol, symbol))
                            print("Missing price override sucessful insert of overriden values"
                                  " to price.benchmark_history for symbol ", symbol)
                            cursor.execute(dscrpt, (symbol, exptyp, expfield, exptbl))
                            print("successful status update from exception_master for symbol-exception pair:", symbol,
                                  "-",exptyp)
                        except pgs.Error as e:
                            print(e.pgerror)
                    else:
                        print(symbol,
                              " doesn't have benchmark price field's override populated to be eligble for exception handling")
                elif expfield == 'name':
                    if ovrvaltxt is not None and len(ovrvaltxt) > 0:
                        updscrpt = """update benchmark_master set name=%s where symbol=%s"""
                        dscrpt = """update exception_master set status='closed' where symbol=%s and exception_type=%s
                                 and exception_field=%s and exception_table=%s and status <>'closed'"""
                        try:
                            cursor.execute(updscrpt, (ovrvaltxt, symbol))
                            print("Missing name override sucessful insert of overriden values"
                                      " to benchmark_master for symbol ", symbol)

                            cursor.execute(dscrpt, (symbol, exptyp, expfield, exptbl))
                            print("successful status update from exception_master for symbol-exception pair:",
                                      symbol,
                                      "-", exptyp)
                        except pgs.Error as e:
                            print(e.pgerror)
                    else:
                        print(symbol,
                        " doesn't have stock currency field's override populated to be eligble for exception handling")
                else:
                    if ovrvalnum is not None:
                        updscrpt = 'update '+exptbl+' set '+expfield+' = %s where symbol=%s'
                        dscrpt = """update exception_master set status='closed' where symbol=%s and exception_type=%s
                        and exception_field=%s and exception_table=%s and status <>'closed'"""
                        try:
                            cursor.execute(updscrpt, (ovrvalnum, symbol))
                            print( "Missing ",expfield ," override sucessful insert of overriden values"
                                " to ",exptbl," for symbol ", symbol)
                            cursor.execute(dscrpt, (symbol, exptyp, expfield, exptbl))
                            print("successful status update from exception_master for symbol-exception pair:", symbol,
                                  "-",exptyp)
                        except pgs.Error as e:
                            print(e.pgerror)
                    elif ovrvaltxt is not None and len(ovrvaltxt)>1:
                        updscrpt = 'update '+exptbl+' set '+expfield+' = %s where symbol=%s'
                        dscrpt = """update exception_master set status='closed' where symbol=%s and exception_type=%s
                        and exception_field=%s and exception_table=%s and status <>'closed'"""
                        try:
                            cursor.execute(updscrpt, (ovrvalnum, symbol))
                            print( "Missing ",expfield ," override sucessful insert of overriden values"
                                " to ",exptbl," for symbol ", symbol)
                            cursor.execute(dscrpt, (symbol, exptyp, expfield, exptbl))
                            print("successful status update from exception_master for symbol-exception pair:", symbol,
                                  "-",exptyp)
                        except pgs.Error as e:
                            print(e.pgerror)
                    else:
                        print(symbol, " doesn't have benchmark ",expfield," field's override populated to be eligble for exception handling")
            else:
                print("category is neither S or B for missing value overides. exiting missing value function")
        else:
            print(symbol, " has no missing value exception for exception type:",
                  exptyp, "in field-table pair ", expfield, "-", exptbl)
# Based on field update will be done on respective tables
