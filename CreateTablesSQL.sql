CREATE DATABASE country_name;
CREATE SCHEMA schema_name;
CREATE EXTENSION postgis;
CREATE EXTENSION pgrouting;

CREATE SEQUENCE schema_name.sys_substation_id_seq;
CREATE SEQUENCE schema_name.sys_feeder_id_seq;
CREATE SEQUENCE schema_name.conductor_table_id_seq;

CREATE TABLE schema_name.sys_substation
(
    id integer not null DEFAULT nextval('schema_name.sys_substation_id_seq'::regclass),,
    substation character varying(30) COLLATE pg_catalog."default",
    sub_asset_id character varying(30) COLLATE pg_catalog."default",
    sub_code character varying(5) COLLATE pg_catalog."default",
    sub_loc character varying(30) COLLATE pg_catalog."default",
    sub_serv_date date, sub_x float, sub_y float, sub_trn_num integer,
    sub_cap float,
    sub_type_cat character varying(30) COLLATE pg_catalog."default",
    sub_rem character varying(100) COLLATE pg_catalog."default",
    sub_con character varying(20) COLLATE pg_catalog."default",
    sub_lg float, sub_ll float, sub_bus_v float,
    sub_reg character varying(5) COLLATE pg_catalog."default",
    sub_min_imp float, sub_max_imp float, sub_ovr_imp float,
    sub_und_imp float,
    sub_note character varying(50) COLLATE pg_catalog."default",
    sub_lst_bld date, sub_lst_udt date
    
    constraint sys_sub_primary_key PRIMARY KEY (id)
);

CREATE TABLE schema_name.sys_feeder
(
    id integer not null DEFAULT nextval('schema_name.sys_feeder_id_seq'::regclass),
    substation character varying(30) COLLATE pg_catalog."default",
    feeder character varying(30) COLLATE pg_catalog."default",
    fed_code character varying(5) COLLATE pg_catalog."default",
    fed_length float, fed_nom_v float, fed_bus_v float, fed_flt_res float,
    fed_con character varying(20) COLLATE pg_catalog."default",
    fed_desc character varying(50) COLLATE pg_catalog."default",
    fed_rs1 float, fed_rs2 float, fed_rs3 float, fed_rst float,
    fed_sc1 float, fed_sc2 float, fed_sc3 float, fed_sct float,
    fed_lc1 float, fed_lc2 float, fed_lc3 float, fed_lct float,
    fed_si1 float, fed_si2 float, fed_si3 float, fed_sit float,
    fed_li1 float, fed_li2 float, fed_li3 float, fed_lit float,
    fed_pb1 float, fed_pb2, float, fed_pb3 float, fed_pbt float,
    fed_ag1 float, fed_ag2 float, fed_ag3 float, fed_agt float,
    fed_st1 float, fed_st2 float, fed_st3 float, fed_stt float,
    fed_rsc float, fed_scc float, fed_lcc float, fed_sic float,
    fed_lic float, fed_pbc float, fed_agc float, fed_stc float,
    fed_con1 float, fed_con2 float, fed_con3 float, fed_cont float,
    fed_kva1 float, fed_kva2 float, fed_kva3 float, fed_kvat float,
    fed_kwh1 float, fed_kwh2 float, fed_kwh3 float, fed_kwht float,
    fed_kw1 float, fed_kw2 float, fed_kw3 float, fed_kwt float,
    fed_kvar1 float, fed_kvar2 float, fed_kvar3 float, fed_kvart float,
    fed_amps1 float, fed_amps2 float, fed_amps3 float, fed_ampst float,
    fed_pf1 float, fed_pf2 float, fed_pf3 float, fed_pft float,
    fed_lst-bld float, fed_lst-udt float
    
    constraint sys_fed_primary_key PRIMARY KEY (id)
);

CREATE TABLE schema_name.conductor_table
(
    id integer not null DEFAULT nextval('schema_name.conductor_table_id_seq'::regclass),
    name character varying(30) COLLATE pg_catalog."default",
    constrntn character varying(50) COLLATE pg_catalog."default",
    strand character varying(20) COLLATE pg_catalog."default",
    dia_mm float, area_mm2 float, r_km float, gmr_m float,
    x_50_km float, x_60_km integer, max_amps float
    
    constraint cond_table_primary_key PRIMARY KEY (id)
);