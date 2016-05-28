--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.2
-- Dumped by pg_dump version 9.5.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: contacts; Type: TABLE; Schema: public; Owner: alyon
--

CREATE TABLE contacts (
    user_id integer NOT NULL,
    contact_id integer NOT NULL,
    first_name character varying(64) NOT NULL,
    last_name character varying(64),
    email character varying(128),
    cell_phone character varying(12),
    street character varying(256),
    city character varying(64),
    state character varying(2),
    zipcode character varying(5),
    total_frienergy double precision,
    avg_t_btwn_ints double precision,
    t_since_last_int integer
);


ALTER TABLE contacts OWNER TO alyon;

--
-- Name: contacts_contact_id_seq; Type: SEQUENCE; Schema: public; Owner: alyon
--

CREATE SEQUENCE contacts_contact_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE contacts_contact_id_seq OWNER TO alyon;

--
-- Name: contacts_contact_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: alyon
--

ALTER SEQUENCE contacts_contact_id_seq OWNED BY contacts.contact_id;


--
-- Name: interactions; Type: TABLE; Schema: public; Owner: alyon
--

CREATE TABLE interactions (
    interaction_id integer NOT NULL,
    contact_id integer NOT NULL,
    user_id integer NOT NULL,
    date date NOT NULL,
    frienergy integer NOT NULL,
    t_delta_since_last_int integer
);


ALTER TABLE interactions OWNER TO alyon;

--
-- Name: interactions_interaction_id_seq; Type: SEQUENCE; Schema: public; Owner: alyon
--

CREATE SEQUENCE interactions_interaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE interactions_interaction_id_seq OWNER TO alyon;

--
-- Name: interactions_interaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: alyon
--

ALTER SEQUENCE interactions_interaction_id_seq OWNED BY interactions.interaction_id;


--
-- Name: notes; Type: TABLE; Schema: public; Owner: alyon
--

CREATE TABLE notes (
    note_id integer NOT NULL,
    contact_id integer NOT NULL,
    interaction_id integer NOT NULL,
    text text NOT NULL
);


ALTER TABLE notes OWNER TO alyon;

--
-- Name: notes_note_id_seq; Type: SEQUENCE; Schema: public; Owner: alyon
--

CREATE SEQUENCE notes_note_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE notes_note_id_seq OWNER TO alyon;

--
-- Name: notes_note_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: alyon
--

ALTER SEQUENCE notes_note_id_seq OWNED BY notes.note_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: alyon
--

CREATE TABLE users (
    user_id integer NOT NULL,
    first_name character varying(32) NOT NULL,
    last_name character varying(32) NOT NULL,
    email character varying(64) NOT NULL,
    password character varying(64) NOT NULL,
    zipcode character varying(15)
);


ALTER TABLE users OWNER TO alyon;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: alyon
--

CREATE SEQUENCE users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_user_id_seq OWNER TO alyon;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: alyon
--

ALTER SEQUENCE users_user_id_seq OWNED BY users.user_id;


--
-- Name: contact_id; Type: DEFAULT; Schema: public; Owner: alyon
--

ALTER TABLE ONLY contacts ALTER COLUMN contact_id SET DEFAULT nextval('contacts_contact_id_seq'::regclass);


--
-- Name: interaction_id; Type: DEFAULT; Schema: public; Owner: alyon
--

ALTER TABLE ONLY interactions ALTER COLUMN interaction_id SET DEFAULT nextval('interactions_interaction_id_seq'::regclass);


--
-- Name: note_id; Type: DEFAULT; Schema: public; Owner: alyon
--

ALTER TABLE ONLY notes ALTER COLUMN note_id SET DEFAULT nextval('notes_note_id_seq'::regclass);


--
-- Name: user_id; Type: DEFAULT; Schema: public; Owner: alyon
--

ALTER TABLE ONLY users ALTER COLUMN user_id SET DEFAULT nextval('users_user_id_seq'::regclass);


--
-- Data for Name: contacts; Type: TABLE DATA; Schema: public; Owner: alyon
--

