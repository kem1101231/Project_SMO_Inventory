--
-- PostgreSQL database dump
--

-- Dumped from database version 9.4.11
-- Dumped by pg_dump version 9.4.11
-- Started on 2017-06-24 06:42:34

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 1 (class 3079 OID 11855)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2351 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 208 (class 1259 OID 16743)
-- Name: abstract_of_canvass; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE abstract_of_canvass (
    canvassnum character varying(50) NOT NULL,
    bidnum character varying(50),
    dateofquotation date,
    dateopen date,
    recomendation text,
    sel_approval boolean
);


ALTER TABLE abstract_of_canvass OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 16751)
-- Name: abstract_of_canvass_items; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE abstract_of_canvass_items (
    canvassnum character varying(15),
    itemnum integer,
    description character varying(250),
    unit character varying(150),
    quantity double precision
);


ALTER TABLE abstract_of_canvass_items OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 16754)
-- Name: abstract_of_canvass_supplier_price; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE abstract_of_canvass_supplier_price (
    canvassnum character varying(50),
    supplier character varying(150),
    itemnum integer,
    unitprice double precision,
    sel_approval boolean,
    reason character varying(250),
    bid_item_descrip character varying(250)
);


ALTER TABLE abstract_of_canvass_supplier_price OWNER TO postgres;

--
-- TOC entry 173 (class 1259 OID 16409)
-- Name: account_items; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE account_items (
);


ALTER TABLE account_items OWNER TO postgres;

--
-- TOC entry 174 (class 1259 OID 16412)
-- Name: accounts; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE accounts (
);


ALTER TABLE accounts OWNER TO postgres;

--
-- TOC entry 175 (class 1259 OID 16415)
-- Name: asset; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE asset (
    asset_id character varying(10) NOT NULL,
    itemid character varying(15),
    description character varying(250),
    brand character varying(150),
    type character varying(80),
    class character varying(80),
    unit character varying(50),
    unit_price double precision,
    date_of_update date
);


ALTER TABLE asset OWNER TO postgres;

--
-- TOC entry 176 (class 1259 OID 16421)
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE auth_group OWNER TO postgres;

--
-- TOC entry 177 (class 1259 OID 16424)
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_group_id_seq OWNER TO postgres;

--
-- TOC entry 2352 (class 0 OID 0)
-- Dependencies: 177
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- TOC entry 178 (class 1259 OID 16426)
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE auth_group_permissions OWNER TO postgres;

--
-- TOC entry 179 (class 1259 OID 16429)
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_group_permissions_id_seq OWNER TO postgres;

--
-- TOC entry 2353 (class 0 OID 0)
-- Dependencies: 179
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- TOC entry 180 (class 1259 OID 16431)
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE auth_permission OWNER TO postgres;

--
-- TOC entry 181 (class 1259 OID 16434)
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_permission_id_seq OWNER TO postgres;

--
-- TOC entry 2354 (class 0 OID 0)
-- Dependencies: 181
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- TOC entry 182 (class 1259 OID 16436)
-- Name: auth_user; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE auth_user OWNER TO postgres;

--
-- TOC entry 183 (class 1259 OID 16442)
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE auth_user_groups OWNER TO postgres;

--
-- TOC entry 184 (class 1259 OID 16445)
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_groups_id_seq OWNER TO postgres;

--
-- TOC entry 2355 (class 0 OID 0)
-- Dependencies: 184
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- TOC entry 185 (class 1259 OID 16447)
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_id_seq OWNER TO postgres;

--
-- TOC entry 2356 (class 0 OID 0)
-- Dependencies: 185
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- TOC entry 186 (class 1259 OID 16449)
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE auth_user_user_permissions OWNER TO postgres;

--
-- TOC entry 187 (class 1259 OID 16452)
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_user_permissions_id_seq OWNER TO postgres;

--
-- TOC entry 2357 (class 0 OID 0)
-- Dependencies: 187
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- TOC entry 188 (class 1259 OID 16454)
-- Name: college; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE college (
    id character varying(10) NOT NULL,
    name character varying(255)
);


ALTER TABLE college OWNER TO postgres;

--
-- TOC entry 189 (class 1259 OID 16457)
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE django_admin_log OWNER TO postgres;

--
-- TOC entry 190 (class 1259 OID 16464)
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_admin_log_id_seq OWNER TO postgres;

--
-- TOC entry 2358 (class 0 OID 0)
-- Dependencies: 190
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- TOC entry 191 (class 1259 OID 16466)
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE django_content_type OWNER TO postgres;

--
-- TOC entry 192 (class 1259 OID 16469)
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_content_type_id_seq OWNER TO postgres;

--
-- TOC entry 2359 (class 0 OID 0)
-- Dependencies: 192
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- TOC entry 193 (class 1259 OID 16471)
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE django_migrations OWNER TO postgres;

--
-- TOC entry 194 (class 1259 OID 16477)
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_migrations_id_seq OWNER TO postgres;

--
-- TOC entry 2360 (class 0 OID 0)
-- Dependencies: 194
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- TOC entry 195 (class 1259 OID 16479)
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE django_session OWNER TO postgres;

--
-- TOC entry 196 (class 1259 OID 16485)
-- Name: employees; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE employees (
    idnum character varying(15) NOT NULL,
    fname character varying(100),
    sname character varying(100),
    designation character varying(100),
    dept character varying(50),
    rank character varying(25),
    title character varying(25),
    mname character(100)
);


ALTER TABLE employees OWNER TO postgres;

--
-- TOC entry 197 (class 1259 OID 16491)
-- Name: equip_particulars; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE equip_particulars (
    idname character varying(15) NOT NULL,
    name character varying(255),
    subhead character varying(15),
    itemnum character varying(10)
);


ALTER TABLE equip_particulars OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 16766)
-- Name: iar_items; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE iar_items (
    iarnum character varying(15),
    stocknum integer,
    unit character varying(50),
    description character varying(255),
    quantity double precision,
    compstat boolean,
    compdate date,
    workstat boolean,
    workdate date,
    compstatmiss double precision,
    workstatmiss double precision
);


ALTER TABLE iar_items OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 16777)
-- Name: insp_and_accept_report; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE insp_and_accept_report (
    iarnum character varying(15) NOT NULL,
    ponum character varying(15),
    reqoff character varying(180),
    podate date,
    recieptnum character varying(150),
    recieptdate date,
    insstatus boolean,
    insdate date,
    insofficer character varying(255),
    isitemcomplete boolean,
    receivedate date,
    receiveofficer character varying(255),
    counter integer
);


ALTER TABLE insp_and_accept_report OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 16834)
-- Name: inventory; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE inventory (
    invnum integer NOT NULL,
    parnum character varying(25) NOT NULL,
    description character varying(255),
    unit character varying(50),
    unitprice double precision,
    quantity double precision,
    status boolean
);


ALTER TABLE inventory OWNER TO postgres;

--
-- TOC entry 198 (class 1259 OID 16506)
-- Name: items; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE items (
    itemid character varying(10) NOT NULL,
    description character varying(255),
    type character varying(15),
    class character varying(15),
    unit character varying(10),
    price double precision
);


ALTER TABLE items OWNER TO postgres;

--
-- TOC entry 2361 (class 0 OID 0)
-- Dependencies: 198
-- Name: COLUMN items.price; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN items.price IS '
';


--
-- TOC entry 199 (class 1259 OID 16509)
-- Name: keypositions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE keypositions (
    id character varying(10) NOT NULL,
    empid character varying(15)
);


ALTER TABLE keypositions OWNER TO postgres;

--
-- TOC entry 213 (class 1259 OID 16790)
-- Name: log; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE log (
    logid character varying(15) NOT NULL,
    idnum character varying(15),
    accttype integer,
    datetimeloggoed date
);


ALTER TABLE log OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 16795)
-- Name: notifications; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE notifications (
    notifnum character varying(15) NOT NULL,
    fromid character varying(15),
    toid character varying(15),
    status boolean,
    priority integer,
    notifref character varying(30),
    details character varying(100)[],
    dateofnotif date,
    timeofnotif time without time zone,
    type integer,
    reftype character varying(25)
);


ALTER TABLE notifications OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 16521)
-- Name: offices; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE offices (
    id character varying(25) NOT NULL,
    name character varying(255),
    type character varying(25),
    head character varying(25),
    authopersonel character varying(25),
    division character varying(25)
);


