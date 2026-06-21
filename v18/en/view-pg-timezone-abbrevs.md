## 53.33. `pg_timezone_abbrevs` [#](#VIEW-PG-TIMEZONE-ABBREVS)

The view `pg_timezone_abbrevs` provides a list of time zone abbreviations that are currently recognized by the datetime input routines. The contents of this view change when the [TimeZone](runtime-config-client.md#GUC-TIMEZONE) or [timezone_abbreviations](runtime-config-client.md#GUC-TIMEZONE-ABBREVIATIONS) run-time parameters are modified.

**Table 53.33. `pg_timezone_abbrevs` Columns**



<table border="1" class="table" summary="pg_timezone_abbrevs Columns">
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
     True if this is a daylight-savings abbreviation
    </p>
   </td>
  </tr>
 </tbody>
</table>




  

While most timezone abbreviations represent fixed offsets from UTC, there are some that have historically varied in value (see [Section B.4](datetime-config-files.md "B.4. Date/Time Configuration Files") for more information). In such cases this view presents their current meaning.
