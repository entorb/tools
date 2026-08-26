"""Read .fit file and print available fields."""

# see https://towardsdatascience.com/parsing-fitness-tracker-data-with-python-a59e7dc17418
import warnings

import fitdecode  # pip install fitdecode

# read all fields available in this .fit file

warnings.filterwarnings("ignore", message=".*native_field_num.*not found in message.*")

file_in = "data/231111.fit"

d_fields_lap = {}
d_fields_record = {}
with fitdecode.FitReader(file_in) as fit_file:
    for frame in fit_file:
        if isinstance(frame, fitdecode.records.FitDataMessage):
            if frame.name == "lap":
                # This frame contains data about a lap.
                for field in frame.fields:
                    # field is a FieldData object
                    if field.name not in d_fields_lap:
                        d_fields_lap[field.name] = 1
                    else:
                        d_fields_lap[field.name] += 1

            elif frame.name == "record":
                # This frame contains data about a "track point".
                for field in frame.fields:
                    if field.name not in d_fields_record:
                        d_fields_record[field.name] = 1
                    else:
                        d_fields_record[field.name] += 1

print("Laps:")
for key in sorted(d_fields_lap.keys()):
    print(key, d_fields_lap[key])


# avg_altitude 8
# avg_cadence 8
# avg_grade 8
# avg_heart_rate 8
# avg_speed 8
# avg_temperature 8
# enhanced_avg_altitude 8
# enhanced_avg_speed 8
# enhanced_max_altitude 8
# enhanced_max_speed 8
# enhanced_min_altitude 8
# event 8
# event_type 8
# max_altitude 8
# max_cadence 8
# max_heart_rate 8
# max_neg_grade 8
# max_pos_grade 8
# max_speed 8
# max_temperature 8
# min_altitude 8
# min_heart_rate 8
# start_time 8
# time_in_hr_zone 8
# timestamp 8
# total_ascent 8
# total_calories 8
# total_descent 8
# total_distance 8
# total_elapsed_time 8
# total_timer_time 8

print("Points:")
for key in sorted(d_fields_record.keys()):
    print(key, d_fields_record[key])


# altitude
# ascent
# battery_soc
# cadence
# calories
# descent
# distance
# enhanced_altitude
# enhanced_speed
# gps_accuracy
# grade
# heart_rate
# position_lat
# position_long
# speed
# temperature
# timestamp
