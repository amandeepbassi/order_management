PGDMP     0                    x            ordermgt     12.3 (Ubuntu 12.3-1.pgdg20.04+1)     12.3 (Ubuntu 12.3-1.pgdg20.04+1)     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    24595    ordermgt    DATABASE     n   CREATE DATABASE ordermgt WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_IN' LC_CTYPE = 'en_IN';
    DROP DATABASE ordermgt;
                postgres    false            �            1259    24596 	   orderbook    TABLE     �   CREATE TABLE public.orderbook (
    id integer NOT NULL,
    customer_id integer NOT NULL,
    datetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP(2) NOT NULL
);
    DROP TABLE public.orderbook;
       public         heap    postgres    false            �            1259    24603    order book_id_seq    SEQUENCE     �   CREATE SEQUENCE public."order book_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public."order book_id_seq";
       public          postgres    false    202            �           0    0    order book_id_seq    SEQUENCE OWNED BY     H   ALTER SEQUENCE public."order book_id_seq" OWNED BY public.orderbook.id;
          public          postgres    false    203            �            1259    24605    order_details    TABLE     ~   CREATE TABLE public.order_details (
    order_id integer NOT NULL,
    details json,
    order_details_id integer NOT NULL
);
 !   DROP TABLE public.order_details;
       public         heap    postgres    false            �            1259    24611    order_details_id_seq    SEQUENCE     �   CREATE SEQUENCE public.order_details_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.order_details_id_seq;
       public          postgres    false    204            �           0    0    order_details_id_seq    SEQUENCE OWNED BY     [   ALTER SEQUENCE public.order_details_id_seq OWNED BY public.order_details.order_details_id;
          public          postgres    false    205            �            1259    32783    status    TABLE     �   CREATE TABLE public.status (
    order_id2 integer,
    status text,
    date date DEFAULT CURRENT_DATE NOT NULL,
    "time" time without time zone DEFAULT CURRENT_TIME NOT NULL,
    status_id integer NOT NULL
);
    DROP TABLE public.status;
       public         heap    postgres    false                       2604    24613    order_details order_details_id    DEFAULT     �   ALTER TABLE ONLY public.order_details ALTER COLUMN order_details_id SET DEFAULT nextval('public.order_details_id_seq'::regclass);
 M   ALTER TABLE public.order_details ALTER COLUMN order_details_id DROP DEFAULT;
       public          postgres    false    205    204                       2604    24614    orderbook id    DEFAULT     o   ALTER TABLE ONLY public.orderbook ALTER COLUMN id SET DEFAULT nextval('public."order book_id_seq"'::regclass);
 ;   ALTER TABLE public.orderbook ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    203    202            �          0    24605    order_details 
   TABLE DATA           L   COPY public.order_details (order_id, details, order_details_id) FROM stdin;
    public          postgres    false    204   �       �          0    24596 	   orderbook 
   TABLE DATA           >   COPY public.orderbook (id, customer_id, datetime) FROM stdin;
    public          postgres    false    202   T       �          0    32783    status 
   TABLE DATA           L   COPY public.status (order_id2, status, date, "time", status_id) FROM stdin;
    public          postgres    false    206   �       �           0    0    order book_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public."order book_id_seq"', 1, true);
          public          postgres    false    203            �           0    0    order_details_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.order_details_id_seq', 46, true);
          public          postgres    false    205            !           2606    24616    orderbook order book_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.orderbook
    ADD CONSTRAINT "order book_pkey" PRIMARY KEY (id);
 E   ALTER TABLE ONLY public.orderbook DROP CONSTRAINT "order book_pkey";
       public            postgres    false    202            $           2606    24618     order_details order_details_pkey 
   CONSTRAINT     l   ALTER TABLE ONLY public.order_details
    ADD CONSTRAINT order_details_pkey PRIMARY KEY (order_details_id);
 J   ALTER TABLE ONLY public.order_details DROP CONSTRAINT order_details_pkey;
       public            postgres    false    204            '           2606    32790    status status_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public.status
    ADD CONSTRAINT status_pkey PRIMARY KEY (status_id);
 <   ALTER TABLE ONLY public.status DROP CONSTRAINT status_pkey;
       public            postgres    false    206            "           1259    24619    fki_order_id_to_order_book_id    INDEX     [   CREATE INDEX fki_order_id_to_order_book_id ON public.order_details USING btree (order_id);
 1   DROP INDEX public.fki_order_id_to_order_book_id;
       public            postgres    false    204            %           1259    32796    fki_order_id_to_order_id_2    INDEX     R   CREATE INDEX fki_order_id_to_order_id_2 ON public.status USING btree (order_id2);
 .   DROP INDEX public.fki_order_id_to_order_id_2;
       public            postgres    false    206            (           2606    24620 '   order_details order_id_to_order_book_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.order_details
    ADD CONSTRAINT order_id_to_order_book_id FOREIGN KEY (order_id) REFERENCES public.orderbook(id) NOT VALID;
 Q   ALTER TABLE ONLY public.order_details DROP CONSTRAINT order_id_to_order_book_id;
       public          postgres    false    204    202    2849            )           2606    32791    status order_id_to_order_id_2    FK CONSTRAINT     �   ALTER TABLE ONLY public.status
    ADD CONSTRAINT order_id_to_order_id_2 FOREIGN KEY (order_id2) REFERENCES public.orderbook(id) NOT VALID;
 G   ALTER TABLE ONLY public.status DROP CONSTRAINT order_id_to_order_id_2;
       public          postgres    false    202    2849    206            �   T   x�31�V*(�O)M.Q�RP�4P�Q 
d&���F ^aib^IfI%P����Ę�Č$MF@M&\&樚�	k2�2� �&3�=... ��9�      �   @   x�uɹ� �������Aj��:��æ98LM��$�۞�D���6�lD]n}חk���]�      �   _   x�}�;� �z�.������ F�7�x~?��SJ����}N1R�+4�� 	���H3J��8~��Fm�#�.���}g����	n3_�%_     