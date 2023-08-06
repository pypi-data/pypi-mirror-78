## Function to translate geometries for postgis

def geojson_to_wkt(engine, gjson):
    """ This function converts a geojson to wkt format using postgis 
    """

    # Build statement
    clean_gjson = str(gjson).replace("'", '"')
    statement="SELECT ST_AsText(ST_GeomFromGeoJSON('" + clean_gjson + "'))"

    con=engine.connect()

    result_proxy=con.execute(statement)
    result_set=result_proxy.fetchall()

    output=result_set[0][0]

    return(output)


def st_make_envelope(bbox):
    # list in the format of xmin, ymin, xmax, ymax where x=lon and y=lat

    bbox_str = [str(x) for x in bbox]

    pgis_bbox = "ST_MakeEnvelope(" + ",".join(bbox_str) + ", 4326)"

    return(pgis_bbox)


def st_intersects(
    geom,
    table="dev_sector_maps",
    geom_col="geom"
):
    """ 
        Builds the intersection condition for the given geometry (in wkt or wkb format) with the geometry column 
    """

    geo_col = table + "." + geom_col

    pgis_intersects = "ST_Intersects(" + geo_col + ", '" + geom + "')"

    return(pgis_intersects)