ALTER TABLE offices OWNER TO postgres;

--
-- TOC entry 201 (class 1259 OID 16524)
-- Name: physical_count; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE physical_count (
);


ALTER TABLE physical_count OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16823)
-- Name: property_acc_receipt; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE property_acc_receipt (
    parnum character varying(15) NOT NULL,
    dateofpar date,
    receiveby character varying(25),
    datereceiveby date,
    receivefrom character varying(25),
    datereceivefrom date,
    ponum character varying(15),
    counter integer
);


ALTER TABLE property_acc_receipt OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16839)
-- Name: purchase_order; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE purchase_order (
    ponum character varying(50) NOT NULL,
    supplier character varying(255),
    datecreated date,
    procmode character varying(150),
    dateofdelivery date,
    placeofdelivery character varying(250),
    deliveryterm character varying(25),
    paymentterm character varying(25),
    amount double precision,
    status boolean,
    deliverystatus boolean,
    paymentstatus boolean,
    conforme character varying(255),
    prref character varying(15),
    counter integer,
    fundref character varying,
    approval_date date,
    serve_date date
);


ALTER TABLE purchase_order OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16847)
-- Name: purchase_order_items; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE purchase_order_items (
    ponum character varying(50),
    itemnum integer,
    quantity double precision,
    unit character varying(50),
    description character varying(150),
    unitcost double precision
);


ALTER TABLE purchase_order_items OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16850)
-- Name: purchase_request; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE purchase_request (
    reqnum character varying(25) NOT NULL,
    prnum character varying(50),
    purpose character varying(250),
    purpose_details text,
    requester_id character varying(15),
    date_created date,
    status boolean,
    init_approval_status boolean,
    approval_status boolean,
    declinereason text,
    counter integer,
    approval_staus_date date
);


ALTER TABLE purchase_request OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16867)
-- Name: purchase_request_items; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE purchase_request_items (
    reqnum character varying(10),
    stock_num character varying(25),
    description character varying(250),
    unit character varying(50),
    unit_price double precision,
    quantity double precision
);


ALTER TABLE purchase_request_items OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16870)
-- Name: received_items; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE received_items (
    iarnum character varying(15),
    availability boolean,
    description character varying(255),
    quantity double precision,
    price double precision,
    itemnum integer
);


ALTER TABLE received_items OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 16551)
-- Name: received_items_list; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE received_items_list (
);


ALTER TABLE received_items_list OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16912)
-- Name: req_for_quotation; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE req_for_quotation (
    quotationnum character varying(15) NOT NULL,
    refnum character varying(50),
    projname character varying(255),
    projlocation character varying(255),
    datecreated date,
    canvasser character varying(150),
    counter integer
);


ALTER TABLE req_for_quotation OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16925)
-- Name: req_for_quotation_items; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE req_for_quotation_items (
    quotationnum character varying(25),
    itemnum integer,
    description character varying(250),
    quantity double precision,
    unit character varying(50),
    unitprice double precision
);


ALTER TABLE req_for_quotation_items OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 16937)
-- Name: req_for_quotation_suppliers; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE req_for_quotation_suppliers (
    quotationnum character varying(15),
    compid character varying(15),
    warrantyper double precision,
    delperiod double precision,
    pricevalidity double precision
);


ALTER TABLE req_for_quotation_suppliers OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 16566)
-- Name: suppliers; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE suppliers (
    compid character varying(25) NOT NULL,
    name character varying(255),
    address character varying(250),
    comprep character varying(250),
    reptel character varying(50),
    repemail character varying(50),
    comptin character varying(50),
    dateadded date,
    rating integer,
    ratingupdate date
);


ALTER TABLE suppliers OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 16572)
-- Name: test; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE test (
    dr date,
    re boolean
);


ALTER TABLE test OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 16575)
-- Name: transactions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE transactions (
);


ALTER TABLE transactions OWNER TO postgres;

--
-- TOC entry 206 (class 1259 OID 16578)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE users (
    uname character varying(25) NOT NULL,
    pass character varying(50),
    idnum character varying(15),
    access_type integer[],
    profile_pic bytea,
    status boolean
);


ALTER TABLE users OWNER TO postgres;

--
-- TOC entry 207 (class 1259 OID 16584)
-- Name: waste_mat_report; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE waste_mat_report (
);


ALTER TABLE waste_mat_report OWNER TO postgres;

--
-- TOC entry 2080 (class 2604 OID 16587)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- TOC entry 2081 (class 2604 OID 16588)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- TOC entry 2082 (class 2604 OID 16589)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- TOC entry 2083 (class 2604 OID 16590)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- TOC entry 2084 (class 2604 OID 16591)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- TOC entry 2085 (class 2604 OID 16592)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- TOC entry 2086 (class 2604 OID 16593)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- TOC entry 2088 (class 2604 OID 16594)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- TOC entry 2089 (class 2604 OID 16595)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- TOC entry 2327 (class 0 OID 16743)
-- Dependencies: 208
-- Data for Name: abstract_of_canvass; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY abstract_of_canvass (canvassnum, bidnum, dateofquotation, dateopen, recomendation, sel_approval) FROM stdin;
\.


--
-- TOC entry 2328 (class 0 OID 16751)
-- Dependencies: 209
-- Data for Name: abstract_of_canvass_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY abstract_of_canvass_items (canvassnum, itemnum, description, unit, quantity) FROM stdin;
\.


--
-- TOC entry 2329 (class 0 OID 16754)
-- Dependencies: 210
-- Data for Name: abstract_of_canvass_supplier_price; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY abstract_of_canvass_supplier_price (canvassnum, supplier, itemnum, unitprice, sel_approval, reason, bid_item_descrip) FROM stdin;
\.


--
-- TOC entry 2292 (class 0 OID 16409)
-- Dependencies: 173
-- Data for Name: account_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY account_items  FROM stdin;
\.


--
-- TOC entry 2293 (class 0 OID 16412)
-- Dependencies: 174
-- Data for Name: accounts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY accounts  FROM stdin;
\.


--
-- TOC entry 2294 (class 0 OID 16415)
-- Dependencies: 175
-- Data for Name: asset; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY asset (asset_id, itemid, description, brand, type, class, unit, unit_price, date_of_update) FROM stdin;
BoiT-2104	ErTY-3211	\N	Epson	\N	it	Unit	\N	2017-02-01
dRtE-6985	XcTp-6954	\N	HP	\N	it	Piece	\N	2017-02-01
LWed-5613	XcTp-6954	\N	AOC	\N	it	Piece	\N	2017-02-01
QlFr-6214	ErTY-3211	\N	Canon	\N	it	Unit	\N	2017-02-01
ades-8621	OprG-5214	Aspire	Acer	\N	it	Unit	\N	2017-02-01
EtfD-3652	OprG-5214	iMac	Apple	\N	it	Unit	\N	2017-02-01
IORt-8541	OprG-5214	Pavillon	HP	\N	it	Unit	45000	2017-02-01
\.


--
-- TOC entry 2295 (class 0 OID 16421)
-- Dependencies: 176
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_group (id, name) FROM stdin;
\.


--
-- TOC entry 2362 (class 0 OID 0)
-- Dependencies: 177
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_group_id_seq', 1, false);


--
-- TOC entry 2297 (class 0 OID 16426)
-- Dependencies: 178
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- TOC entry 2363 (class 0 OID 0)
-- Dependencies: 179
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 1, false);


--
-- TOC entry 2299 (class 0 OID 16431)
-- Dependencies: 180
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can add group	2	add_group
5	Can change group	2	change_group
6	Can delete group	2	delete_group
7	Can add user	3	add_user
8	Can change user	3	change_user
9	Can delete user	3	delete_user
10	Can add permission	4	add_permission
11	Can change permission	4	change_permission
12	Can delete permission	4	delete_permission
13	Can add content type	5	add_contenttype
14	Can change content type	5	change_contenttype
15	Can delete content type	5	delete_contenttype
16	Can add session	6	add_session
17	Can change session	6	change_session
18	Can delete session	6	delete_session
\.


--
-- TOC entry 2364 (class 0 OID 0)
-- Dependencies: 181
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_permission_id_seq', 18, true);


--
-- TOC entry 2301 (class 0 OID 16436)
-- Dependencies: 182
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
\.


