--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.6
-- Dumped by pg_dump version 9.3.6
-- Started on 2017-02-16 13:26:55

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 217 (class 3079 OID 11750)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2260 (class 0 OID 0)
-- Dependencies: 217
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 170 (class 1259 OID 65537)
-- Name: abstract_of_canvass; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE abstract_of_canvass (
    canvassnum character varying(50) NOT NULL,
    bidnum character varying(50),
    dateofquotation date,
    dateopen date,
    recomendation text
);


ALTER TABLE public.abstract_of_canvass OWNER TO postgres;

--
-- TOC entry 171 (class 1259 OID 65540)
-- Name: abstract_of_canvass_supplier_price; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE abstract_of_canvass_supplier_price (
    canvassnum character varying(50),
    supplier character varying(150),
    itemnum integer,
    unit character varying(50),
    description character varying(250),
    unitprice double precision,
    sel_approval boolean,
    reason character varying(250)
);


ALTER TABLE public.abstract_of_canvass_supplier_price OWNER TO postgres;

--
-- TOC entry 172 (class 1259 OID 65546)
-- Name: account_items; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE account_items (
);


ALTER TABLE public.account_items OWNER TO postgres;

--
-- TOC entry 173 (class 1259 OID 65549)
-- Name: accounts; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE accounts (
);


ALTER TABLE public.accounts OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 73791)
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- TOC entry 201 (class 1259 OID 73789)
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO postgres;

--
-- TOC entry 2261 (class 0 OID 0)
-- Dependencies: 201
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- TOC entry 204 (class 1259 OID 73801)
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 73799)
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO postgres;

--
-- TOC entry 2262 (class 0 OID 0)
-- Dependencies: 203
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- TOC entry 200 (class 1259 OID 73783)
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- TOC entry 199 (class 1259 OID 73781)
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO postgres;

--
-- TOC entry 2263 (class 0 OID 0)
-- Dependencies: 199
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- TOC entry 206 (class 1259 OID 73809)
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


ALTER TABLE public.auth_user OWNER TO postgres;

--
-- TOC entry 208 (class 1259 OID 73819)
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO postgres;

--
-- TOC entry 207 (class 1259 OID 73817)
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO postgres;

--
-- TOC entry 2264 (class 0 OID 0)
-- Dependencies: 207
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- TOC entry 205 (class 1259 OID 73807)
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO postgres;

--
-- TOC entry 2265 (class 0 OID 0)
-- Dependencies: 205
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- TOC entry 210 (class 1259 OID 73827)
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 73825)
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO postgres;

--
-- TOC entry 2266 (class 0 OID 0)
-- Dependencies: 209
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- TOC entry 174 (class 1259 OID 65552)
-- Name: college; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE college (
    id character varying(10) NOT NULL,
    name character varying(255)
);


ALTER TABLE public.college OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 73887)
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


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 73885)
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO postgres;

--
-- TOC entry 2267 (class 0 OID 0)
-- Dependencies: 211
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- TOC entry 198 (class 1259 OID 73773)
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- TOC entry 197 (class 1259 OID 73771)
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO postgres;

--
-- TOC entry 2268 (class 0 OID 0)
-- Dependencies: 197
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- TOC entry 175 (class 1259 OID 65555)
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- TOC entry 176 (class 1259 OID 65561)
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO postgres;

--
-- TOC entry 2269 (class 0 OID 0)
-- Dependencies: 176
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- TOC entry 213 (class 1259 OID 73915)
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- TOC entry 177 (class 1259 OID 65563)
-- Name: employees; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE employees (
    idnum character varying(15) NOT NULL,
    fname character varying(100),
    sname character varying(100),
    designation character varying(100),
    dept character varying(50),
    rank character varying(25),
    title character varying(25)
);


ALTER TABLE public.employees OWNER TO postgres;

--
-- TOC entry 178 (class 1259 OID 65566)
-- Name: equipment; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE equipment (
    equip_id character varying(10) NOT NULL,
    description character varying(250),
    unit character varying(50),
    unit_price double precision,
    equip_type character varying(50),
    equip_brand character varying(100),
    date_of_update date
);


ALTER TABLE public.equipment OWNER TO postgres;

--
-- TOC entry 179 (class 1259 OID 65569)
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
    workdate date
);


ALTER TABLE public.iar_items OWNER TO postgres;

