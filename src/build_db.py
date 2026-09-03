
import pandas as pd

def normalize_modern(df):
    #Convert started_at and ended_at to real datetimes
    #Then compute duration_sec from their difference
    #Select just the unified columns and return that as the result
    df = df.copy()

    started = pd.to_datetime(df['started_at'])
    ended = pd.to_datetime(df['ended_at'])
    seconds = (ended - started).dt.total_seconds()
    print(seconds)
    df['duration_sec'] = seconds.astype('int64')
    print(df['duration_sec'])
    return df[['ride_id', 'rideable_type', 'started_at', 'ended_at', 'duration_sec',
       'start_station_name', 'start_station_id', 'end_station_name',
       'end_station_id', 'start_lat', 'start_lng', 'end_lat', 'end_lng',
       'member_casual']]

def normalize_legacy(df):
    df = df.copy()

    # rename columns
        # start_time → started_at
        # end_time → ended_at
        # start_station_latitude → start_lat
        # start_station_longitude → start_lng
        # end_station_latitude → end_lat
        # end_station_longitude → end_lng
    df = df.rename(columns={
        "start_time": "started_at",
        "end_time": "ended_at",
        "start_station_latitude": "start_lat",
        "start_station_longitude": "start_lng",
        "end_station_latitude": "end_lat",
        "end_station_longitude": "end_lng"
        })

    # add two columns don't exist at all in legacy files
        # rideable_type gets filled with the constant "classic_bike" (no e-bikes yet in this era)
        # ride_id gets filled with null for every row (legacy trips never had one)
    df['rideable_type'] = "classic_bike"
    df["ride_id"] = None

    # rename AND value translation
        # user_type becomes member_casual
            # Subscriber → Member
            # Customer → Casual
    df = df.rename(columns={"user_type": "member_casual"})
    df['member_casual'] = df['member_casual'].map({'Subscriber': 'member', 'Customer': 'casual'})

    # two (possibly three, if in a transitional file) columns get dropped entirely
        # bike_id, bike_share_for_all_trip, and rental_access_method
    #return dataframe with the 14 unified columns
    return df[['ride_id', 'rideable_type', 'started_at', 'ended_at', 'duration_sec',
           'start_station_name', 'start_station_id', 'end_station_name',
           'end_station_id', 'start_lat', 'start_lng', 'end_lat', 'end_lng',
           'member_casual']]