--
-- TOC entry 2302 (class 0 OID 16442)
-- Dependencies: 183
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- TOC entry 2365 (class 0 OID 0)
-- Dependencies: 184
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 1, false);


--
-- TOC entry 2366 (class 0 OID 0)
-- Dependencies: 185
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_user_id_seq', 1, false);


--
-- TOC entry 2305 (class 0 OID 16449)
-- Dependencies: 186
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- TOC entry 2367 (class 0 OID 0)
-- Dependencies: 187
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);


--
-- TOC entry 2307 (class 0 OID 16454)
-- Dependencies: 188
-- Data for Name: college; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY college (id, name) FROM stdin;
\.


--
-- TOC entry 2308 (class 0 OID 16457)
-- Dependencies: 189
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- TOC entry 2368 (class 0 OID 0)
-- Dependencies: 190
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 1, false);


--
-- TOC entry 2310 (class 0 OID 16466)
-- Dependencies: 191
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	group
3	auth	user
4	auth	permission
5	contenttypes	contenttype
6	sessions	session
\.


--
-- TOC entry 2369 (class 0 OID 0)
-- Dependencies: 192
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('django_content_type_id_seq', 6, true);


--
-- TOC entry 2312 (class 0 OID 16471)
-- Dependencies: 193
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2017-02-14 00:07:11.295832+00
2	auth	0001_initial	2017-02-14 00:07:12.139732+00
3	admin	0001_initial	2017-02-14 00:07:12.342885+00
4	admin	0002_logentry_remove_auto_add	2017-02-14 00:07:12.389753+00
5	contenttypes	0002_remove_content_type_name	2017-02-14 00:07:12.483477+00
6	auth	0002_alter_permission_name_max_length	2017-02-14 00:07:12.530357+00
7	auth	0003_alter_user_email_max_length	2017-02-14 00:07:12.577252+00
8	auth	0004_alter_user_username_opts	2017-02-14 00:07:12.717855+00
9	auth	0005_alter_user_last_login_null	2017-02-14 00:07:12.764765+00
10	auth	0006_require_contenttypes_0002	2017-02-14 00:07:12.780382+00
11	auth	0007_alter_validators_add_error_messages	2017-02-14 00:07:12.811635+00
12	auth	0008_alter_user_username_max_length	2017-02-14 00:07:12.889983+00
13	sessions	0001_initial	2017-02-14 00:07:13.032179+00
\.


--
-- TOC entry 2370 (class 0 OID 0)
-- Dependencies: 194
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('django_migrations_id_seq', 13, true);