--
-- TOC entry 180 (class 1259 OID 65572)
-- Name: insp_and_accept_report; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE insp_and_accept_report (
    iarnum character varying(15) NOT NULL,
    supplier character varying(180),
    ponum character varying(15),
    reqoff character varying(180),
    podate date,
    recieptnum character varying(150),
    recieptdate date,
    insstatus boolean,
    insdate date,
    insofficer character varying(15),
    isitemcomplete boolean,
    partialquan integer,
    receivedate date,
    receiveofficer character varying(15)
);


ALTER TABLE public.insp_and_accept_report OWNER TO postgres;

--
-- TOC entry 181 (class 1259 OID 65578)
-- Name: inventory; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE inventory (
    invnum integer NOT NULL,
    parnum character varying(25) NOT NULL,
    description character varying(255),
    unit character varying(50),
    unitprice double precision,
    status boolean
);


ALTER TABLE public.inventory OWNER TO postgres;

--
-- TOC entry 182 (class 1259 OID 65581)
-- Name: keypositions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE keypositions (
    id character varying(10) NOT NULL,
    empid character varying(15)
);


ALTER TABLE public.keypositions OWNER TO postgres;

--
-- TOC entry 193 (class 1259 OID 73747)
-- Name: log; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE log (
    logid character varying(15) NOT NULL,
    idnum character varying(15),
    accttype integer,
    datetimeloggoed date
);


ALTER TABLE public.log OWNER TO postgres;

--
-- TOC entry 194 (class 1259 OID 73752)
-- Name: notifications; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE notifications (
    notifnum character varying(15) NOT NULL,
    fromid character varying(15),
    toid character varying(15),
    status boolean,
    priority integer,
    notifref character varying(30),
    details character varying(50)[],
    dateofnotif date,
    timeofnotif time without time zone,
    type integer,
    reftype character varying(25)
);


ALTER TABLE public.notifications OWNER TO postgres;

--
-- TOC entry 183 (class 1259 OID 65593)
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


ALTER TABLE public.offices OWNER TO postgres;

--
-- TOC entry 184 (class 1259 OID 65596)
-- Name: physical_count; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE physical_count (
);


ALTER TABLE public.physical_count OWNER TO postgres;

--
-- TOC entry 185 (class 1259 OID 65599)
-- Name: property_acc_receipt; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE property_acc_receipt (
);


ALTER TABLE public.property_acc_receipt OWNER TO postgres;

--
-- TOC entry 186 (class 1259 OID 65602)
-- Name: purchase_order; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE purchase_order (
    ponum character varying(50) NOT NULL,
    supplier character varying(250),
    address character varying(250),
    tin character varying(50),
    datecreated date,
    procmode character varying(150),
    dateofdelivery date,
    placeofdelivery character varying(250),
    deliveryterm character varying(25),
    paymentterm character varying(25),
    amount double precision,
    status boolean,
    deliverystatus boolean,
    paymentstatus boolean
);


ALTER TABLE public.purchase_order OWNER TO postgres;

--
-- TOC entry 187 (class 1259 OID 65608)
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


ALTER TABLE public.purchase_order_items OWNER TO postgres;

--
-- TOC entry 195 (class 1259 OID 73760)
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
    declinereason text
);


ALTER TABLE public.purchase_request OWNER TO postgres;

--
-- TOC entry 196 (class 1259 OID 73768)
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


ALTER TABLE public.purchase_request_items OWNER TO postgres;

--
-- TOC entry 188 (class 1259 OID 65620)
-- Name: req_for_quotation; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE req_for_quotation (
    quotationnum character varying(15) NOT NULL,
    refnum character varying(50),
    projname character varying(255),
    projlocation character varying(255),
    datecreated date,
    canvasser character varying(150)
);


ALTER TABLE public.req_for_quotation OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 81926)
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


ALTER TABLE public.req_for_quotation_items OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 81920)
-- Name: req_for_quotation_suppliers; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE req_for_quotation_suppliers (
    quotationnum character varying(15),
    compid character varying(15),
    warrantyper double precision,
    delperiod double precision,
    pricevalidity double precision
);


ALTER TABLE public.req_for_quotation_suppliers OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 81929)
-- Name: suppliers; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE suppliers (
    compid character varying(25) NOT NULL,
    name character varying(255),
    address character varying(250),
    comprep character varying(250),
    reptel character varying(50),
    repemail character varying(50),
    comptin character varying(50)
);


ALTER TABLE public.suppliers OWNER TO postgres;

--
-- TOC entry 189 (class 1259 OID 65629)
-- Name: test; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE test (
    c character varying(5)[]
);


