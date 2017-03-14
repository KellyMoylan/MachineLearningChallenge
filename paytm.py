__author__ = 'Kelly Moylan'

import pandas as pd
from sklearn.cluster import KMeans
import datetime
import os.path
import sys

def read_transactions(t_file_name):
    if os.path.isfile(t_file_name):
        return pd.read_csv(t_file_name)
    else:
        raise Exception("Incorrect transaction data path")
        sys.exit(1)

def read_cancels(rc_file_name):
    if os.path.isfile(rc_file_name):
        return pd.read_csv(rc_file_name)
    else:
        raise Exception("Incorrect return/cancel data path")
        sys.exit(1)

def convert_ship_time(tdata):
    # The date-time stamps in the data are important.  To properly use them, they need to be converted into a proper
    # datetime type so they can be compared.
    try:
        return tdata.apply(lambda x: datetime.datetime.strptime(x['item_ship_by_date'], "%Y-%m-%d %H:%M:%S.%f"), axis=1)
    except:
        raise Exception("Error in data for item_ship_by_date")
        print(sys.exc_info()[0])
        sys.exit(1)

def convert_fulfil_time(tdata):
    # For any orders which were not fulfilled, the fulfillment date would be entered as a null value.  In this case, it
    # would be incorrect to mark this as being late, as something that was never sent is not late.
    try:
        return tdata.apply(lambda x: datetime.datetime.min if x['fulfillment_shipped_at'] == 'null' else datetime.datetime.strptime(x['fulfillment_shipped_at'], "%Y-%m-%d %H:%M:%S.%f"), axis=1)
    except:
        raise Exception("Error in data for fulfillment_shipped_at")
        print(sys.exc_info()[0])
        sys.exit(1)

def set_late(tdata):
    # To determine if the shipment was late, we check to see if the fulfillment shipping date is greater than the date
    # set for requirement to be shipped
    try:
        return tdata.apply((lambda x: 0 if (x['fulfillment_shipped_at'] < x['item_ship_by_date']) else 1), axis=1)
    except:
        raise Exception("Error determining lateness of shipment")
        print(sys.exc_info()[0])
        sys.exit(1)

def group_transactions(tdata):
    # The only necessary data from the transaction data is the number of shipments, and how many times it was late
    try:
        return tdata.groupby(["merchant_id"]).agg({"qty_ordered":sum, "late":sum}).reset_index()
    except:
        raise Exception("Error grouping transaction data")
        print(sys.exc_info()[0])
        sys.exit(1)

def group_cancels(rcdata):
    # The only necessary data from the return/cancel data is the number of times it happened
    try:
        return rcdata.groupby(["merchant_id"])[["cancel_num","return_num"]].sum().reset_index()
    except:
        raise Exception("Error grouping return/cancel data")
        print(sys.exc_info()[0])
        sys.exit(1)

def merge_sets(tdataGrouped, rcdataGrouped, id):
    # Merge the data together based on merchant_id to have all the needed data for clustering each merchant
    try:
        temp = tdataGrouped.merge(rcdataGrouped, on=id)
        temp.set_index(id, inplace=True)
        return temp
    except:
        raise Exception("Error merging transaction data and return/cancel data")
        print(sys.exc_info()[0])
        sys.exit(1)

def calc_bad_percentage(mergedData):
    try:
        return mergedData.apply((lambda x: (x['cancel_num'] + x['return_num']) / x['qty_ordered']), axis=1)
    except:
        raise Exception("Error calculating percentage of bad orders")
        print(sys.exc_info()[0])
        sys.exit(1)

def calc_late_percentage(mergedData):
    try:
        return mergedData.apply((lambda x: x['late'] / x['qty_ordered']), axis=1)
    except:
        raise Exception("Error calculating percentage of tale orders")
        print(sys.exc_info()[0])
        sys.exit(1)

def perform_kmeans(mergedData, clusters):
    # Perform the k-means clustering on the data.  The cluster number is based on how many rating types are wanted
    try:
        return KMeans(n_clusters=clusters).fit(mergedData)
    except:
        raise Exception("Unable to perform clustering")
        print(sys.exc_info()[0])
        sys.exit(1)

def write_file(mergedData, outputName):
     # Print out the data for analysis
    try:
        mergedData.to_csv(outputName)
    except:
        raise Exception("Unable to output file")
        print(sys.exc_info()[0])
        sys.exit(1)

if __name__ == "__main__":
    clusterNum = 5
    idMergeOn = "merchant_id"
    outputFile = sys.argv[3]

    # Data read in
    tdata = read_transactions(sys.argv[1])
    rcdata = read_cancels(sys.argv[2])

    tdata['item_ship_by_date'] = convert_ship_time(tdata)

    tdata['fulfillment_shipped_at'] = convert_fulfil_time(tdata)

    # Some data points are not required for this rating.  The item itself as well as which order it was is irrelevant,
    # as a bad order is still a bad order if it is a shirt or a computer
    tdata.drop(["T1","T2","T4","order_id","order_item_id","product_id"], inplace=True, axis=1)

    tdata['late'] = set_late(tdata)

    tdataGrouped = group_transactions(tdata)

    rcdataGrouped = group_cancels(rcdata)

    mergedData = merge_sets(tdataGrouped, rcdataGrouped, idMergeOn)

    mergedData['bad_orders_percent'] = calc_bad_percentage(mergedData)

    mergedData['late_orders_percent'] = calc_late_percentage(mergedData)

    kmeans = perform_kmeans(mergedData, clusterNum)

    # Place the cluster ID on the original data
    mergedData['labels'] = kmeans.labels_

    write_file(mergedData, outputFile)

