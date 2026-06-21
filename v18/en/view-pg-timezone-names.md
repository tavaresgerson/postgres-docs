## 53.34. `pg_timezone_names` [#](#VIEW-PG-TIMEZONE-NAMES)

The view `pg_timezone_names` provides a list of time zone names that are recognized by `SET TIMEZONE`, along with their associated abbreviations, UTC offsets, and daylight-savings status. (Technically, PostgreSQL does not use UTC because leap seconds are not handled.) Unlike the abbreviations shown in [`pg_timezone_abbrevs`](view-pg-timezone-abbrevs.md "53.33. pg_timezone_abbrevs"), many of these names imply a set of daylight-savings transition date rules. Therefore, the associated information changes across local DST boundaries. The displayed information is computed based on the current value of `CURRENT_TIMESTAMP`.

**Table 53.34. `pg_timezone_names` Columns**



<table border="1" class="table" summary="pg_timezone_names Columns">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="catalog_table_entry">
    <p class="column_definition">
     Column Type
    </p>
    <p>
     Description
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      name
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Time zone name
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      abbrev
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Time zone abbreviation
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      utc_offset
     </code>
     <code class="type">
      interval
     </code>
    </p>
    <p>
     Offset from UTC (positive means east of Greenwich)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      is_dst
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     True if currently observing daylight savings
    </p>
   </td>
  </tr>
 </tbody>
</table>