ALTER TABLE public.test OWNER TO postgres;

--
-- TOC entry 190 (class 1259 OID 65635)
-- Name: transactions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE transactions (
);


ALTER TABLE public.transactions OWNER TO postgres;

--
-- TOC entry 191 (class 1259 OID 65638)
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


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 192 (class 1259 OID 65644)
-- Name: waste_mat_report; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE waste_mat_report (
);


ALTER TABLE public.waste_mat_report OWNER TO postgres;

--
-- TOC entry 2004 (class 2604 OID 73794)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- TOC entry 2005 (class 2604 OID 73804)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- TOC entry 2003 (class 2604 OID 73786)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- TOC entry 2006 (class 2604 OID 73812)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- TOC entry 2007 (class 2604 OID 73822)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- TOC entry 2008 (class 2604 OID 73830)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- TOC entry 2009 (class 2604 OID 73890)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- TOC entry 2002 (class 2604 OID 73776)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- TOC entry 2001 (class 2604 OID 65647)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- TOC entry 2206 (class 0 OID 65537)
-- Dependencies: 170
-- Data for Name: abstract_of_canvass; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY abstract_of_canvass (canvassnum, bidnum, dateofquotation, dateopen, recomendation) FROM stdin;
\.


--
-- TOC entry 2207 (class 0 OID 65540)
-- Dependencies: 171
-- Data for Name: abstract_of_canvass_supplier_price; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY abstract_of_canvass_supplier_price (canvassnum, supplier, itemnum, unit, description, unitprice, sel_approval, reason) FROM stdin;
\.


--
-- TOC entry 2208 (class 0 OID 65546)
-- Dependencies: 172
-- Data for Name: account_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY account_items  FROM stdin;
\.


--
-- TOC entry 2209 (class 0 OID 65549)
-- Dependencies: 173
-- Data for Name: accounts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY accounts  FROM stdin;
\.


--
-- TOC entry 2238 (class 0 OID 73791)
-- Dependencies: 202
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_group (id, name) FROM stdin;
\.


--
-- TOC entry 2270 (class 0 OID 0)
-- Dependencies: 201
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_group_id_seq', 1, false);


--
-- TOC entry 2240 (class 0 OID 73801)
-- Dependencies: 204
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- TOC entry 2271 (class 0 OID 0)
-- Dependencies: 203
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 1, false);


--
-- TOC entry 2236 (class 0 OID 73783)
-- Dependencies: 200
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
-- TOC entry 2272 (class 0 OID 0)
-- Dependencies: 199
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_permission_id_seq', 18, true);


--
-- TOC entry 2242 (class 0 OID 73809)
-- Dependencies: 206
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
\.


--
-- TOC entry 2244 (class 0 OID 73819)
-- Dependencies: 208
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- TOC entry 2273 (class 0 OID 0)
-- Dependencies: 207
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 1, false);


--
-- TOC entry 2274 (class 0 OID 0)
-- Dependencies: 205
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_user_id_seq', 1, false);


--
-- TOC entry 2246 (class 0 OID 73827)
-- Dependencies: 210
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- TOC entry 2275 (class 0 OID 0)
-- Dependencies: 209
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);


--
-- TOC entry 2210 (class 0 OID 65552)
-- Dependencies: 174
-- Data for Name: college; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY college (id, name) FROM stdin;
\.


--
-- TOC entry 2248 (class 0 OID 73887)
-- Dependencies: 212
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- TOC entry 2276 (class 0 OID 0)
-- Dependencies: 211
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 1, false);


--
-- TOC entry 2234 (class 0 OID 73773)
-- Dependencies: 198
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
-- TOC entry 2277 (class 0 OID 0)
-- Dependencies: 197
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('django_content_type_id_seq', 6, true);


--
-- TOC entry 2211 (class 0 OID 65555)
-- Dependencies: 175
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2017-02-13 16:07:11.295832-08
2	auth	0001_initial	2017-02-13 16:07:12.139732-08
3	admin	0001_initial	2017-02-13 16:07:12.342885-08
4	admin	0002_logentry_remove_auto_add	2017-02-13 16:07:12.389753-08
5	contenttypes	0002_remove_content_type_name	2017-02-13 16:07:12.483477-08
6	auth	0002_alter_permission_name_max_length	2017-02-13 16:07:12.530357-08
7	auth	0003_alter_user_email_max_length	2017-02-13 16:07:12.577252-08
8	auth	0004_alter_user_username_opts	2017-02-13 16:07:12.717855-08
9	auth	0005_alter_user_last_login_null	2017-02-13 16:07:12.764765-08
10	auth	0006_require_contenttypes_0002	2017-02-13 16:07:12.780382-08
11	auth	0007_alter_validators_add_error_messages	2017-02-13 16:07:12.811635-08
12	auth	0008_alter_user_username_max_length	2017-02-13 16:07:12.889983-08
13	sessions	0001_initial	2017-02-13 16:07:13.032179-08
\.


