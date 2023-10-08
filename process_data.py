"""
    This program processes open data from IDFM to prepare it for usage
    in picorims/station-games repository.
    Copyright (C) 2023  Picorims<picorims.contact@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import pandas as pd

print("opening src: stops...")
stopsFields = ["ArRId", "ZdAId", "ArRTown", "ArRPostalRegion"]
dfStops = pd.read_csv("./src/arrets.csv", usecols=stopsFields, header=0, sep=";", on_bad_lines="warn")

print("opening src: lines...")
lineFields = ["ID_Line", "ShortName_Line", "TransportMode", "TransportSubmode", "OperatorName", "ColourWeb_hexa", "TextColourWeb_hexa"]
dfLines = pd.read_csv("./src/referentiel-des-lignes.csv", usecols=lineFields, header=0, sep=";", on_bad_lines="warn")

print("opening src: line stops...")
lineStopsFields = ["route_id", "route_long_name", "stop_id", "stop_name", "stop_lon", "stop_lat"]
dfLineStops = pd.read_csv("./src/arrets-lignes.csv", usecols=lineStopsFields, header=0, sep=";", on_bad_lines="warn")




print("Preparing fields...")

# adapt IDs in line stops
dfLineStops["route_id"] = dfLineStops["route_id"].str.replace("IDFM:", "")
dfLineStops["stop_id"] = dfLineStops["stop_id"].str.replace("IDFM:", "")

# train stop are area stops, not referential stops.
# Those IDs are mixed up in line stops and must be separated
dfLineStops["area_id"] = dfLineStops["stop_id"]
dfLineStops["stop_id"] = dfLineStops["stop_id"].replace(to_replace="^monomodalStopPlace:[0-9]*$", value="-1", regex=True)
dfLineStops["area_id"] = dfLineStops["area_id"].replace(to_replace="^[0-9]*$", value="-1", regex=True)
dfLineStops["area_id"] = dfLineStops["area_id"].str.replace("monomodalStopPlace:", "")


# convert to int
dfLineStops["stop_id"] = pd.to_numeric(dfLineStops["stop_id"], downcast="integer")
dfLineStops["area_id"] = pd.to_numeric(dfLineStops["area_id"], downcast="integer")





print("merging data...")

# print("LINES", dfLines)
# print("LINE STOPS", dfLineStops)
# print("STOPS", dfStops)

dfMerge = dfLineStops.copy()
dfMerge = pd.merge(dfMerge, dfStops, how="left", left_on="stop_id", right_on="ArRId")
# print("MERGE HERE", dfMerge)
dfMerge = pd.merge(dfMerge, dfStops, how="left", left_on="area_id", right_on="ZdAId")
# print("MERGE HERE", dfMerge)
dfMerge = pd.merge(dfMerge, dfLines, how="left", left_on="route_id", right_on="ID_Line")
# print("MERGE HERE", dfMerge)



print("sorting data...")
dfMerge = dfMerge.sort_values(by=["stop_id", "area_id"])



print("removing duplicate columns...")
# merge duplicate columns resulting from merging stops twice
duplicate_cols = ["ArRId","ZdAId","ArRTown","ArRPostalRegion"]
renamed_cols = {}
for col in duplicate_cols:
    renamed_cols[col + "_x"] = col

dfMerge = dfMerge.rename(columns=renamed_cols)

for col in duplicate_cols:
    dfMerge[col] = dfMerge[col].combine_first(dfMerge[col + "_y"])
    dfMerge = dfMerge.drop(col + "_y", axis=1)




print("removing duplicate stations...")
dfMerge = dfMerge.drop_duplicates(subset=["stop_id", "area_id", "route_id"])

print("remove duplicate id column...s")
dfMerge = dfMerge.drop(["ZdAId", "ArRId", "ID_Line"], axis=1)



print("create unique id...")
dfMerge["id"] = dfMerge[["stop_id", "area_id", "route_id"]].astype(str).apply("_".join, axis=1)



print("convert postal region to int...")
dfMerge["ArRPostalRegion"] = dfMerge["ArRPostalRegion"].astype("Int64")



print("rename columns...")
dfMerge = dfMerge.rename(columns={\
    "ArRTown": "town",\
    "ArRPostalRegion": "postal_region",\
    "ShortName_Line": "route_short_name",\
    "TransportMode": "transport_mode",\
    "TransportSubmode": "transport_submode",\
    "OperatorName": "operator_name",\
    "ColourWeb_hexa": "background_color",\
    "TextColourWeb_hexa": "text_color"\
})



print("exporting in out folder...")
dfMerge = dfMerge.set_index("id")
dfMerge.to_csv("./out/stops_data.csv")
dfMerge.to_json("./out/stops_data.json", indent=2, orient="index")



print("done.")