--
-- TOC entry 2314 (class 0 OID 16479)
-- Dependencies: 195
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
p1qz2h0m6aj5nygvayn8eur29rslsunf	NjNkNGIxMzIwMjY2MTZmYWQ0Njc1N2VlMmQ3YjYwZTE2NjJlOTBmNTp7InRoZU9mZklEIjoiQmlvIiwicHJDb29raWUiOiJYR2trLTYxNzAiLCJ0aGVDb29raWUiOiJxTEJrLTUxMTkiLCJ0aGVEZXB0SUQiOiJDTlNNIn0=	2017-03-03 00:38:34.926058+00
h9pooz81myhw6zc7tutq8tx2o791219a	NTVmYWM1YzYzNjc1NGY3NGQyNzk5Mjg2NjllNDYxNjNlOTRhOGFhYzp7InRoZUNvb2tpZSI6ImxBUHQtMzQ0MiJ9	2017-03-02 00:46:02.237025+00
5jix1dscvy01d2yq9d4eynm7kikcegj7	ZDU4M2VlYjQ3NzRkZjQwYWZiOWJkMDBlMjFlNTUyNjk4ZjcwZWQ4ZDp7InRoZUNvb2tpZSI6IkdWa28tMzI1NCJ9	2017-03-29 15:49:33.098226+01
bbllexbvle5284po5rvibmtjwlnu7n56	NjQwOTRjNGE2YjljYzQwZDMyZWU1Zjc5YWRiMTNmNDMyYjgzNDkzMzp7InByQ29va2llIjoiRk5say0zMjgyIiwidGhlQ29va2llIjoiQ01JTS05NTg5In0=	2017-03-30 10:18:08.01337+01
vlxpux0wyg8g5ys36e4w6adsf93jjqcu	MjE0MmZlY2EzMWI4OGMxMTFkMGRkNjM4NWY4NjFkZGUyNzg3MTU4MTp7InRoZUNvb2tpZSI6IkFEQUUtNjI0NyJ9	2017-11-01 09:20:43.377626+00
5y7sg6hrzze80da1q1rl1wlbqwfvir4d	Y2NlY2M4ZTMzYTc0MTAzYmY1ZTNjNTExNWYyNjRkNDViMTU1NWE5OTp7InRoZU9mZklEIjoiSVQtUGh5c2ljcyIsInRoZUNvb2tpZSI6IkFJaVUtNDk2MiIsInByQ29va2llIjoiVHpTTS02Nzc1IiwidGhlRGVwdElEIjoiQ05TTSJ9	2017-03-30 04:15:07.226095+01
aj9rd1psp52zzh62orcusulxsgs0s1wf	MDVkYjI2NTY5YWUyZWFiNjU4ZDJiZGNjMDM4YjNiNjc2MzEwMTg2NTp7InRoZUNvb2tpZSI6ImJsTkItNzIzMyJ9	2017-03-23 15:15:17.928942+00
i8ofq605yva46gjthxznazia7y9sfxyo	MzdmNDM3NGQyYTQ3Y2Q5MGFkMTg5YjAxYzkyYzljMmQ5YTIzMDFmOTp7InRoZUNvb2tpZSI6InFiZFYtOTI5MyJ9	2017-03-30 15:01:57.69636+01
ofllw9xikx4slbr7mt5tppwt82lxx1ow	YTdiNTRiM2RhZThhNzdmZWRmMDBkNzc1YTFlMjNhNDAzNjI1YzQ5NTp7InByQ29va2llIjoiRk5say0zMjgyIiwidGhlQ29va2llIjoiUnZWci04NTMxIiwicGFyQ29va2llIjoiMDAxLTE3In0=	2017-03-30 15:11:40.380788+01
24hug7ywspwrws3sktg67bd432gaxeqs	ZDI0ZDVmYTBiNDRiNjU2NzY5MmRkM2U4NTBjYjU0MDFlZDZmOTAxNDp7InRoZUNvb2tpZSI6ImdhUHotNjkwNiIsInByQ29va2llIjoiRkZLTS01MjEyIn0=	2017-05-04 08:57:17.535169+01
b77vw7rvm74kx3o3bh34yyknol1x4tp1	NjY5Mjk1NjNhYTZhMmRmOGNhNjViOWIzNGQxOTcxNTc4ZDlmZDRkYTp7InRoZUNvb2tpZSI6IlR3eHEtNzk4OSIsInBhckNvb2tpZSI6IjAwMS0xNyJ9	2017-04-25 09:26:39.109848+01
rfn5qkgepmhxz0ic9kl5qe99jebqyun5	MTFlNmFjOGY2Y2QzN2MwOWYzZjIyZjhiODAxYjk0NjZkNmMxYzM0OTp7InRoZUNvb2tpZSI6ImZoaGQtODU0NSJ9	2017-04-24 18:27:27.633869+01
k6sja166rh3jrptfx8uxz5nem280x9bo	ZmJiZGJlOGQ4Yzc3MjNiYmUxNjc1OWEzNmY1ODc4YThiZmNkOGI2Nzp7InRoZUNvb2tpZSI6IlptQXotODU3NiIsInByQ29va2llIjoicFlJTC00MDEzIn0=	2017-04-25 12:17:44.170062+01
q8b7h6f00ahnwso1jtvndl7hzp2m6ums	MzNlNjIyOWUwYTI4ZjcyNTk0OTQ4MjA0ZDMzZTI4M2Q0ZDcyYmVjMTp7InRoZUNvb2tpZSI6IkhGZXUtOTg4MyJ9	2017-05-01 02:37:00.203685+01
0z2xh750v9zyhm7ds584hicw4ra9in7l	ODE3OTE4M2RmMTA1YjgzMmQ2NGNkMTNlNGU3YzY4MzFkMjk0MDUzMjp7InByQ29va2llIjoiRkZLTS01MjEyIiwidGhlQ29va2llIjoiQkVUVC0zMDMyIn0=	2017-05-04 09:56:18.525727+01
sqqs54bl8ew8led7u5o84mqpm9z3rz8z	ZDgxM2M1YTJhMDMwYTQ5MDNiZGJjMjcwNGU2NzI1OTU4YjgxZTI4Njp7InRoZUNvb2tpZSI6IndnaEgtODE4NiJ9	2017-05-01 11:17:38.22889+01
if0i3y4etbarv0ktj80pqp647a4b2w9g	ZWQ3MTY3MDQ5MGRmYTQ3YTYxZjUzOGQ4MjIxOTliNzdhZGRkNmQxYjp7InRoZUNvb2tpZSI6IndHY0ctOTIyNSJ9	2017-04-27 23:08:26.070813+01
27labrr486meuh98h74w25a29yaxqsuv	MGU5NTRjMzdlYmIzZTM4YTc2ZDE4ZjAwZWI1NDVjNzE3MjAxMTc2Njp7InByQ29va2llIjoiMDA2LTE3IiwidGhlQ29va2llIjoia1VYdC00MTM3In0=	2017-05-05 09:08:15.10937+01
rtwhxbn6kllrrjrvrx1h5qrsjbqhpqb0	YzFlMTg2YmQ2MzBhZjQ0NWM5MzUyYmE3ZGRiYWYzODNiZjYyYTc4MDp7InRoZUNvb2tpZSI6ImxKY3MtMjUzOCIsInByQ29va2llIjoiRk5say0zMjgyIiwicGFyQ29va2llIjoiMDAxLTE3In0=	2017-04-24 12:37:35.240709+01
xm8zt45jfme3506fctf4i6hds6opet7f	NjBjNDEyYjI3YWYyZGU1MDE3M2Y4OGYwMTkwNzNiNTQzODI4MmJjZTp7InByQ29va2llIjoiRkZLTS01MjEyIiwidGhlQ29va2llIjoiS2RNVC02NTU3In0=	2017-05-07 18:19:37.471278+01
tqa1pz2tjr4wp6vbkffjqn6mwkj85g49	NzgwNzU2MjUyNWI1NWI0YzMyYzI0ZWJjOGUyYTI5NzAwNzNmNzNkODp7InRoZUNvb2tpZSI6IlB6eUMtODg3NCJ9	2017-05-08 04:49:25.41685+01
cyu9e6ccuxiggj26pguul0szvhqc3cyf	NjI5YzhmMmI4MmY0YWU0NTg2ZGQ3ZDY4N2E3Y2VkMTdlNzk5MjIzMTp7InRoZUNvb2tpZSI6InRqRkstMTYzMyJ9	2017-05-09 20:40:03.73514+01
m5k24gbkzdycfyix2eokhk34cnjmvfim	ODk3OTkwYTAxODk5ODMzY2E4MGU0MjVhNmQyNTk5YzZmMmVhYWMyNTp7fQ==	2017-05-03 06:19:44.071225+01
7xab1jbj4jap8tp25gdrt2yu489bzioj	NmI3ODY5ZTNkYmNjNDEyZTYzODJlMTc2M2Q1NjRmNGFjMGI5NGI3Nzp7InRoZUNvb2tpZSI6Im9xblAtNTg0NCIsInByQ29va2llIjoiTlVqeC0wMDgxIn0=	2017-05-10 01:52:34.687143+01
qcjwcdjygrzi87c9yj29bjgth0ix5uwh	YmQ0YjI4MTU0OTAyYTY4NTUzYzE5OGI5YTBjMGU2NDdkMTlmMTQ5ZTp7InRoZUNvb2tpZSI6ImtiZm8tNzg0NiJ9	2017-05-30 14:57:40.904349+01
uzl07eowqpplmopx73o3ve57p1jwb0zc	ODk3OTkwYTAxODk5ODMzY2E4MGU0MjVhNmQyNTk5YzZmMmVhYWMyNTp7fQ==	2017-05-23 10:55:41.936731+01
vl1ichon9olla4gng8tpfmgqul6svidh	N2ViODdhZGEwODFjZDVlOTBiYzdjMWVlMTI2MDRkNzIyNDgxODE5Njp7InRoZUNvb2tpZSI6IkZDZEktNDAwNSJ9	2017-05-25 08:17:25.320723+01
9dewbdx28et62bhvr6uc2rdnehafyo0f	YWExYjNjMGZiZWY0Mzg4MGEwNWI0ODIwNTc1MDU2ZDVjM2MwNjM3NDp7InRoZUNvb2tpZSI6ImtLSXUtNjMyOCIsInByQ29va2llIjoiemhwci0wMDUzIn0=	2017-05-22 05:52:41.642548+01
tqom1dx4bar1m9pbc9vsaqvfhpw4y75j	NmRlYWVkZTIwNjMwZjg0ZjRhZTBjNzliZDk0N2IzMGQ5MjZjZDgwNTp7InRoZUNvb2tpZSI6Imd6QUYtNDMzNCJ9	2017-05-21 13:35:50.193428+01
0cvhsi8bfrs1g5eqc27y4b3jo8ypyafw	YzQxMDk0NTUxZjQxOGVmMmJjNGUxYWM5MzJkMTgzMGRlMzM4ODZkNTp7InRoZUNvb2tpZSI6IlZsR24tODQxMCIsInByQ29va2llIjoiTFZBRi04MjAzIn0=	2017-05-18 05:02:10.440356+01
p5jpxuhmq0d3w7xx134sko45ly9167ve	ZGQyZmU5ZDYyY2JhNTNmMWI3YjBmM2NmOWNhYWQ4OWMxNGQyYmU3ZDp7InByQ29va2llIjoiZFNyeC03NDg3IiwidGhlQ29va2llIjoicUdmeC0wNDk5In0=	2017-05-22 01:26:05.901592+01
nybywcvh4yamg9qmh1x9d3i32d2yf0vs	NjUxMzJkYTMyOWQ3N2Y3YzQ0MGZkMjA2MGM1YzgxZWI0YjY4ZmU0ZTp7InRoZUNvb2tpZSI6Ikt1Y3YtMjY3OSJ9	2017-05-16 02:11:55.535622+01
vkgu1fke5jybv4b4nh7xj5edriji0sr5	ZTBmZDFkYmEwODIzMjMyMGUxOTY0ZmI1OTI1NzY0YjRhMThiN2E5Njp7InRoZUNvb2tpZSI6IkhTcmYtODEzMiIsInByQ29va2llIjoiemhwci0wMDUzIn0=	2017-05-22 03:57:14.664327+01
zdwvqybst4yeq2t577p7ya5uwnpp6s1i	MjlkZWJmOTE3MzZiZjBiMGI0ZDUwNGM1NjIyZWUyZDBlMmM4YjI5ZTp7InBhckNvb2tpZSI6IjAwMi0xNyIsInRoZUNvb2tpZSI6InlTU0EtNzkyMSIsInByQ29va2llIjoiemhwci0wMDUzIn0=	2017-05-19 07:05:04.616404+01
odtm15xkma4ubrow34t4kz88l4vvypao	MjFhNjUxNmMxNGFlNTllZDI0ZTk4ODliODY1MDg2NGRiYjM3NjgzMDp7InRoZUNvb2tpZSI6IndXQ2ctNDY5OSIsInByQ29va2llIjoiemhwci0wMDUzIn0=	2017-05-18 23:21:25.224864+01
29cge0s9e89x8dcvz7cxtf9qusytqcx2	Njc2YzU4Y2I2YjBmMzcwYzAxN2ZmMDQxMmJiNWUyODQ2YmQ0NDE0Yjp7InRoZUNvb2tpZSI6ImJXa0stNzc5MyIsInByQ29va2llIjoiTFZBRi04MjAzIn0=	2017-05-21 22:06:32.29531+01
qmrytas0ls20p1vcngjb0m3596l9sw2a	YTRmYTU3MDkyNTY5MjA2ZWVkYmU3NjVlNDk1N2IxM2M1MmQxYWMxMjp7InRoZUNvb2tpZSI6InhSWnUtNDI3NyIsInByQ29va2llIjoiSmZIWi03NTIwIn0=	2017-05-18 05:52:42.814951+01
5x44wriglgwidgb8p16uggweorg9env4	Y2M1MDhhMjQ1NmFjMGIxMDRjZjhhNjc5YTFiNjQwNDhmNTZiMzRmOTp7InByQ29va2llIjoiTFZBRi04MjAzIiwidGhlQ29va2llIjoidWNacS04NjExIn0=	2017-05-17 19:14:31.746483+01
57uvde08zg9n3t78rqym192r2u16nu0r	NTczNjg3NTk1NDVjYjdjMWFmMjljOWNiYWYzODcwZDUzODgxYzY5MTp7InByQ29va2llIjoiemhwci0wMDUzIiwidGhlQ29va2llIjoiS21zSi0wNjYzIn0=	2017-05-19 07:32:43.095178+01
b68rsdccau2ehxgzk4un62k49skeubq8	MWY0NmMwOTJmMmFhYjBiZjNiNjhkZjQwNmI5MzYxYzcxZjYzZGRiNTp7InByQ29va2llIjoidVlwRS02MjY5IiwidGhlQ29va2llIjoib3RZQS00OTUxIn0=	2017-05-18 07:00:22.780443+01
g9oinbm5qpk23zw7m31a6zk5vbg9maod	ZTFiZjIxZTNlNGEwMGE2MTY3MWY2OWNjZWY1ZDRkZDNjNDQ0YTU4ZTp7InRoZUNvb2tpZSI6IlhDbnctNDg5NiJ9	2017-05-20 22:16:07.020919+01
xiybm0qf4g811ur0flb56ly5pcnwvb0g	YmExNjBhZjAwNGU2YmM0ODM5Y2U4YzQwYmRmZThlMzYyZjY0MDc2MDp7InByQ29va2llIjoicVVlSS0wNTA0IiwidGhlQ29va2llIjoiUklmRy0zNzQ5In0=	2017-06-01 08:43:38.659421+01
elxvzcnq58eclh0fua6gle7ronvmxyxx	MGUzZGNmNWZmZWQ1NWVkZWFhODIyYWNmNDczYzVlMTNlNzE3OGM0YTp7InBhckNvb2tpZSI6IjAwMi0xNyIsInByQ29va2llIjoiZFNyeC03NDg3IiwidGhlQ29va2llIjoiQmVoSi01ODc4In0=	2017-05-22 08:31:46.585738+01
vlh6jm7icyw9zfrch6bvw55f5ak0acij	NThlMTE0NTg5OGViODc5NWE2NGVhNGQ3NTQ3Yzk1MDA0NTA5MzA4Yzp7InRoZUNvb2tpZSI6IkRWSkgtMzI4MSJ9	2017-05-26 07:56:12.047371+01
gmww52gk0qz0p1u4rwgy8uxy9gezg3kb	ZDg3ZDU1MDM3MTk5N2UxNDRmM2M1MmFkYTA4NjRlNjI3NWM2NmI1Yzp7InBhckNvb2tpZSI6IjAwMS0xNyIsInRoZU9mZklEIjoiSVQtUGh5c2ljcyIsInBvQ29va2llIjoiMDAzLTE3IiwicHJDb29raWUiOiJkU3J4LTc0ODciLCJ0aGVEZXB0SUQiOiJDTlNNIiwidGhlQ29va2llIjoidXBEYS0xNTU5In0=	2017-05-22 23:35:23.958074+01
3i93tger6d91iphujvxibv6bkl2b5g5r	ZWQ0YThlMDJhNWU5MmU1Y2RlOTNmMjBkZDE5ZjJlMWI1NGY1YjQ3ZTp7InRoZUNvb2tpZSI6IkxnYW0tNjc3NCIsInByQ29va2llIjoiZFNyeC03NDg3In0=	2017-05-22 06:16:37.49199+01
1y7cxtvw02k2omotzhz0ict57u1r9i3j	NWZmOTFiMjY0MmJkNGZmMzc5NWVjYWZlN2NjNDc5OTgyOTFmYzYwMzp7InRoZUNvb2tpZSI6IklzS3QtNDYzOCJ9	2017-06-08 09:33:40.141465+01
y73wca8x8qch4qxfmqau8gnr35ymmbpf	YjM4NGM3NWI0YTU4NmI0ZDY0ODZkMzg3ODhkY2U5ZmFhMTRlNzVhNDp7InRoZUNvb2tpZSI6ImpYSFAtNzc4OCJ9	2017-05-23 08:41:30.110037+01
9pa4y88r74gf6lk26j8pyjybzww6sh5i	M2UwMDkxYmJkMjdkMmJmYzc2MGU3Mjk0ZjQxN2E4MjFlN2RjNDRjNTp7InRoZUNvb2tpZSI6Ik1jSFMtOTA3NSJ9	2017-05-30 07:15:21.07398+01
tahalbxpv9w9k4wd9tahlbhcvdyc25ko	NDcyMjQ1MWI4YTk5NzI5NjA2MTBiNTlhMmM1YWZhZDkzOGM1NTQxOTp7InRoZUNvb2tpZSI6IkFtT1EtNzI2MCJ9	2017-05-29 17:35:23.19768+01
uoz1m17565ql1784r5zeis3bikbycuhk	YzA5YTM2YTA4MTliMTMxODQ1MWEzNzRmMTZmYWRlOTZlMzU3OTU4MTp7InByQ29va2llIjoiYlpkVi0xMzY4IiwidGhlQ29va2llIjoiU0FjdC00MzgwIn0=	2017-05-25 07:25:21.319774+01
ei7g5nwl2g3wbw5oclqqb6llqilyou6j	ODlkYTE1MGU1ZDQ5MTBhYzkxNjI5M2VhMWUxMWM1NWNiZTlkNGVhYjp7InRoZUNvb2tpZSI6IkF4em8tMjUxOSJ9	2017-05-31 12:05:58.565038+01
ptpaq94q2adz8ori0mminztzpbnn8em6	N2NlYjAzOTY3YmQyYjgzM2IzYzM2YTBhYzJiNGIxOTA0MGY3ZWI1Mjp7InRoZU9mZklEIjoiSVQtUGh5c2ljcyIsInRoZUNvb2tpZSI6IlJoUlgtMTIyNCIsInRoZURlcHRJRCI6IkNOU00ifQ==	2017-05-23 05:51:27.937216+01
yp2pj8jahdrsgjpfzodwsf3polcpock1	ZDNlMzUyMzQ5N2M4YjRjNzBjZTg1NmJlNjkwNTBlODkwYmM2Njk5ZTp7InRoZUNvb2tpZSI6InFvbEstNjMxMyJ9	2017-05-22 10:16:41.317785+01
mcvnal0v10x73yexw8sb1l4ayi9uxer7	NTBkY2ExMWNiNjY3M2FmN2I5MGQ3YmY5ZTY3YmQ2MWEyMTE5OTc0ODp7InBvQ29va2llIjoiMDAyLTE3IiwidGhlQ29va2llIjoidnpBWC02NzUzIiwicHJDb29raWUiOiJtRkFLLTYzMTQifQ==	2017-06-08 10:46:39.854799+01
jisxi3gdwvotesei5jyurub0l62rghgy	NTlhMmQxNmEzMzI3NTBlMWY3ZDA4YWQ4NzAxNjQ1ZmE2YWE0MzI3ZTp7InByQ29va2llIjoibWhTcC0zOTU1IiwidGhlQ29va2llIjoib3lkVy0yODEwIn0=	2017-05-30 09:39:56.124884+01
938qhbvghsx29fwjlmw6rwft13hlx7wu	YTY5OTk1NzAwYWRhNzU5ZmU0ZWQ5YmMxMTk3NjQ4NzQ5MzJlYjBhMjp7InRoZUNvb2tpZSI6IlhYR0YtMzM0MiJ9	2017-05-30 16:28:40.248691+01
tccp3qm90mhxma4ppuumji921edctsgx	Mzk1NDQwNDg3ZTk3NWM2MDMyZTJmYzBmMzk1NDkwMTM5YWQ5YTZjZDp7InByQ29va2llIjoiSXhIaC0wNTcyIiwidGhlQ29va2llIjoielJpZC0xMjAwIn0=	2017-05-27 13:02:40.279406+01
cars6ob6s6ryrw5zl59r3yst4egm9jvw	NmEyYWY2MWQ5MzlmNDZhZTA1ZmQ0NDBkYTFlODk4ZjRjMjQ5MTVhYTp7InByQ29va2llIjoibXRoYi02MzM3IiwidGhlQ29va2llIjoiQWJOZy00NTI2In0=	2017-06-01 08:42:13.616828+01
vf2cc27tezof231pt56712ophraf51pj	YTM3YzIxYjI2MmQzZmI1ZjMwZjAzMzRjZWZiMjJjNzE2OWQwNWNjYjp7InRoZUNvb2tpZSI6Ik9nY1EtMzYzMiJ9	2017-05-28 18:13:57.080618+01
iyqbq595vfpywkus7zpszrsbhwwl4zcf	NWY4OWExMTQ4MmQ4MGIzOTRmZDk3MTM1ZmQ5NTQ3NTZlZjcxMWUzZjp7InRoZUNvb2tpZSI6IkhDTHktMzczMyJ9	2017-05-29 10:51:18.732136+01
bo4wwo7mqsvgxob9ini3w6morka8adkq	ODk3OTkwYTAxODk5ODMzY2E4MGU0MjVhNmQyNTk5YzZmMmVhYWMyNTp7fQ==	2017-07-07 23:40:22.155094+01
ol8w1r8w6vn4vx00nto0m43cetqai5zp	ODk3OTkwYTAxODk5ODMzY2E4MGU0MjVhNmQyNTk5YzZmMmVhYWMyNTp7fQ==	2017-07-07 23:40:28.523133+01
9di9kefsx4tbmqttek2nr5ga5s7p7p61	ZDFhMTk5Yzc0ODQ2Y2U0YTZjYzlhNTFkNWUyNjJmNWFlODQ5NzVmMDp7InRoZUNvb2tpZSI6Ik9QSHYtNDU4NSJ9	2017-07-07 23:41:10.349849+01
xorbtqkqubpvns616pdc3xkspe8m0n1u	ZmJjNmQ4N2NhNWEwNTg0NGVkNTQwYTI2Y2NjYTg0MzBmYTA1NDUwOTp7InByQ29va2llIjoiYlpkVi0xMzY4IiwidGhlQ29va2llIjoiVkdrdy03MjM5In0=	2017-07-05 23:45:14.03311+01
enw0n3j2wx0uyt39tdt9tnjdywkumooj	NDZmYjRmOWM4YzhhOTMwOWVmMDg1NGQ0ZmEzM2VmMzk4NDdmYWRiODp7InRoZUNvb2tpZSI6IkRUSFotNjQ4MiIsInByQ29va2llIjoiMDA0LTE3In0=	2017-07-07 23:12:52.360579+01
\.


