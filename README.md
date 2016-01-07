# PCORnet CDM

### History
* v0.01:
  - Bootstrap script ([bootstrap_cdm_tables.py](bootstrap_cdm_tables.py)) to create table structures (MSSQL) from PCORnet CDM v3 defintion files ([2015-06-01 PCORnet Common Data Model v3.0 – parseable](http://www.pcornet.org/wp-content/uploads/2015/06/2015-06-01-PCORnet-Common-Data-Model-v3dot0-parseable.xlsx))
* v0.02:
  - **OneFlorida Specific**: Add `UPDATED` and `SOURCE` columns to each table for tracking the SOURCE system and when the record is updated; HARVEST table does have these two columns as well. Up for discussion. 
