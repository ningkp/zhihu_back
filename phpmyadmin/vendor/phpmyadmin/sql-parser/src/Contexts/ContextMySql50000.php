<?php

/**
 * Context for MySQL 5.
 *
 * This file was auto-generated.
 *
 * @see https://dev.mysql.com/doc/refman/5.0/en/keywords.html
 */

namespace PhpMyAdmin\SqlParser\Contexts;

use PhpMyAdmin\SqlParser\Context;

/**
 * Context for MySQL 5.
 *
 * @category   Contexts
 *
 * @license    https://www.gnu.org/licenses/gpl-2.0.txt GPL-2.0+
 */
class ContextMySql50000 extends Context
{
    /**
     * List of keywords.
     *
     * The value associated to each keyword represents its flags.
     *
     * @see Token::FLAG_KEYWORD_*
     *
     * @var array
     */
    public static $KEYWORDS = array(
        'DO' => 1, 'IO' => 1, 'NO' => 1, 'XA' => 1,
        'ANY' => 1, 'BDB' => 1, 'CPU' => 1, 'END' => 1, 'IPC' => 1, 'NDB' => 1,
        'NEW' => 1, 'ONE' => 1, 'ROW' => 1,
        'BOOL' => 1, 'BYTE' => 1, 'CODE' => 1, 'CUBE' => 1, 'DATA' => 1, 'FAST' => 1,
        'FILE' => 1, 'FULL' => 1, 'HASH' => 1, 'HELP' => 1, 'LAST' => 1, 'LOGS' => 1,
        'MODE' => 1, 'NAME' => 1, 'NEXT' => 1, 'NONE' => 1, 'OPEN' => 1, 'PAGE' => 1,
        'PREV' => 1, 'ROWS' => 1, 'SOME' => 1, 'STOP' => 1, 'TYPE' => 1, 'VIEW' => 1,
        'WORK' => 1, 'X509' => 1,
        'AFTER' => 1, 'BEGIN' => 1, 'BLOCK' => 1, 'BTREE' => 1, 'CACHE' => 1,
        'CHAIN' => 1, 'CLOSE' => 1, 'FIRST' => 1, 'FIXED' => 1, 'FLUSH' => 1,
        'FOUND' => 1, 'HOSTS' => 1, 'LEVEL' => 1, 'LOCAL' => 1, 'LOCKS' => 1,
        'MERGE' => 1, 'MUTEX' => 1, 'NAMES' => 1, 'NCHAR' => 1, 'PHASE' => 1,
        'QUERY' => 1, 'QUICK' => 1, 'RAID0' => 1, 'RESET' => 1, 'RTREE' => 1,
        'SHARE' => 1, 'SLAVE' => 1, 'START' => 1, 'SUPER' => 1, 'SWAPS' => 1,
        'TYPES' => 1, 'UNTIL' => 1, 'VALUE' => 1,
        'ACTION' => 1, 'BACKUP' => 1, 'BINLOG' => 1, 'CIPHER' => 1, 'CLIENT' => 1,
        'COMMIT' => 1, 'ENABLE' => 1, 'ENGINE' => 1, 'ERRORS' => 1, 'ESCAPE' => 1,
        'EVENTS' => 1, 'FAULTS' => 1, 'FIELDS' => 1, 'GLOBAL' => 1, 'GRANTS' => 1,
        'IMPORT' => 1, 'INNODB' => 1, 'ISSUER' => 1, 'LEAVES' => 1, 'MASTER' => 1,
        'MEDIUM' => 1, 'MEMORY' => 1, 'MODIFY' => 1, 'OFFSET' => 1, 'RELOAD' => 1,
        'REPAIR' => 1, 'RESUME' => 1, 'ROLLUP' => 1, 'SIGNED' => 1, 'SIMPLE' => 1,
        'SOUNDS' => 1, 'SOURCE' => 1, 'STATUS' => 1, 'STRING' => 1, 'TABLES' => 1,
        'CHANGED' => 1, 'COLUMNS' => 1, 'COMMENT' => 1, 'COMPACT' => 1, 'CONTEXT' => 1,
        'DEFINER' => 1, 'DISABLE' => 1, 'DISCARD' => 1, 'DYNAMIC' => 1, 'ENGINES' => 1,
        'EXECUTE' => 1, 'HANDLER' => 1, 'INDEXES' => 1, 'INVOKER' => 1, 'MIGRATE' => 1,
        'PARTIAL' => 1, 'PREPARE' => 1, 'PROFILE' => 1, 'RECOVER' => 1, 'RESTORE' => 1,
        'RETURNS' => 1, 'ROUTINE' => 1, 'SESSION' => 1, 'STORAGE' => 1, 'STRIPED' => 1,
        'SUBJECT' => 1, 'SUSPEND' => 1, 'UNICODE' => 1, 'UNKNOWN' => 1, 'UPGRADE' => 1,
        'USE_FRM' => 1, 'VIRTUAL' => 1,
        'CASCADED' => 1, 'CHECKSUM' => 1, 'DUMPFILE' => 1, 'EXTENDED' => 1,
        'FUNCTION' => 1, 'INNOBASE' => 1, 'LANGUAGE' => 1, 'MAX_ROWS' => 1,
        'MIN_ROWS' => 1, 'NATIONAL' => 1, 'NVARCHAR' => 1, 'ONE_SHOT' => 1,
        'PROFILES' => 1, 'ROLLBACK' => 1, 'SECURITY' => 1, 'SHUTDOWN' => 1,
        'SNAPSHOT' => 1, 'SWITCHES' => 1, 'TRIGGERS' => 1, 'WARNINGS' => 1,
        'AGGREGATE' => 1, 'ALGORITHM' => 1, 'COMMITTED' => 1, 'DIRECTORY' => 1,
        'DUPLICATE' => 1, 'EXPANSION' => 1, 'IO_THREAD' => 1, 'ISOLATION' => 1,
        'PACK_KEYS' => 1, 'RAID_TYPE' => 1, 'REDUNDANT' => 1, 'SAVEPOINT' => 1,
        'SQL_CACHE' => 1, 'TEMPORARY' => 1, 'TEMPTABLE' => 1, 'UNDEFINED' => 1,
        'VARIABLES' => 1,
        'BERKELEYDB' => 1, 'COMPRESSED' => 1, 'CONCURRENT' => 1, 'CONNECTION' => 1,
        'CONSISTENT' => 1, 'DEALLOCATE' => 1, 'IDENTIFIED' => 1, 'MASTER_SSL' => 1,
        'NDBCLUSTER' => 1, 'PARTITIONS' => 1, 'PERSISTENT' => 1, 'PRIVILEGES' => 1,
        'REPEATABLE' => 1, 'ROW_FORMAT' => 1, 'SQL_THREAD' => 1, 'TABLESPACE' => 1,
        'FRAC_SECOND' => 1, 'MASTER_HOST' => 1, 'MASTER_PORT' => 1, 'MASTER_USER' => 1,
        'PROCESSLIST' => 1, 'RAID_CHUNKS' => 1, 'REPLICATION' => 1, 'SQL_TSI_DAY' => 1,
        'TRANSACTION' => 1, 'UNCOMMITTED' => 1,
        'DES_KEY_FILE' => 1, 'RELAY_THREAD' => 1, 'SERIALIZABLE' => 1,
        'SQL_NO_CACHE' => 1, 'SQL_TSI_HOUR' => 1, 'SQL_TSI_WEEK' => 1,
        'SQL_TSI_YEAR' => 1,
        'INSERT_METHOD' => 1, 'MASTER_SSL_CA' => 1, 'RELAY_LOG_POS' => 1,
        'SQL_TSI_MONTH' => 1, 'SUBPARTITIONS' => 1,
        'AUTO_INCREMENT' => 1, 'AVG_ROW_LENGTH' => 1, 'MASTER_LOG_POS' => 1,
        'MASTER_SSL_KEY' => 1, 'RAID_CHUNKSIZE' => 1, 'RELAY_LOG_FILE' => 1,
        'SQL_TSI_MINUTE' => 1, 'SQL_TSI_SECOND' => 1, 'USER_RESOURCES' => 1,
        'DELAY_KEY_WRITE' => 1, 'MASTER_LOG_FILE' => 1, 'MASTER_PASSWORD' => 1,
        'MASTER_SSL_CERT' => 1, 'SQL_TSI_QUARTER' => 1,
        'MASTER_SERVER_ID' => 1,
        'MASTER_SSL_CAPATH' => 1, 'MASTER_SSL_CIPHER' => 1, 'SQL_BUFFER_RESULT' => 1,
        'SQL_TSI_FRAC_SECOND' => 1,
        'MASTER_CONNECT_RETRY' => 1, 'MAX_QUERIES_PER_HOUR' => 1,
        'MAX_UPDATES_PER_HOUR' => 1, 'MAX_USER_CONNECTIONS' => 1,
        'MAX_CONNECTIONS_PER_HOUR' => 1,

        'AS' => 3, 'BY' => 3, 'IS' => 3, 'ON' => 3, 'OR' => 3, 'TO' => 3,
        'ADD' => 3, 'ALL' => 3, 'AND' => 3, 'ASC' => 3, 'DEC' => 3, 'DIV' => 3,
        'FOR' => 3, 'NOT' => 3, 'OUT' => 3, 'SQL' => 3, 'SSL' => 3, 'USE' => 3,
        'XOR' => 3,
        'BOTH' => 3, 'CALL' => 3, 'CASE' => 3, 'DESC' => 3, 'DROP' => 3, 'DUAL' => 3,
        'EACH' => 3, 'ELSE' => 3, 'EXIT' => 3, 'FROM' => 3, 'INT1' => 3, 'INT2' => 3,
        'INT3' => 3, 'INT4' => 3, 'INT8' => 3, 'INTO' => 3, 'JOIN' => 3, 'KEYS' => 3,
        'KILL' => 3, 'LIKE' => 3, 'LOAD' => 3, 'LOCK' => 3, 'LONG' => 3, 'LOOP' => 3,
        'NULL' => 3, 'READ' => 3, 'SHOW' => 3, 'THEN' => 3, 'TRUE' => 3, 'UNDO' => 3,
        'WHEN' => 3, 'WITH' => 3,
        'ALTER' => 3, 'CHECK' => 3, 'CROSS' => 3, 'FALSE' => 3, 'FETCH' => 3,
        'FORCE' => 3, 'GRANT' => 3, 'GROUP' => 3, 'INNER' => 3, 'INOUT' => 3,
        'LEAVE' => 3, 'LIMIT' => 3, 'LINES' => 3, 'ORDER' => 3, 'OUTER' => 3,
        'PURGE' => 3, 'READS' => 3, 'RLIKE' => 3, 'TABLE' => 3, 'UNION' => 3,
        'USAGE' => 3, 'USING' => 3, 'WHERE' => 3, 'WHILE' => 3, 'WRITE' => 3,
        'BEFORE' => 3, 'CHANGE' => 3, 'COLUMN' => 3, 'CREATE' => 3, 'CURSOR' => 3,
        'DELETE' => 3, 'ELSEIF' => 3, 'EXISTS' => 3, 'FLOAT4' => 3, 'FLOAT8' => 3,
        'HAVING' => 3, 'IGNORE' => 3, 'INFILE' => 3, 'OPTION' => 3, 'REGEXP' => 3,
        'RENAME' => 3, 'RETURN' => 3, 'REVOKE' => 3, 'SELECT' => 3, 'SONAME' => 3,
        'UNLOCK' => 3, 'UPDATE' => 3,
        'ANALYZE' => 3, 'BETWEEN' => 3, 'CASCADE' => 3, 'COLLATE' => 3, 'DECLARE' => 3,
        'DELAYED' => 3, 'ESCAPED' => 3, 'EXPLAIN' => 3, 'FOREIGN' => 3, 'ITERATE' => 3,
        'LEADING' => 3, 'NATURAL' => 3, 'OUTFILE' => 3, 'PRIMARY' => 3, 'RELEASE' => 3,
        'REQUIRE' => 3, 'SCHEMAS' => 3, 'TRIGGER' => 3, 'VARYING' => 3,
        'CONTINUE' => 3, 'DAY_HOUR' => 3, 'DESCRIBE' => 3, 'DISTINCT' => 3,
        'ENCLOSED' => 3, 'MODIFIES' => 3, 'OPTIMIZE' => 3, 'RESTRICT' => 3,
        'SPECIFIC' => 3, 'SQLSTATE' => 3, 'STARTING' => 3, 'TRAILING' => 3,
        'UNSIGNED' => 3, 'ZEROFILL' => 3,
        'CONDITION' => 3, 'DATABASES' => 3, 'MIDDLEINT' => 3, 'PRECISION' => 3,
        'PROCEDURE' => 3, 'SENSITIVE' => 3, 'SEPARATOR' => 3,
        'ASENSITIVE' => 3, 'CONSTRAINT' => 3, 'DAY_MINUTE' => 3, 'DAY_SECOND' => 3,
        'OPTIONALLY' => 3, 'REFERENCES' => 3, 'SQLWARNING' => 3, 'TERMINATED' => 3,
        'YEAR_MONTH' => 3,
        'DISTINCTROW' => 3, 'HOUR_MINUTE' => 3, 'HOUR_SECOND' => 3, 'INSENSITIVE' => 3,
        'LOW_PRIORITY' => 3, 'SQLEXCEPTION' => 3, 'VARCHARACTER' => 3,
        'DETERMINISTIC' => 3, 'HIGH_PRIORITY' => 3, 'MINUTE_SECOND' => 3,
        'STRAIGHT_JOIN' => 3,
        'SQL_BIG_RESULT' => 3,
        'DAY_MICROSECOND' => 3,
        'HOUR_MICROSECOND' => 3, 'SQL_SMALL_RESULT' => 3,
        'MINUTE_MICROSECOND' => 3, 'NO_WRITE_TO_BINLOG' => 3, 'SECOND_MICROSECOND' => 3,
        'SQL_CALC_FOUND_ROWS' => 3,

        'GROUP BY' => 7, 'NOT NULL' => 7, 'ORDER BY' => 7, 'SET NULL' => 7,
        'AND CHAIN' => 7, 'FULL JOIN' => 7, 'IF EXISTS' => 7, 'LEFT JOIN' => 7,
        'LESS THAN' => 7, 'NO ACTION' => 7, 'ON DELETE' => 7, 'ON UPDATE' => 7,
        'UNION ALL' => 7,
        'CROSS JOIN' => 7, 'ESCAPED BY' => 7, 'FOR UPDATE' => 7, 'INNER JOIN' => 7,
        'LINEAR KEY' => 7, 'NO RELEASE' => 7, 'OR REPLACE' => 7, 'RIGHT JOIN' => 7,
        'ENCLOSED BY' => 7, 'LINEAR HASH' => 7, 'STARTING BY' => 7,
        'AND NO CHAIN' => 7, 'FOR EACH ROW' => 7, 'NATURAL JOIN' => 7,
        'PARTITION BY' => 7, 'SET PASSWORD' => 7, 'SQL SECURITY' => 7,
        'CHARACTER SET' => 7, 'IF NOT EXISTS' => 7, 'TERMINATED BY' => 7,
        'DATA DIRECTORY' => 7, 'UNION DISTINCT' => 7,
        'DEFAULT CHARSET' => 7, 'DEFAULT COLLATE' => 7, 'FULL OUTER JOIN' => 7,
        'INDEX DIRECTORY' => 7, 'LEFT OUTER JOIN' => 7, 'SUBPARTITION BY' => 7,
        'GENERATED ALWAYS' => 7, 'RIGHT OUTER JOIN' => 7,
        'NATURAL LEFT JOIN' => 7, 'START TRANSACTION' => 7,
        'LOCK IN SHARE MODE' => 7, 'NATURAL RIGHT JOIN' => 7, 'SELECT TRANSACTION' => 7,
        'DEFAULT CHARACTER SET' => 7,
        'NATURAL LEFT OUTER JOIN' => 7,
        'NATURAL RIGHT OUTER JOIN' => 7, 'WITH CONSISTENT SNAPSHOT' => 7,

        'BIT' => 9, 'XML' => 9,
        'ENUM' => 9, 'JSON' => 9, 'TEXT' => 9,
        'ARRAY' => 9,
        'SERIAL' => 9,
        'BOOLEAN' => 9,
        'DATETIME' => 9, 'GEOMETRY' => 9, 'MULTISET' => 9,
        'MULTILINEPOINT' => 9,
        'MULTILINEPOLYGON' => 9,

        'INT' => 11, 'SET' => 11,
        'BLOB' => 11, 'REAL' => 11,
        'FLOAT' => 11,
        'BIGINT' => 11, 'DOUBLE' => 11,
        'DECIMAL' => 11, 'INTEGER' => 11, 'NUMERIC' => 11, 'TINYINT' => 11, 'VARCHAR' => 11,
        'LONGBLOB' => 11, 'LONGTEXT' => 11, 'SMALLINT' => 11, 'TINYBLOB' => 11,
        'TINYTEXT' => 11,
        'CHARACTER' => 11, 'MEDIUMINT' => 11, 'VARBINARY' => 11,
        'MEDIUMBLOB' => 11, 'MEDIUMTEXT' => 11,

        'BINARY VARYING' => 15,

        'KEY' => 19,
        'INDEX' => 19,
        'UNIQUE' => 19,
        'SPATIAL' => 19,
        'FULLTEXT' => 19,

        'INDEX KEY' => 23,
        'UNIQUE KEY' => 23,
        'FOREIGN KEY' => 23, 'PRIMARY KEY' => 23, 'SPATIAL KEY' => 23,
        'FULLTEXT KEY' => 23, 'UNIQUE INDEX' => 23,
        'SPATIAL INDEX' => 23,
        'FULLTEXT INDEX' => 23,

        'X' => 33, 'Y' => 33,
        'LN' => 33, 'PI' => 33,
        'ABS' => 33, 'AVG' => 33, 'BIN' => 33, 'COS' => 33, 'COT' => 33, 'DAY' => 33,
        'ELT' => 33, 'EXP' => 33, 'HEX' => 33, 'LOG' => 33, 'MAX' => 33, 'MD5' => 33,
        'MID' => 33, 'MIN' => 33, 'NOW' => 33, 'OCT' => 33, 'ORD' => 33, 'POW' => 33,
        'SIN' => 33, 'STD' => 33, 'SUM' => 33, 'TAN' => 33,
        'ACOS' => 33, 'AREA' => 33, 'ASIN' => 33, 'ATAN' => 33, 'CAST' => 33, 'CEIL' => 33,
        'CONV' => 33, 'HOUR' => 33, 'LOG2' => 33, 'LPAD' => 33, 'RAND' => 33, 'RPAD' => 33,
        'SHA1' => 33, 'SIGN' => 33, 'SQRT' => 33, 'SRID' => 33, 'TRIM' => 33, 'USER' => 33,
        'UUID' => 33, 'WEEK' => 33,
        'ASCII' => 33, 'ATAN2' => 33, 'COUNT' => 33, 'CRC32' => 33, 'FIELD' => 33,
        'FLOOR' => 33, 'INSTR' => 33, 'LCASE' => 33, 'LEAST' => 33, 'LOG10' => 33,
        'LOWER' => 33, 'LTRIM' => 33, 'MONTH' => 33, 'POWER' => 33, 'QUOTE' => 33,
        'ROUND' => 33, 'RTRIM' => 33, 'SLEEP' => 33, 'SPACE' => 33, 'UCASE' => 33,
        'UNHEX' => 33, 'UPPER' => 33,
        'ASTEXT' => 33, 'BIT_OR' => 33, 'CONCAT' => 33, 'DECODE' => 33, 'ENCODE' => 33,
        'EQUALS' => 33, 'FORMAT' => 33, 'IFNULL' => 33, 'ISNULL' => 33, 'LENGTH' => 33,
        'LOCATE' => 33, 'MINUTE' => 33, 'NULLIF' => 33, 'POINTN' => 33, 'SECOND' => 33,
        'STDDEV' => 33, 'STRCMP' => 33, 'SUBSTR' => 33, 'WITHIN' => 33,
        'ADDDATE' => 33, 'ADDTIME' => 33, 'AGAINST' => 33, 'BIT_AND' => 33, 'BIT_XOR' => 33,
        'CEILING' => 33, 'CHARSET' => 33, 'CROSSES' => 33, 'CURDATE' => 33, 'CURTIME' => 33,
        'DAYNAME' => 33, 'DEGREES' => 33, 'ENCRYPT' => 33, 'EXTRACT' => 33, 'GLENGTH' => 33,
        'ISEMPTY' => 33, 'QUARTER' => 33, 'RADIANS' => 33, 'REVERSE' => 33, 'SOUNDEX' => 33,
        'SUBDATE' => 33, 'SUBTIME' => 33, 'SYSDATE' => 33, 'TOUCHES' => 33, 'TO_DAYS' => 33,
        'VAR_POP' => 33, 'VERSION' => 33, 'WEEKDAY' => 33,
        'ASBINARY' => 33, 'CENTROID' => 33, 'COALESCE' => 33, 'COMPRESS' => 33,
        'CONTAINS' => 33, 'DATEDIFF' => 33, 'DATE_ADD' => 33, 'DATE_SUB' => 33,
        'DISJOINT' => 33, 'ENDPOINT' => 33, 'ENVELOPE' => 33, 'GET_LOCK' => 33,
        'GREATEST' => 33, 'ISCLOSED' => 33, 'ISSIMPLE' => 33, 'MAKEDATE' => 33,
        'MAKETIME' => 33, 'MAKE_SET' => 33, 'MBREQUAL' => 33, 'OVERLAPS' => 33,
        'PASSWORD' => 33, 'POSITION' => 33, 'TIMEDIFF' => 33, 'TRUNCATE' => 33,
        'VARIANCE' => 33, 'VAR_SAMP' => 33, 'YEARWEEK' => 33,
        'BENCHMARK' => 33, 'BIT_COUNT' => 33, 'COLLATION' => 33, 'CONCAT_WS' => 33,
        'DAYOFWEEK' => 33, 'DAYOFYEAR' => 33, 'DIMENSION' => 33, 'FROM_DAYS' => 33,
        'GEOMETRYN' => 33, 'INET_ATON' => 33, 'INET_NTOA' => 33, 'LOAD_FILE' => 33,
        'MBRWITHIN' => 33, 'MONTHNAME' => 33, 'NUMPOINTS' => 33, 'ROW_COUNT' => 33,
        'SUBSTRING' => 33,
        'BIT_LENGTH' => 33, 'CONVERT_TZ' => 33, 'DAYOFMONTH' => 33, 'EXPORT_SET' => 33,
        'FOUND_ROWS' => 33, 'GET_FORMAT' => 33, 'INTERSECTS' => 33, 'MBRTOUCHES' => 33,
        'MULTIPOINT' => 33, 'NAME_CONST' => 33, 'PERIOD_ADD' => 33, 'STARTPOINT' => 33,
        'STDDEV_POP' => 33, 'UNCOMPRESS' => 33, 'WEEKOFYEAR' => 33,
        'AES_DECRYPT' => 33, 'AES_ENCRYPT' => 33, 'CHAR_LENGTH' => 33, 'DATE_FORMAT' => 33,
        'DES_DECRYPT' => 33, 'DES_ENCRYPT' => 33, 'FIND_IN_SET' => 33, 'GEOMFROMWKB' => 33,
        'LINEFROMWKB' => 33, 'MBRCONTAINS' => 33, 'MBRDISJOINT' => 33, 'MBROVERLAPS' => 33,
        'MICROSECOND' => 33, 'PERIOD_DIFF' => 33, 'POLYFROMWKB' => 33, 'SEC_TO_TIME' => 33,
        'STDDEV_SAMP' => 33, 'STR_TO_DATE' => 33, 'SYSTEM_USER' => 33, 'TIME_FORMAT' => 33,
        'TIME_TO_SEC' => 33,
        'COERCIBILITY' => 33, 'EXTERIORRING' => 33, 'GEOMETRYTYPE' => 33,
        'GEOMFROMTEXT' => 33, 'GROUP_CONCAT' => 33, 'IS_FREE_LOCK' => 33,
        'IS_USED_LOCK' => 33, 'LINEFROMTEXT' => 33, 'MLINEFROMWKB' => 33,
        'MPOLYFROMWKB' => 33, 'MULTIPOLYGON' => 33, 'OCTET_LENGTH' => 33,
        'OLD_PASSWORD' => 33, 'POINTFROMWKB' => 33, 'POLYFROMTEXT' => 33,
        'RELEASE_LOCK' => 33, 'SESSION_USER' => 33, 'TIMESTAMPADD' => 33,
        'CONNECTION_ID' => 33, 'FROM_UNIXTIME' => 33, 'INTERIORRINGN' => 33,
        'MBRINTERSECTS' => 33, 'MLINEFROMTEXT' => 33, 'MPOINTFROMWKB' => 33,
        'MPOLYFROMTEXT' => 33, 'NUMGEOMETRIES' => 33, 'POINTFROMTEXT' => 33,
        'TIMESTAMPDIFF' => 33,
        'LAST_INSERT_ID' => 33, 'MPOINTFROMTEXT' => 33, 'UNIX_TIMESTAMP' => 33,
        'GEOMCOLLFROMWKB' => 33, 'MASTER_POS_WAIT' => 33, 'SUBSTRING_INDEX' => 33,
        'CHARACTER_LENGTH' => 33, 'GEOMCOLLFROMTEXT' => 33, 'NUMINTERIORRINGS' => 33,
        'UNCOMPRESSED_LENGTH' => 33,

        'IF' => 35, 'IN' => 35,
        'MOD' => 35,
        'LEFT' => 35,
        'MATCH' => 35, 'RIGHT' => 35,
        'INSERT' => 35, 'REPEAT' => 35, 'SCHEMA' => 35, 'VALUES' => 35,
        'CONVERT' => 35, 'DEFAULT' => 35, 'REPLACE' => 35,
        'DATABASE' => 35, 'UTC_DATE' => 35, 'UTC_TIME' => 35,
        'LOCALTIME' => 35,
        'CURRENT_DATE' => 35, 'CURRENT_TIME' => 35, 'CURRENT_USER' => 35,
        'UTC_TIMESTAMP' => 35,
        'LOCALTIMESTAMP' => 35,
        'CURRENT_TIMESTAMP' => 35,

        'NOT IN' => 39,

        'DATE' => 41, 'TIME' => 41, 'YEAR' => 41,
        'POINT' => 41,
        'POLYGON' => 41,
        'TIMESTAMP' => 41,
        'LINESTRING' => 41,
        'MULTILINESTRING' => 41,
        'GEOMETRYCOLLECTION' => 41,

        'CHAR' => 43,
        'BINARY' => 43,
        'INTERVAL' => 43,
    );
}