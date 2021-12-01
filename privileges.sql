--867
SELECT pgd.datname as database_name, pgu.usename as user_name, array_to_string(array(select privs from unnest(ARRAY[
(CASE WHEN has_database_privilege(pgu.usename,pgd.oid,'CREATE') THEN 'CREATE' ELSE NULL END),
(CASE WHEN has_database_privilege(pgu.usename,pgd.oid,'TEMPORARY, TEMP') THEN 'TEMPORARY' ELSE NULL END),
(CASE WHEN has_database_privilege(pgu.usename,pgd.oid,'CONNECT') THEN 'CONNECT' ELSE NULL END)])foo(privs) WHERE privs IS NOT NULL), ', ')
as permissions,

array_to_string(array(select privs from unnest(ARRAY[
(CASE WHEN pgr.rolcanlogin THEN 'CAN LOGIN' ELSE NULL END),
(CASE WHEN pgr.rolsuper THEN 'SUPERUSER' ELSE NULL END),
(CASE WHEN pgr.rolcreaterole THEN 'CREATE ROLE' ELSE NULL END),
(CASE WHEN pgr.rolcreatedb THEN 'CREATE DATABASES' ELSE NULL END),
(CASE WHEN pgr.rolinherit THEN 'INHERIT RIGHTS FROM THE PARENT ROLES' ELSE NULL END),
(CASE WHEN pgr.rolreplication THEN 'CAN INITIATE STREAMING REPLICATION AND BACKUPS' ELSE NULL END)])foo(privs) WHERE privs IS NOT NULL), ', ')
as privileges,


array_to_string(array(select privs from unnest(ARRAY[
(CASE WHEN pgu.usename like '%_usr' THEN 'GRANT CONNECT, CREATE, TEMPORARY ON DATABASE' ELSE NULL END),
(CASE WHEN pgu.usename like '%_read' THEN 'GRANT CONNECT ON DATABASE, GRANT USAGE ON SCHEMA ent_alumni and GRANT SELECT ON ALL TABLES IN SCHEMA ent_alumni' ELSE NULL END),
(CASE WHEN pgu.usename like '%_admin' THEN 'GRANT CONNECT, CREATE, TEMPORARY ON DATABASE, GRANT USAGE, CREATE ON SCHEMA ent_alumni, GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA ent_alumni and GRANT USAGE ON ALL SEQUENCES IN SCHEMA ent_alumni' ELSE NULL END)])foo(privs) WHERE privs IS NOT NULL), ', ')
as role_attribute

FROM pg_database pgd, pg_user pgu, pg_roles pgr
WHERE pgu.usename != 'rdsadmin' and
--pgd.datname = 'alumni_yourcorp' and
not pgd.datistemplate and
has_database_privilege(pgu.usename,pgd.oid,'CONNECT,CREATE,TEMPORARY,TEMP')
and pgu.usename = pgr.rolname
order by 1,2;




--*************************************************************************************--


select pgu.usename as user_name,
       (select string_agg(pgd.datname, ',' order by pgd.datname) 
        from pg_database pgd 
        where has_database_privilege(pgu.usename, pgd.datname, 'CREATE')) as database_name
from pg_user pgu
order by pgu.usename;

select pgd.datname as database_name, pgu.usename as user_name, 
case
when has_database_privilege(pgu.usename, pgd.datname, 'CREATE')
and  has_database_privilege(pgu.usename, pgd.datname, 'TEMPORARY')
and  has_database_privilege(pgu.usename, pgd.datname, ' CONNECT') then
'ALL, CREATE, TEMPORARY, CONNECT'

when has_database_privilege(pgu.usename, pgd.datname, 'CREATE')
and  has_database_privilege(pgu.usename, pgd.datname, 'TEMPORARY')then
'CREATE, TEMPORARY'

when has_database_privilege(pgu.usename, pgd.datname, 'CREATE')
and  has_database_privilege(pgu.usename, pgd.datname, ' CONNECT') then
'CREATE, CONNECT'

when has_database_privilege(pgu.usename, pgd.datname, 'TEMPORARY')
and  has_database_privilege(pgu.usename, pgd.datname, ' CONNECT') then
'TEMPORARY, CONNECT'

when has_database_privilege(pgu.usename, pgd.datname, 'CREATE') then
'CREATE'
when  has_database_privilege(pgu.usename, pgd.datname, 'TEMPORARY') then
'TEMPORARY'
when  has_database_privilege(pgu.usename, pgd.datname, ' CONNECT') then
'CONNECT'

end
as permissions
from pg_user pgu, pg_database pgd
where pgu.usename != 'rdsadmin' and
pgd.datname = 'alumni_yourcorp' and
not pgd.datistemplate and
(has_database_privilege(pgu.usename, pgd.datname, 'CREATE')
or has_database_privilege(pgu.usename, pgd.datname, 'TEMPORARY')
or has_database_privilege(pgu.usename, pgd.datname, ' CONNECT'))
order by 1, 2;






--********************************************************************--
SELECT d.datname as "Name",
   pg_catalog.pg_get_userbyid(d.datdba) as "Owner",
   pg_catalog.pg_encoding_to_char(d.encoding) as "Encoding",
   d.datcollate as "Collate",
   d.datctype as "Ctype",
   pg_catalog.array_to_string(d.datacl, E'\n') AS "Access privileges"
FROM pg_catalog.pg_database d
where d.datname = 'alumni_yourcorp'
ORDER BY 1;


--********************************************************************--
select pg_get_userbyid(d.defaclrole) as user, n.nspname as schema, 
case d.defaclobjtype when 'r' then 'tables' when 'f' then 'functions' end as object_type,
array_to_string(d.defaclacl, ' + ')  as default_privileges 
from pg_catalog.pg_default_acl d 
left join pg_catalog.pg_namespace n on n.oid = d.defaclnamespace;