--
-- TOC entry 2278 (class 0 OID 0)
-- Dependencies: 176
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('django_migrations_id_seq', 13, true);


--
-- TOC entry 2249 (class 0 OID 73915)
-- Dependencies: 213
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
h9pooz81myhw6zc7tutq8tx2o791219a	NTVmYWM1YzYzNjc1NGY3NGQyNzk5Mjg2NjllNDYxNjNlOTRhOGFhYzp7InRoZUNvb2tpZSI6ImxBUHQtMzQ0MiJ9	2017-03-01 16:46:02.237025-08
p1qz2h0m6aj5nygvayn8eur29rslsunf	Y2ZkNDYwMTZkN2ZlMzQxYTFmZDI5ZDMwZTgzZTJkNTczNDhjNGY3Mjp7InRoZURlcHRJRCI6IkNOU00iLCJ0aGVPZmZJRCI6IlZDQUYiLCJ0aGVDb29raWUiOiJuQUdpLTg4NjIifQ==	2017-03-01 16:52:27.192299-08
\.


--
-- TOC entry 2213 (class 0 OID 65563)
-- Dependencies: 177
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY employees (idnum, fname, sname, designation, dept, rank, title) FROM stdin;
2016-0001	Kotarou	Katsura	Revolutionary IV	Joishishi	\N	\N
2016-0002	Gintoki	Sakata	Natural Perm VIII	Yurozuya	\N	\N
2016-0003	Kenpachi	Zaraki	Captain	Gotei 13	\N	\N
2016-0004	Kakashi	Hatake	Hokage	Konohagakure	\N	\N
2013-0211	Swan	Silver	Soy Sauce	Condiments	\N	\N
2013-0212	Puti	Datu	Vinegar	Condiments	\N	\N
2013-0213	Tomas	Mang	All-around Sarsa	Condiments	\N	\N
2013-0214	Sita	Mama	Oyster Sauce	Condiments	\N	\N
2013-0215	Ketchup	UFC	Tamis-Anghang Ketchup	Condiments	\N	\N
2016-0011	Rin	Okumura	AC- Head	AccCenter	\N	\N
2016-0012	Janno	Trajano	Dean	CNSM	Professor V	Ph.D
2016-0013	Diana	Acana	Chairman	IT-Physics	\N	Ph.D
2016-0014	Iris	Marcellones	VCAA	VCAA	\N	\N
2016-0015	Shigeo	Kageyama	Chairman	Math	\N	Ph.D
2016-0016	CNSM	Dummy ACCT	Dummy Pos	CNSM	\N	\N
\.


--
-- TOC entry 2214 (class 0 OID 65566)
-- Dependencies: 178
-- Data for Name: equipment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY equipment (equip_id, description, unit, unit_price, equip_type, equip_brand, date_of_update) FROM stdin;
\.


--
-- TOC entry 2215 (class 0 OID 65569)
-- Dependencies: 179
-- Data for Name: iar_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY iar_items (iarnum, stocknum, unit, description, quantity, compstat, compdate, workstat, workdate) FROM stdin;
\.


--
-- TOC entry 2216 (class 0 OID 65572)
-- Dependencies: 180
-- Data for Name: insp_and_accept_report; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY insp_and_accept_report (iarnum, supplier, ponum, reqoff, podate, recieptnum, recieptdate, insstatus, insdate, insofficer, isitemcomplete, partialquan, receivedate, receiveofficer) FROM stdin;
\.


--
-- TOC entry 2217 (class 0 OID 65578)
-- Dependencies: 181
-- Data for Name: inventory; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY inventory (invnum, parnum, description, unit, unitprice, status) FROM stdin;
\.


--
-- TOC entry 2218 (class 0 OID 65581)
-- Dependencies: 182
-- Data for Name: keypositions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY keypositions (id, empid) FROM stdin;
vcaa	\N
chancelor	2013-0214
vcaf	2013-0215
\.