--
-- TOC entry 2315 (class 0 OID 16485)
-- Dependencies: 196
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY employees (idnum, fname, sname, designation, dept, rank, title, mname) FROM stdin;
2016-0001	Kotarou	Katsura	Revolutionary IV	Joishishi	\N	\N	\N
2016-0002	Gintoki	Sakata	Natural Perm VIII	Yurozuya	\N	\N	\N
2016-0003	Kenpachi	Zaraki	Captain	Gotei 13	\N	\N	\N
2016-0004	Kakashi	Hatake	Hokage	Konohagakure	\N	\N	\N
2013-0212	Puti	Datu	Vinegar	Condiments	\N	\N	\N
2013-0213	Tomas	Mang	All-around Sarsa	Condiments	\N	\N	\N
2013-0214	Sita	Mama	Oyster Sauce	Condiments	\N	\N	\N
2013-0215	Ketchup	UFC	Tamis-Anghang Ketchup	Condiments	\N	\N	\N
2016-0011	Rin	Okumura	AC- Head	AccCenter	\N	\N	\N
2016-0012	Janno	Trajano	Dean	CNSM	Professor V	Ph.D	\N
2016-0013	Diana	Acana	Chairman	IT-Physics	\N	Ph.D	\N
2016-0014	Iris	Marcellones	VCAA	VCAA	\N	\N	\N
2016-0015	Shigeo	Kageyama	Chairman	Math	\N	Ph.D	\N
2016-0016	CNSM	Dummy ACCT	Dummy Pos	CNSM	\N	\N	\N
2017-1152	Non_Requi	Test	Dummy	Dummy	\N	\N	\N
2017-0623	\N	\N	\N	\N	\N	\N	\N
2017-0723	\N	\N	\N	\N	\N	\N	\N
2017-0823	\N	\N	\N	\N	\N	\N	\N
2017-0923	\N	\N	\N	\N	\N	\N	\N
2017-0622	\N	\N	\N	\N	\N	\N	\N
2017-0722	\N	\N	\N	\N	\N	\N	\N
2017-0822	\N	\N	\N	\N	\N	\N	\N
2017-0922	\N	\N	\N	\N	\N	\N	\N
2017-0002	Mary Lynn	Abiera	VCAA	VCAA	\N	\N	S                                                                                                   
2017-0003	Virgilio	Ramos	VCAF	VCAF	\N	\N	\N
2017-0122	Genryusai	Yamamoto	Chairman	IT-Physics	\N	\N	\N
2017-0123	Madara	Uchiha	Dean	CNSM	\N	\N	\N
2017-0156	Izuku	Midoriya	Faculty	IT-Physics	\N	\N	\N
2017-0178	Kazuto	Kirigaya	Faculty	IT-Physics	\N	\N	\N
2017-0222	Lalatina	Dustiness Ford	Chairman	Math	\N	\N	\N
2017-0223	Shoyo	Hinata	Faculty	Math	\N	\N	\N
2017-0256	Tobio	Kageyama	Faculty	Math	\N	\N	\N
2017-0278	Shigeo	Kageyama	Dean	CSSH	\N	\N	\N
2017-0322	Zoro	Roronoa	Faculty	English	\N	\N	\N
2017-0323	Asuna	Yuuki	Chairman	English	\N	\N	\N
2017-0356	Hinata	Hyuga	Faculty	English	\N	\N	\N
2017-0378	Tuoka	Kirishima	Head	SMO	\N	\N	\N
2017-0422	Rize	Kamishiro	Employee	SMO	\N	\N	\N
2017-0423	Rukia	Kuchiki	Head	Proc	\N	\N	\N
2017-0456	Akane	Tsunemori	Secretary	Proc	\N	\N	\N
2017-0478	Rin	Okumura	Faculty	IT-Physics	\N	\N	\N
2017-0522	Mikasa	Ackerman	Secretary	OC	\N	\N	\N
2017-0523	Annie	Leonhart	Secretary	VCAA	\N	\N	\N
2017-0556	Natsu	Dragneel	Faculty	Math	\N	\N	\N
2017-0001	Abdurrahman	Canacan	University Chancellor	OC	\N	\N	T                                                                                                   
2017-0578	User	Demo	Officer in Charge	Demo	\N	\N	\N
2013-0211	Swan	Silver	Soy Sauce	Condiments	\N	\N	\N
\.


