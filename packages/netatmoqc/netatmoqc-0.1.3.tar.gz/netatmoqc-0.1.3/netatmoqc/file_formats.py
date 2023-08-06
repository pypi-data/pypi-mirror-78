# from .load_data import epoch2datetime
from netatmoqc.load_data import epoch2datetime


def netatmo_csv_to_obsoul(fpath):
    pass


def save_df_as_obsoul(df):
    valid_data_cols = set(
        [
            #'pressure', 'mslp', 'temperature', 'humidity', 'sum_rain_1'
            "temperature",
            "humidity",
            "sum_rain_1",
        ]
    )
    df_data_cols = valid_data_cols.intersection(df.columns)
    # n_params is the same as "number of bodies" in obsoul lingo
    n_params = len(df_data_cols)

    # Construct header.
    # We should have one header for each (id, lat, lon, alt). Since we
    # forbid, in this package, that stations move (lat, lon, alt) within
    # any given DTG, we can say that we should have one header for each id.
    # Moreover, since we are also removing duplicate station IDs within any
    # given DTG, we can say we should have one header for each dataframe row.
    # Values flagged with -1 are values I still don't know
    df["time_utc"] = epoch2datetime(df["time_utc"])
    obs_type = 1  # 1: SYNOP
    obs_code = 14  # 14: Automated land synop
    obs_quality_flag = "1111"  # Got from Jelena
    site_dependent_flag = 100000  # Got from Jelena
    var2varcode = dict(
        # I got these from https://apps.ecmwf.int/odbgov/varno/
        mslp=108,  # varname="pmsl"
        pressure=110,  # varname="ps"
        temperature=39,  # varname="t2m"
        humidity=58,  # varname="rh2m". Or should I use 7 (varname=q)?
        # sum_rain_1 is prob not OK. I got it from
        # https://apps.ecmwf.int/odbgov/accumulationkind/
        sum_rain_1=39001,
    )
    with open("outfile_tmp.txt", "w") as f:
        date = df._parent_dtg.strftime("%Y%m%d")
        hour = df._parent_dtg.strftime("%H")
        f.write("{} {}\n".format(date, hour))
        for row in df.itertuples(index=False):
            header = (
                17,  # Got this from Jelena
                obs_type,
                obs_code,
                row.lat,
                row.lon,
                "'{}'".format(row.id[7:15]),
                date,
                hour,
                row.alt,
                n_params,
                obs_quality_flag,
                site_dependent_flag,
            )

            f.write(" ".join(map(str, header)) + "\n")
            # Construct bodies
            # Values flagged with -1 are values I still don't know
            for param_name in df_data_cols:
                # param_type is the same as "varid@body" in odb lingo
                # See http://www.rclace.eu/File/Data_Assimilation/2007/lace_obspp.pdf:
                # for some explanation on the vertical coordinate conventions for
                # various obs types. In particular, that document states that, for
                # synop and ship, MSLP should, if available, be used as vertical coord
                # instead of pressure, but the MSLP value should be multiplied by -1
                param_type = var2varcode[param_name]
                param_quality_flag = "ne"  # Got from Jelena
                try:
                    first_vert_coord = row.pressure
                except (AttributeError):
                    first_vert_coord = -row.mslp
                # Got the sentinel value 1.7000000000000000E+038 from CARRA OBSOULs
                second_vert_coord = 1.7e038
                body = (
                    param_type,
                    first_vert_coord,
                    second_vert_coord,
                    getattr(row, param_name),
                    param_quality_flag,
                )
                f.write(" ".join(map(str, body)) + "\n")
        print("")


if __name__ == "__main__":
    from netatmoqc.config_parser import ParsedConfig, UndefinedConfigValue
    from netatmoqc.load_data import read_netatmo_data_for_dtg

    config = ParsedConfig(global_default=UndefinedConfigValue)
    df = read_netatmo_data_for_dtg(
        config.dtgs[0], recover_pressure_from_mslp=True, drop_mslp=True
    )
    save_df_as_obsoul(df)