COPY contacts (user_id, contact_id, first_name, last_name, email, cell_phone, street, city, state, zipcode, total_frienergy, avg_t_btwn_ints, t_since_last_int) FROM stdin;
4	29	Allison								3	0	0
1	13	Chuck	Bonnici		415-860-9344					64	6.22222222222222232	0
1	12	Kristine	Chou		808-342-1680					2	3	15
1	18	Lizzy	Gilman							4	0	24
1	23	Joyce	Lin							8	0	15
1	17	Karl	Gummerlock		650-704-6324					16	8.33333333333333393	10
1	8	Daniel	Feeny			607 Mountain Home Rd	Woodside	CA	94062	10	14	7
1	2	Christina	Clarkin	cristinamclarkin@gmail.com	201-887-1119					13	17	5
1	27	Sharon	Weinnbar							3	0	5
1	28	Eric								8	0	5
1	7	Christina	Feeny	christina@feenys.net	650-380-0666	607 Mountain Home Rd	Woodside	CA	94062	41	5.36363636363636331	4
1	31	Holly	Still			530 Bay Rd. 	Menlo Park	CA	94025	4	0	2
1	10	Jaime	Lyon	lyon.jaime@gmail.com	510-725-2135	235 Walter Hays Dr.	Palo Alto	CA	94303	38	2.11111111111111116	1
1	4	Katie	Simmons	katie@katie.codes	651-361-0974					31	3.66666666666666652	1
1	21	Aisling	Dempsey	aisling.n.dempsey@gmail.com	415-470-3073		San Francisco			25	2.66666666666666652	1
1	6	Veronica	Erik	veronica@ellenblakeley.com	707-696-0691					26	4.20000000000000018	1
1	25	Inas	Hyatt	inas.raheema@gmail.com						14	3.5	1
1	9	Curtis	Feeny	curtis@feenys.net		607 Mountain Home Rd	Woodside	CA	94062	27	8.71428571428571352	2
1	11	Hilary	Jones	hilarypjones@yahoo.com	650-326-8232	235 Walter Hays Dr.	Palo Alto	CA	94303	8	11	4
1	5	Sarah	Flemming	sajafleming@gmail.com	314-750-4493					10	10.5	1
1	3	Katie 	Lundsgard	katie.lundsgaard@gmail.com						11	10.5	1
1	24	Maggie	Yang							8	14	1
1	30	Aiden	Ward							6	1	1
1	1	Anna	Kiefer	annakiefer12@gmail.com	301-536-3989					18	3.5	1
\.


--
-- Name: contacts_contact_id_seq; Type: SEQUENCE SET; Schema: public; Owner: alyon
--

SELECT pg_catalog.setval('contacts_contact_id_seq', 31, true);


--
-- Data for Name: interactions; Type: TABLE DATA; Schema: public; Owner: alyon
--

COPY interactions (interaction_id, contact_id, user_id, date, frienergy, t_delta_since_last_int) FROM stdin;
25	1	1	2016-05-06	8	0
26	2	1	2016-05-06	8	0
27	3	1	2016-05-06	5	0
46	4	1	2016-05-05	9	0
28	5	1	2016-05-06	7	0
29	6	1	2016-05-06	7	0
1	7	1	2016-03-26	6	0
5	7	1	2016-04-04	2	9
8	7	1	2016-04-10	3	6
9	7	1	2016-04-11	4	1
11	7	1	2016-04-14	5	3
12	7	1	2016-04-21	4	7
13	7	1	2016-04-23	2	2
18	7	1	2016-05-02	4	9
31	7	1	2016-05-07	2	5
43	7	1	2016-05-11	5	4
3	8	1	2016-03-26	2	0
14	8	1	2016-04-23	1	28
37	8	1	2016-05-10	2	17
45	8	1	2016-05-11	2	1
2	9	1	2016-03-26	6	0
19	9	1	2016-05-02	3	37
24	9	1	2016-05-05	2	3
32	9	1	2016-05-08	3	3
34	9	1	2016-05-09	5	1
44	9	1	2016-05-11	2	2
33	10	1	2016-05-08	1	0
35	10	1	2016-05-09	2	1
38	10	1	2016-05-10	6	1
20	11	1	2016-05-02	3	0
39	11	1	2016-05-10	3	8
40	12	1	2016-05-10	1	0
4	13	1	2016-04-02	8	0
6	13	1	2016-04-04	8	2
7	13	1	2016-04-06	8	2
10	13	1	2016-04-13	7	7
16	13	1	2016-04-25	4	12
17	13	1	2016-04-30	10	5
21	13	1	2016-05-02	7	2
41	13	1	2016-05-10	9	8
15	17	1	2016-04-23	4	0
22	17	1	2016-05-02	3	9
42	17	1	2016-05-10	3	8
23	18	1	2016-05-04	4	0
50	21	1	2016-05-12	3	1
51	1	1	2016-05-12	1	6
52	12	1	2016-05-13	1	3
53	4	1	2016-05-13	9	8
49	21	1	2016-05-11	7	0
54	21	1	2016-05-13	5	1
55	1	1	2016-05-13	3	1
56	23	1	2016-05-13	8	0
57	24	1	2016-05-13	7	0
59	10	1	2016-05-15	3	4
60	21	1	2016-05-16	1	3
48	10	1	2016-05-11	4	1
58	13	1	2016-05-15	2	5
62	25	1	2016-05-13	2	0
63	6	1	2016-05-18	4	12
64	17	1	2016-05-18	6	8
65	25	1	2016-05-18	2	5
66	25	1	2016-05-18	3	0
68	5	1	2016-05-19	2	13
69	21	1	2016-05-19	1	3
70	10	1	2016-05-18	1	3
72	6	1	2016-05-20	3	2
71	25	1	2016-05-20	4	2
73	3	1	2016-05-20	2	14
75	1	1	2016-05-20	1	7
76	7	1	2016-05-20	1	9
77	1	1	2016-05-21	1	1
78	10	1	2016-05-21	6	3
79	4	1	2016-05-21	3	8
80	8	1	2016-05-21	3	10
81	2	1	2016-05-23	5	17
82	27	1	2016-05-23	3	0
83	1	1	2016-05-23	1	2
84	6	1	2016-05-23	2	3
85	4	1	2016-05-23	2	2
86	9	1	2016-05-23	3	12
87	10	1	2016-05-23	10	2
88	4	1	2016-05-23	3	0
89	28	1	2016-05-23	8	0
90	7	1	2016-05-24	3	4
91	4	1	2016-05-24	3	1
92	10	1	2016-05-24	4	1
93	6	1	2016-05-24	5	1
94	21	1	2016-05-26	4	7
95	29	4	2016-05-26	3	0
96	30	1	2016-05-26	3	0
97	31	1	2016-05-26	4	0
98	10	1	2016-05-27	1	3
99	4	1	2016-05-27	2	3
100	21	1	2016-05-27	4	1
101	6	1	2016-05-27	5	3
102	25	1	2016-05-27	3	7
103	9	1	2016-05-26	3	3
104	11	1	2016-05-24	2	14
105	5	1	2016-05-27	1	8
106	3	1	2016-05-27	4	7
107	24	1	2016-05-27	1	14
108	30	1	2016-05-27	3	1
109	1	1	2016-05-27	3	4
110	13	1	2016-05-28	1	13
\.