--
-- TOC entry 2229 (class 0 OID 73747)
-- Dependencies: 193
-- Data for Name: log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY log (logid, idnum, accttype, datetimeloggoed) FROM stdin;
HLHi-8036	2013-0211	4	\N
QPgm-0253	2013-0213	2	\N
UmMC-3611	2016-0012	4	\N
jfOL-5493	2013-0215	1	\N
UBel-1330	2013-0214	1	\N
IujA-6731	2013-0213	2	\N
tUcu-8016	2016-0012	4	\N
TCMX-5215	2013-0211	4	\N
wtAi-8050	2016-0012	4	\N
OqIN-2657	2013-0215	1	\N
skrB-4350	2013-0214	1	\N
WkQX-2448	2013-0213	2	\N
HYgB-0986	2013-0211	4	\N
Qwop-3968	2013-0215	1	\N
yaOk-6402	2013-0214	1	\N
htoT-5611	2013-0213	2	\N
axby-4900	2013-0211	4	\N
BEwb-4563	2013-0215	1	\N
mtFK-0971	2013-0214	1	\N
KYBP-9585	2013-0213	2	\N
ywJE-5848	2013-0211	4	\N
yjFY-9296	2013-0213	2	\N
OVPT-4689	2013-0215	1	\N
Bxhs-9769	2013-0211	4	\N
VxFy-7779	2013-0211	4	\N
rVif-9026	2013-0215	1	\N
BMLW-6342	2013-0214	1	\N
cJHN-6686	2013-0213	2	\N
FQOd-3998	2013-0211	4	\N
EfHp-9104	2013-0215	1	\N
HnFz-7042	2013-0213	2	\N
ifen-3416	2013-0211	4	\N
NcSB-4760	2013-0212	3	\N
NtQB-7198	2013-0211	4	\N
nAGi-8862	2013-0213	2	\N
lAPt-3442	2013-0211	4	\N
\.


--
-- TOC entry 2230 (class 0 OID 73752)
-- Dependencies: 194
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY notifications (notifnum, fromid, toid, status, priority, notifref, details, dateofnotif, timeofnotif, type, reftype) FROM stdin;
VXDP-3114	2013-0211	2013-0215	t	1	XGkk-6170	{3,4,"From: Silver, Swan","Total cost: 151782.0","You have a new Purchase Request"}	2017-02-13	10:37:00	1	pr
ZZoe-2441	2013-0214	2016-0002	f	1	XGkk-6170	{3,4,"","","New Approved Request is waiting to be Numbered"}	2017-02-13	10:38:00	2	pr
ZlbG-2467	2013-0211	2013-0214	t	1	XGkk-6170	{3,4,"From: Silver, Swan","Total cost: 151782.0","You have a new Purchase Request"}	2017-02-13	10:37:00	1	pr
nDIh-4340		2013-0211	f	1	XGkk-6170	{1,1,"Date of Req.: February 02, 2017","PR no.: XGkk-6170","Your Purchase Request was Approved"}	2017-02-13	10:55:00	2	pr
PwPK-3327	2013-0211	2013-0215	t	1	JpUS-4446	{3,4,"From: Silver, Swan","Total cost: 75000.0","You have a new Purchase Request"}	2017-02-13	10:57:00	1	pr
SfbJ-0319	2013-0214	2016-0002	f	1	JpUS-4446	{3,4,"","","New Approved Request is waiting to be Numbered"}	2017-02-13	10:57:00	2	pr
yLXb-9659	2013-0211	2013-0214	t	1	JpUS-4446	{3,4,"From: Silver, Swan","Total cost: 75000.0","You have a new Purchase Request"}	2017-02-13	10:57:00	1	pr
hnGS-0020	2013-0211	2013-0215	t	1	xWVu-1634	{3,4,"From: Silver, Swan","Total cost: 1845000.0","You have a new Purchase Request"}	2017-02-13	14:31:00	1	pr
XIjV-7493	2013-0214	2016-0002	f	1	xWVu-1634	{3,4,"","","New Approved Request is waiting to be Numbered"}	2017-02-13	14:32:00	2	pr
Qvjz-3018	2013-0211	2013-0214	t	1	xWVu-1634	{3,4,"From: Silver, Swan","Total cost: 1845000.0","You have a new Purchase Request"}	2017-02-13	14:31:00	1	pr
IXGM-9670		2013-0211	f	1	xWVu-1634	{1,1,"","PR no.: 1234","Your Purchase Request was Approved"}	2017-02-13	14:32:00	2	pr
raqc-0046		2013-0211	f	1	xWVu-1634	{1,1,"","PR no.: ","Your Purchase Request was Approved"}	2017-02-13	14:34:00	2	pr
EDRd-3946	2013-0214	2013-0213	t	1	xWVu-1634	{3,4,"","","New Approved Request is waiting to be Numbered"}	2017-02-13	14:32:00	2	pr
wOoj-5152		2013-0211	f	1	XGkk-6170	{1,1,"","PR no.: 12333","Your Purchase Request was Approved"}	2017-02-13	14:34:00	2	pr
CnuI-1662	2013-0214	2013-0213	t	1	XGkk-6170	{3,4,"","","New Approved Request is waiting to be Numbered"}	2017-02-13	10:38:00	2	pr
HMYl-3429		2013-0211	f	1	JpUS-4446	{1,1,"","PR no.: 12544","Your Purchase Request was Approved"}	2017-02-13	14:35:00	2	pr
mlDT-5457	2013-0214	2013-0213	t	1	JpUS-4446	{3,4,"","","New Approved Request is waiting to be Numbered"}	2017-02-13	10:57:00	2	pr
\.