--
-- TOC entry 2316 (class 0 OID 16491)
-- Dependencies: 197
-- Data for Name: equip_particulars; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY equip_particulars (idname, name, subhead, itemnum) FROM stdin;
land	Land and Land Improvement	\N	1
acadblg	Academic/School Buildings	\N	2
others	Other Structures	\N	3
machine	Machinery Equipment	\N	4
comequi	Communication Equipment	machine	4.1
fire	Fire Figthing equipment and Accessories	machine	4.2
it	Information Technology Equipment and Accessories	machine	4.3
medic	Medical and Dental Equipment	machine	4.4
military	Military, Police and Security Equipment	machine	4.5
science	Scientific Equipment and Related Materials	machine	4.6
sound	Sound System Equipment and Accessories	machine	4.7
sports	Sports Equipment and Accessories	machine	4.8
trans	Transportation Equipment	\N	5
motor	Motor Vehicles, Parts and Accessories	trans	5.1
fix	Furniture Fixtures and Books	\N	6
otherprop	Other Property, Plant and Equipment	\N	7
livestock	Livestocks	\N	8
\.


--
-- TOC entry 2330 (class 0 OID 16766)
-- Dependencies: 211
-- Data for Name: iar_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY iar_items (iarnum, stocknum, unit, description, quantity, compstat, compdate, workstat, workdate, compstatmiss, workstatmiss) FROM stdin;
\.


--
-- TOC entry 2331 (class 0 OID 16777)
-- Dependencies: 212
-- Data for Name: insp_and_accept_report; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY insp_and_accept_report (iarnum, ponum, reqoff, podate, recieptnum, recieptdate, insstatus, insdate, insofficer, isitemcomplete, receivedate, receiveofficer, counter) FROM stdin;
\.


