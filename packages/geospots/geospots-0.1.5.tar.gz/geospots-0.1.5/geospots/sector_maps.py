def query_sectors(
    engine,
    geom
):
    """ Receives a geometry and returns a Feature Collection of the ibge census sectors + geostats that intersect
    
    :param engine: valid sqlalchemy engine
    :type sqlalchemy engine

    :param geom: Geojson of a single geometry 
    :type dict or geojson """

    from geopandas import read_postgis
    import sqlalchemy
    from geospots.postgis import st_intersects, geojson_to_wkt

    geom_wkt=geojson_to_wkt(engine=engine, gjson=geom)

    cols = (
        " dev_sector_pop.cod_setor, nome_do_municipio, nome_do_bairro, pop_res_2017_est, pop_acima_10_2017_est, dom_total_2017_est, rendimento_medio_resp_2017," +
        "pop_renda_ate1sm, pop_renda_1_2sm, pop_renda_2_3sm, pop_renda_3_5sm, pop_renda_5_10sm, pop_renda_mais10sm," +
        "pop_ate_4_anos, pop_5_ate_14_anos, pop_15_ate_19_anos, pop_20_ate_29_anos, pop_30_ate_39_anos, pop_40_ate_49_anos, pop_50_ate_59_anos, " +
        "pop_60_ate_69_anos, pop_70_ate_79_anos, pop_acima_80_anos, pop_masculino, pop_feminino, alfabetizacao, geom "
    )

    statement = (
        " SELECT " + cols + 
        " FROM dev_sector_maps " +
        " LEFT JOIN dev_sector_pop " +
        " ON dev_sector_maps.cd_geocodigo=dev_sector_pop.cod_setor " +
        " WHERE " + st_intersects(geom_wkt)
    )

    geo_df = read_postgis(sql=statement, con=engine, geom_col="geom")
    geojson = geo_df.to_json()

    return(geojson)