--
-- TOC entry 2219 (class 0 OID 65593)
-- Dependencies: 183
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
\.


--
-- TOC entry 2220 (class 0 OID 65596)
-- Dependencies: 184
-- Data for Name: physical_count; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY physical_count  FROM stdin;
\.


--
-- TOC entry 2221 (class 0 OID 65599)
-- Dependencies: 185
-- Data for Name: property_acc_receipt; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY property_acc_receipt  FROM stdin;
\.


--
-- TOC entry 2222 (class 0 OID 65602)
-- Dependencies: 186
-- Data for Name: purchase_order; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY purchase_order (ponum, supplier, address, tin, datecreated, procmode, dateofdelivery, placeofdelivery, deliveryterm, paymentterm, amount, status, deliverystatus, paymentstatus) FROM stdin;
\.


--
-- TOC entry 2223 (class 0 OID 65608)
-- Dependencies: 187
-- Data for Name: purchase_order_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY purchase_order_items (ponum, itemnum, quantity, unit, description, unitcost) FROM stdin;
\.


--
-- TOC entry 2231 (class 0 OID 73760)
-- Dependencies: 195
-- Data for Name: purchase_request; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY purchase_request (reqnum, prnum, purpose, purpose_details, requester_id, date_created, status, init_approval_status, approval_status, declinereason) FROM stdin;
kGhH=5241	1234	Test		2013-2011	2016-12-06	\N	t	t	\N
xWVu-1634		Char lang		2013-0211	2017-02-13	\N	t	t	\N
XGkk-6170	12333	ffffffff		2013-0211	2017-02-13	\N	t	t	\N
JpUS-4446	12544	Test Only		2013-0211	2017-02-13	\N	t	t	\N
\.


--
-- TOC entry 2232 (class 0 OID 73768)
-- Dependencies: 196
-- Data for Name: purchase_request_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY purchase_request_items (reqnum, stock_num, description, unit, unit_price, quantity) FROM stdin;
XGkk-6170	1	fffff	ffff	1234	123
JpUS-4446	1	Test	Test	15000	5
xWVu-1634	1	TEst	TEst	15000	123
\.


--
-- TOC entry 2224 (class 0 OID 65620)
-- Dependencies: 188
-- Data for Name: req_for_quotation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY req_for_quotation (quotationnum, refnum, projname, projlocation, datecreated, canvasser) FROM stdin;
\.


--
-- TOC entry 2251 (class 0 OID 81926)
-- Dependencies: 215
-- Data for Name: req_for_quotation_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY req_for_quotation_items (quotationnum, itemnum, description, quantity, unit, unitprice) FROM stdin;
\.


--
-- TOC entry 2250 (class 0 OID 81920)
-- Dependencies: 214
-- Data for Name: req_for_quotation_suppliers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY req_for_quotation_suppliers (quotationnum, compid, warrantyper, delperiod, pricevalidity) FROM stdin;
\.


--
-- TOC entry 2252 (class 0 OID 81929)
-- Dependencies: 216
-- Data for Name: suppliers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY suppliers (compid, name, address, comprep, reptel, repemail, comptin) FROM stdin;
\.