--
-- TOC entry 2335 (class 0 OID 16834)
-- Dependencies: 216
-- Data for Name: inventory; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY inventory (invnum, parnum, description, unit, unitprice, quantity, status) FROM stdin;
\.


--
-- TOC entry 2317 (class 0 OID 16506)
-- Dependencies: 198
-- Data for Name: items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY items (itemid, description, type, class, unit, price) FROM stdin;
OprG-5214	Computer	Desktop	Equipment	Unit	41000
ErTY-3211	Printer	Ink-Jet	Equipment	Unit	8000
yTRe-4538	Computer	Laptop	Equipment	Unit	36000
rPtg-3853	Projector	\N	Equipment	Unit	12000
XcTp-6954	Computer Monitor	LED	Equipment	Piece	8000
\.


--
-- TOC entry 2318 (class 0 OID 16509)
-- Dependencies: 199
-- Data for Name: keypositions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY keypositions (id, empid) FROM stdin;
chancelor	2017-0001
vcaf	2017-0003
vcaa	2017-0002
\.


--
-- TOC entry 2332 (class 0 OID 16790)
-- Dependencies: 213
-- Data for Name: log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY log (logid, idnum, accttype, datetimeloggoed) FROM stdin;
OPHv-4585	2013-0211	\N	\N
\.


--
-- TOC entry 2333 (class 0 OID 16795)
-- Dependencies: 214
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY notifications (notifnum, fromid, toid, status, priority, notifref, details, dateofnotif, timeofnotif, type, reftype) FROM stdin;
\.


--
-- TOC entry 2319 (class 0 OID 16521)
-- Dependencies: 200
-- Data for Name: offices; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY offices (id, name, type, head, authopersonel, division) FROM stdin;
SMO	Supply Management Office	administrative	\N	\N	VCAF
OC	Office of the University Chancellor	administrative	\N	\N	OC
MSU-CC	MSU - Computer Center	administrative	\N	\N	VCAF
VCAF	Office of the Vice Chancellor for Administration and Finances	administrative	\N	\N	VCAF
ComLab2	IT - Computer Laboratory 2	academics	\N	\N	CNSM
CSSH	College of Social Sciences and Humanities	college	\N	\N	VCAA
AccCenter	MSU - Accreditation Center	academics	2016-0011	\N	VCAA
CNSM	College of Natural Sciences and Mathematics	college	2016-0012	\N	VCAA
IT-Physics	Information Technology and Physics Department	department	2016-0013	\N	CNSM
VCAA	Office of the Vice Chancellor for Academic Affairs	academics	2016-0014	\N	VCAA
Mathematics	\N	\N	\N	\N	\N
Math	Mathematics Department	department	\N	\N	CNSM
Bio	Biology Department	department	\N	\N	CNSM
Demo	Demonstration Office	administrative	2017-0578	\N	VCAF
\.


--
-- TOC entry 2320 (class 0 OID 16524)
-- Dependencies: 201
-- Data for Name: physical_count; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY physical_count  FROM stdin;
\.


--
-- TOC entry 2334 (class 0 OID 16823)
-- Dependencies: 215
-- Data for Name: property_acc_receipt; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY property_acc_receipt (parnum, dateofpar, receiveby, datereceiveby, receivefrom, datereceivefrom, ponum, counter) FROM stdin;
\.


--
-- TOC entry 2336 (class 0 OID 16839)
-- Dependencies: 217
-- Data for Name: purchase_order; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY purchase_order (ponum, supplier, datecreated, procmode, dateofdelivery, placeofdelivery, deliveryterm, paymentterm, amount, status, deliverystatus, paymentstatus, conforme, prref, counter, fundref, approval_date, serve_date) FROM stdin;
\.


--
-- TOC entry 2337 (class 0 OID 16847)
-- Dependencies: 218
-- Data for Name: purchase_order_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY purchase_order_items (ponum, itemnum, quantity, unit, description, unitcost) FROM stdin;
\.


--
-- TOC entry 2338 (class 0 OID 16850)
-- Dependencies: 219
-- Data for Name: purchase_request; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY purchase_request (reqnum, prnum, purpose, purpose_details, requester_id, date_created, status, init_approval_status, approval_status, declinereason, counter, approval_staus_date) FROM stdin;
\.


--
-- TOC entry 2339 (class 0 OID 16867)
-- Dependencies: 220
-- Data for Name: purchase_request_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY purchase_request_items (reqnum, stock_num, description, unit, unit_price, quantity) FROM stdin;
\.


--
-- TOC entry 2340 (class 0 OID 16870)
-- Dependencies: 221
-- Data for Name: received_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY received_items (iarnum, availability, description, quantity, price, itemnum) FROM stdin;
\.


--
-- TOC entry 2321 (class 0 OID 16551)
-- Dependencies: 202
-- Data for Name: received_items_list; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY received_items_list  FROM stdin;
\.


--
-- TOC entry 2341 (class 0 OID 16912)
-- Dependencies: 222
-- Data for Name: req_for_quotation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY req_for_quotation (quotationnum, refnum, projname, projlocation, datecreated, canvasser, counter) FROM stdin;
\.


--
-- TOC entry 2342 (class 0 OID 16925)
-- Dependencies: 223
-- Data for Name: req_for_quotation_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY req_for_quotation_items (quotationnum, itemnum, description, quantity, unit, unitprice) FROM stdin;
\.


--
-- TOC entry 2343 (class 0 OID 16937)
-- Dependencies: 224
-- Data for Name: req_for_quotation_suppliers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY req_for_quotation_suppliers (quotationnum, compid, warrantyper, delperiod, pricevalidity) FROM stdin;
\.


--
-- TOC entry 2322 (class 0 OID 16566)
-- Dependencies: 203
-- Data for Name: suppliers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY suppliers (compid, name, address, comprep, reptel, repemail, comptin, dateadded, rating, ratingupdate) FROM stdin;
Dzgh-3783	Star Bright Office Depot	Quirino Ave, General Santos City	Katsura Kotarou	123-1234-567	zura@joishishi.com	123-4567	\N	\N	\N
kLjY-9965	KCC Mall of Gensan	Lagao, General Santos City	Juan Dela Cruz	123-4566	juan@kccmall.com	123-1234	\N	\N	\N
DuYh-5412	Yurozuya Gin-chan	Kabuki District, Edo, Japan	Sakata Gintoki	1259-12584	gin@edo.jp	125-9846	\N	\N	\N
ldSr-8547	Karakura Candy Shop	Karakura Town, Japan	Urahara Kisuke	5844-68556	princess@gotie13.jp	685-9654	\N	\N	\N
hyQQ-5235	Antique Coffe Shop	20th Ward, Tokyo, Japan	Yoshimura Kuzen	2155-86655	owl@antique.jp	122-5662	\N	\N	\N
TYui-8332	Boars Hat	Lioness Kingdom, Britania	Meliodas	2558-8741	dragon@sevensins.jp	899-6566	\N	\N	\N
\.


--
-- TOC entry 2323 (class 0 OID 16572)
-- Dependencies: 204
-- Data for Name: test; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY test (dr, re) FROM stdin;
\N	\N
\N	\N
2012-03-15	\N
2017-12-12	t
\.


--
-- TOC entry 2324 (class 0 OID 16575)
-- Dependencies: 205
-- Data for Name: transactions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY transactions  FROM stdin;
\.


--
-- TOC entry 2325 (class 0 OID 16578)
-- Dependencies: 206
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY users (uname, pass, idnum, access_type, profile_pic, status) FROM stdin;
kem1101231	condigago	\N	\N	\N	\N
smoadmin	pass	2013-0212	{3}	\N	t
procadmin	pass	2013-0213	{2}	\N	\N
approv	pass	2013-0214	{1}	\N	\N
gin1101	haaaaa	2016-0002	{2}	\N	t
zura1101	zurajanaikatsurada	2016-0001	{3}	\N	t
ora220	umoshereze	2016-0003	{4}	\N	\N
sharingan	obito	2016-0004	{1}	\N	\N
init_approv	pass	2013-0215	{1}	\N	t
kem1101233	condigago	\N	\N	\N	\N
cnsm	deanlogin	2016-0012	{4}	\N	t
kem22012	condigago	2016-0015	{4}	\N	\N
lop	jk	2016-0016	{4}	\N	\N
test5	pass	2017-1152	{5}	\N	t
kj10	condi		{3,3}	\N	\N
kem1101	condigago	2011-0813	{0}	\N	\N
vcaf	password	2017-0003	{1}	\N	t
chancellor	password	2017-0001	{1}	\N	t
requi	pass	2013-0211	{4}	\N	t
demo	pass	2017-0578	{4}	\N	t
\.