--
-- Name: interactions_interaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: alyon
--

SELECT pg_catalog.setval('interactions_interaction_id_seq', 110, true);


--
-- Data for Name: notes; Type: TABLE DATA; Schema: public; Owner: alyon
--

COPY notes (note_id, contact_id, interaction_id, text) FROM stdin;
1	13	17	Helped me move had lunch at Buck's
5	21	49	text
4	10	48	text msg
16	13	58	Phone call
17	25	62	Note thingy
18	6	63	Chitchat about bootstrap
19	17	64	Dinner at food trucks
20	6	72	Debugging
21	25	71	Debugging
22	10	87	Moto accident pick-up
23	29	95	Talking Websites
24	30	96	Philosophical debate
\.


--
-- Name: notes_note_id_seq; Type: SEQUENCE SET; Schema: public; Owner: alyon
--

SELECT pg_catalog.setval('notes_note_id_seq', 24, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: alyon
--

COPY users (user_id, first_name, last_name, email, password, zipcode) FROM stdin;
1	Allison	Lyon	alyoness1@gmail.com	password123	94062
2	Test	User	test@email.com	password	99999
4	Katie				
\.


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: alyon
--

SELECT pg_catalog.setval('users_user_id_seq', 4, true);


--
-- Name: contacts_pkey; Type: CONSTRAINT; Schema: public; Owner: alyon
--

ALTER TABLE ONLY contacts
    ADD CONSTRAINT contacts_pkey PRIMARY KEY (contact_id);


--
-- Name: interactions_pkey; Type: CONSTRAINT; Schema: public; Owner: alyon
--

ALTER TABLE ONLY interactions
    ADD CONSTRAINT interactions_pkey PRIMARY KEY (interaction_id);


--
-- Name: notes_pkey; Type: CONSTRAINT; Schema: public; Owner: alyon
--

ALTER TABLE ONLY notes
    ADD CONSTRAINT notes_pkey PRIMARY KEY (note_id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: alyon
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: contacts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: alyon
--

ALTER TABLE ONLY contacts
    ADD CONSTRAINT contacts_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: interactions_contact_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: alyon
--

ALTER TABLE ONLY interactions
    ADD CONSTRAINT interactions_contact_id_fkey FOREIGN KEY (contact_id) REFERENCES contacts(contact_id);


--
-- Name: interactions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: alyon
--

ALTER TABLE ONLY interactions
    ADD CONSTRAINT interactions_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: notes_contact_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: alyon
--

ALTER TABLE ONLY notes
    ADD CONSTRAINT notes_contact_id_fkey FOREIGN KEY (contact_id) REFERENCES contacts(contact_id);


--
-- Name: notes_interaction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: alyon
--

ALTER TABLE ONLY notes
    ADD CONSTRAINT notes_interaction_id_fkey FOREIGN KEY (interaction_id) REFERENCES interactions(interaction_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