--
-- TOC entry 2225 (class 0 OID 65629)
-- Dependencies: 189
-- Data for Name: test; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY test (c) FROM stdin;
{ee,erer,elo}
{rtr,ee,szx}
\.


--
-- TOC entry 2226 (class 0 OID 65635)
-- Dependencies: 190
-- Data for Name: transactions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY transactions  FROM stdin;
\.


--
-- TOC entry 2227 (class 0 OID 65638)
-- Dependencies: 191
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY users (uname, pass, idnum, access_type, profile_pic, status) FROM stdin;
kem1101231	condigago	\N	\N	\N	\N
requi	pass	2013-0211	{4}	\N	t
smoadmin	pass	2013-0212	{3}	\N	t
procadmin	pass	2013-0213	{2}	\N	\N
approv	pass	2013-0214	{1}	\N	\N
gin1101	haaaaa	2016-0002	{2}	\N	t
zura1101	zurajanaikatsurada	2016-0001	{3}	\N	t
ora220	umoshereze	2016-0003	{4}	\N	\N
sharingan	obito	2016-0004	{1}	\N	\N
kem1101	condigago	2011-0813	{0}	\N	\N
init_approv	pass	2013-0215	{1}	\N	t
kem1101233	condigago	\N	\N	\N	\N
cnsm	deanlogin	2016-0012	{4}	\N	t
\.


--
-- TOC entry 2228 (class 0 OID 65644)
-- Dependencies: 192
-- Data for Name: waste_mat_report; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY waste_mat_report  FROM stdin;
\.


--
-- TOC entry 2012 (class 2606 OID 65649)
-- Name: abstract_of_canvass_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY abstract_of_canvass
    ADD CONSTRAINT abstract_of_canvass_pkey PRIMARY KEY (canvassnum);


--
-- TOC entry 2052 (class 2606 OID 73798)
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- TOC entry 2058 (class 2606 OID 73853)
-- Name: auth_group_permissions_group_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- TOC entry 2060 (class 2606 OID 73806)
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 2054 (class 2606 OID 73796)
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- TOC entry 2047 (class 2606 OID 73839)
-- Name: auth_permission_content_type_id_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- TOC entry 2049 (class 2606 OID 73788)
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- TOC entry 2069 (class 2606 OID 73824)
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- TOC entry 2071 (class 2606 OID 73868)
-- Name: auth_user_groups_user_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- TOC entry 2062 (class 2606 OID 73814)
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- TOC entry 2075 (class 2606 OID 73832)
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 2077 (class 2606 OID 73882)
-- Name: auth_user_user_permissions_user_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- TOC entry 2065 (class 2606 OID 73910)
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- TOC entry 2014 (class 2606 OID 65651)
-- Name: college_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY college
    ADD CONSTRAINT college_pkey PRIMARY KEY (id);


--
-- TOC entry 2081 (class 2606 OID 73896)
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- TOC entry 2042 (class 2606 OID 73780)
-- Name: django_content_type_app_label_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- TOC entry 2044 (class 2606 OID 73778)
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- TOC entry 2016 (class 2606 OID 65653)
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- TOC entry 2084 (class 2606 OID 73922)
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- TOC entry 2018 (class 2606 OID 65655)
-- Name: employees_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (idnum);


--
-- TOC entry 2020 (class 2606 OID 65657)
-- Name: equipment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY equipment
    ADD CONSTRAINT equipment_pkey PRIMARY KEY (equip_id);


--
-- TOC entry 2022 (class 2606 OID 65659)
-- Name: insp_and_accept_report_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY insp_and_accept_report
    ADD CONSTRAINT insp_and_accept_report_pkey PRIMARY KEY (iarnum);


--
-- TOC entry 2024 (class 2606 OID 65661)
-- Name: inventory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY inventory
    ADD CONSTRAINT inventory_pkey PRIMARY KEY (invnum);


--
-- TOC entry 2026 (class 2606 OID 65663)
-- Name: keypositions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY keypositions
    ADD CONSTRAINT keypositions_pkey PRIMARY KEY (id);


--
-- TOC entry 2036 (class 2606 OID 73751)
-- Name: log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY log
    ADD CONSTRAINT log_pkey PRIMARY KEY (logid);


--
-- TOC entry 2038 (class 2606 OID 73759)
-- Name: notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (notifnum);


--
-- TOC entry 2028 (class 2606 OID 65690)
-- Name: offices_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY offices
    ADD CONSTRAINT offices_pkey PRIMARY KEY (id);