--
-- TOC entry 2326 (class 0 OID 16584)
-- Dependencies: 207
-- Data for Name: waste_mat_report; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY waste_mat_report  FROM stdin;
\.


--
-- TOC entry 2156 (class 2606 OID 16750)
-- Name: abstract_of_canvass_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY abstract_of_canvass
    ADD CONSTRAINT abstract_of_canvass_pkey PRIMARY KEY (canvassnum);


--
-- TOC entry 2094 (class 2606 OID 16599)
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- TOC entry 2100 (class 2606 OID 16601)
-- Name: auth_group_permissions_group_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- TOC entry 2102 (class 2606 OID 16603)
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 2096 (class 2606 OID 16605)
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- TOC entry 2105 (class 2606 OID 16607)
-- Name: auth_permission_content_type_id_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- TOC entry 2107 (class 2606 OID 16609)
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- TOC entry 2116 (class 2606 OID 16611)
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- TOC entry 2118 (class 2606 OID 16613)
-- Name: auth_user_groups_user_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- TOC entry 2109 (class 2606 OID 16615)
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- TOC entry 2122 (class 2606 OID 16617)
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 2124 (class 2606 OID 16619)
-- Name: auth_user_user_permissions_user_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- TOC entry 2112 (class 2606 OID 16621)
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- TOC entry 2126 (class 2606 OID 16623)
-- Name: college_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY college
    ADD CONSTRAINT college_pkey PRIMARY KEY (id);


--
-- TOC entry 2130 (class 2606 OID 16625)
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- TOC entry 2132 (class 2606 OID 16627)
-- Name: django_content_type_app_label_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- TOC entry 2134 (class 2606 OID 16629)
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- TOC entry 2136 (class 2606 OID 16631)
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- TOC entry 2139 (class 2606 OID 16633)
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- TOC entry 2142 (class 2606 OID 16635)
-- Name: employees_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (idnum);


--
-- TOC entry 2144 (class 2606 OID 16637)
-- Name: equip_particulars_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY equip_particulars
    ADD CONSTRAINT equip_particulars_pkey PRIMARY KEY (idname);


--
-- TOC entry 2091 (class 2606 OID 16639)
-- Name: equipment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY asset
    ADD CONSTRAINT equipment_pkey PRIMARY KEY (asset_id);


--
-- TOC entry 2158 (class 2606 OID 16784)
-- Name: insp_and_accept_report_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY insp_and_accept_report
    ADD CONSTRAINT insp_and_accept_report_pkey PRIMARY KEY (iarnum);


--
-- TOC entry 2166 (class 2606 OID 16838)
-- Name: inventory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY inventory
    ADD CONSTRAINT inventory_pkey PRIMARY KEY (invnum);


--
-- TOC entry 2146 (class 2606 OID 16645)
-- Name: items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY items
    ADD CONSTRAINT items_pkey PRIMARY KEY (itemid);


--
-- TOC entry 2148 (class 2606 OID 16647)
-- Name: keypositions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY keypositions
    ADD CONSTRAINT keypositions_pkey PRIMARY KEY (id);


--
-- TOC entry 2160 (class 2606 OID 16794)
-- Name: log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY log
    ADD CONSTRAINT log_pkey PRIMARY KEY (logid);


--
-- TOC entry 2162 (class 2606 OID 16802)
-- Name: notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (notifnum);


--
-- TOC entry 2150 (class 2606 OID 16653)
-- Name: offices_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY offices
    ADD CONSTRAINT offices_pkey PRIMARY KEY (id);


--
-- TOC entry 2164 (class 2606 OID 16827)
-- Name: property_acc_receipt_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY property_acc_receipt
    ADD CONSTRAINT property_acc_receipt_pkey PRIMARY KEY (parnum);


--
-- TOC entry 2168 (class 2606 OID 16846)
-- Name: purchase_order_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY purchase_order
    ADD CONSTRAINT purchase_order_pkey PRIMARY KEY (ponum);


--
-- TOC entry 2170 (class 2606 OID 16857)
-- Name: purchase_request_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY purchase_request
    ADD CONSTRAINT purchase_request_pkey PRIMARY KEY (reqnum);


--
-- TOC entry 2172 (class 2606 OID 16919)
-- Name: req_for_quotation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY req_for_quotation
    ADD CONSTRAINT req_for_quotation_pkey PRIMARY KEY (quotationnum);


--
-- TOC entry 2152 (class 2606 OID 16663)
-- Name: suppliers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY suppliers
    ADD CONSTRAINT suppliers_pkey PRIMARY KEY (compid);


--
-- TOC entry 2154 (class 2606 OID 16665)
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (uname);


--
-- TOC entry 2092 (class 1259 OID 16666)
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_group_name_a6ea08ec_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- TOC entry 2097 (class 1259 OID 16667)
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_group_permissions_0e939a4f ON auth_group_permissions USING btree (group_id);


--
-- TOC entry 2098 (class 1259 OID 16668)
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_group_permissions_8373b171 ON auth_group_permissions USING btree (permission_id);


--
-- TOC entry 2103 (class 1259 OID 16669)
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_permission_417f1b1c ON auth_permission USING btree (content_type_id);


--
-- TOC entry 2113 (class 1259 OID 16670)
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_groups_0e939a4f ON auth_user_groups USING btree (group_id);


--
-- TOC entry 2114 (class 1259 OID 16671)
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_groups_e8701ad4 ON auth_user_groups USING btree (user_id);


--
-- TOC entry 2119 (class 1259 OID 16672)
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_8373b171 ON auth_user_user_permissions USING btree (permission_id);


--
-- TOC entry 2120 (class 1259 OID 16673)
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON auth_user_user_permissions USING btree (user_id);


--
-- TOC entry 2110 (class 1259 OID 16674)
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_username_6821ab7c_like ON auth_user USING btree (username varchar_pattern_ops);


--
-- TOC entry 2127 (class 1259 OID 16675)
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX django_admin_log_417f1b1c ON django_admin_log USING btree (content_type_id);


--
-- TOC entry 2128 (class 1259 OID 16676)
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX django_admin_log_e8701ad4 ON django_admin_log USING btree (user_id);


--
-- TOC entry 2137 (class 1259 OID 16677)
-- Name: django_session_de54fa62; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX django_session_de54fa62 ON django_session USING btree (expire_date);


--
-- TOC entry 2140 (class 1259 OID 16678)
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX django_session_session_key_c0390e0f_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- TOC entry 2173 (class 2606 OID 16684)
-- Name: auth_group_permiss_permission_id_84c5c92e_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permiss_permission_id_84c5c92e_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2174 (class 2606 OID 16689)
-- Name: auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2175 (class 2606 OID 16694)
-- Name: auth_permiss_content_type_id_2f476e4b_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permiss_content_type_id_2f476e4b_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2176 (class 2606 OID 16699)
-- Name: auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2177 (class 2606 OID 16704)
-- Name: auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2178 (class 2606 OID 16709)
-- Name: auth_user_user_per_permission_id_1fbb5f2c_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_per_permission_id_1fbb5f2c_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2179 (class 2606 OID 16714)
-- Name: auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2180 (class 2606 OID 16719)
-- Name: django_admin_content_type_id_c4bce8eb_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_content_type_id_c4bce8eb_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2181 (class 2606 OID 16724)
-- Name: django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2182 (class 2606 OID 16920)
-- Name: req_for_quotation_quotationnum_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY req_for_quotation
    ADD CONSTRAINT req_for_quotation_quotationnum_fkey FOREIGN KEY (quotationnum) REFERENCES req_for_quotation(quotationnum);


--
-- TOC entry 2350 (class 0 OID 0)
-- Dependencies: 7
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2017-06-24 06:42:35

--
-- PostgreSQL database dump complete
--