--
-- TOC entry 2030 (class 2606 OID 65671)
-- Name: purchase_order_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY purchase_order
    ADD CONSTRAINT purchase_order_pkey PRIMARY KEY (ponum);


--
-- TOC entry 2040 (class 2606 OID 73767)
-- Name: purchase_request_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY purchase_request
    ADD CONSTRAINT purchase_request_pkey PRIMARY KEY (reqnum);


--
-- TOC entry 2032 (class 2606 OID 65675)
-- Name: req_for_quotation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY req_for_quotation
    ADD CONSTRAINT req_for_quotation_pkey PRIMARY KEY (quotationnum);


--
-- TOC entry 2087 (class 2606 OID 81936)
-- Name: suppliers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY suppliers
    ADD CONSTRAINT suppliers_pkey PRIMARY KEY (compid);


--
-- TOC entry 2034 (class 2606 OID 65677)
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (uname);


--
-- TOC entry 2050 (class 1259 OID 73841)
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_group_name_a6ea08ec_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- TOC entry 2055 (class 1259 OID 73854)
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_group_permissions_0e939a4f ON auth_group_permissions USING btree (group_id);


--
-- TOC entry 2056 (class 1259 OID 73855)
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_group_permissions_8373b171 ON auth_group_permissions USING btree (permission_id);


--
-- TOC entry 2045 (class 1259 OID 73840)
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_permission_417f1b1c ON auth_permission USING btree (content_type_id);


--
-- TOC entry 2066 (class 1259 OID 73870)
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_groups_0e939a4f ON auth_user_groups USING btree (group_id);


--
-- TOC entry 2067 (class 1259 OID 73869)
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_groups_e8701ad4 ON auth_user_groups USING btree (user_id);


--
-- TOC entry 2072 (class 1259 OID 73884)
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_8373b171 ON auth_user_user_permissions USING btree (permission_id);


--
-- TOC entry 2073 (class 1259 OID 73883)
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON auth_user_user_permissions USING btree (user_id);


--
-- TOC entry 2063 (class 1259 OID 73911)
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_username_6821ab7c_like ON auth_user USING btree (username varchar_pattern_ops);


--
-- TOC entry 2078 (class 1259 OID 73907)
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX django_admin_log_417f1b1c ON django_admin_log USING btree (content_type_id);


--
-- TOC entry 2079 (class 1259 OID 73908)
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX django_admin_log_e8701ad4 ON django_admin_log USING btree (user_id);


--
-- TOC entry 2082 (class 1259 OID 73923)
-- Name: django_session_de54fa62; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX django_session_de54fa62 ON django_session USING btree (expire_date);


--
-- TOC entry 2085 (class 1259 OID 73924)
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX django_session_session_key_c0390e0f_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- TOC entry 2088 (class 2606 OID 65678)
-- Name: abstract_of_canvass_supplier_price_canvassnum_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY abstract_of_canvass_supplier_price
    ADD CONSTRAINT abstract_of_canvass_supplier_price_canvassnum_fkey FOREIGN KEY (canvassnum) REFERENCES abstract_of_canvass(canvassnum);


--
-- TOC entry 2092 (class 2606 OID 73847)
-- Name: auth_group_permiss_permission_id_84c5c92e_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permiss_permission_id_84c5c92e_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2091 (class 2606 OID 73842)
-- Name: auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2090 (class 2606 OID 73833)
-- Name: auth_permiss_content_type_id_2f476e4b_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permiss_content_type_id_2f476e4b_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2094 (class 2606 OID 73862)
-- Name: auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2093 (class 2606 OID 73857)
-- Name: auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2096 (class 2606 OID 73876)
-- Name: auth_user_user_per_permission_id_1fbb5f2c_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_per_permission_id_1fbb5f2c_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2095 (class 2606 OID 73871)
-- Name: auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2097 (class 2606 OID 73897)
-- Name: django_admin_content_type_id_c4bce8eb_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_content_type_id_c4bce8eb_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2098 (class 2606 OID 73902)
-- Name: django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2089 (class 2606 OID 65683)
-- Name: req_for_quotation_quotationnum_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY req_for_quotation
    ADD CONSTRAINT req_for_quotation_quotationnum_fkey FOREIGN KEY (quotationnum) REFERENCES req_for_quotation(quotationnum);


--
-- TOC entry 2259 (class 0 OID 0)
-- Dependencies: 6
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2017-02-16 13:26:55

--
-- PostgreSQL database dump complete
--

