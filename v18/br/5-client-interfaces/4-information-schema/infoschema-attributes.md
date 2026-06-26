## 35.6. `attributes` [#](#INFOSCHEMA-ATTRIBUTES)

A vista `attributes` contém informações sobre os atributos dos tipos de dados compostos definidos no banco de dados. (Observe que a vista não fornece informações sobre as colunas da tabela, que às vezes são chamadas de atributos em contextos PostgreSQL.) Apenas os atributos que o usuário atual tem acesso (por ser o proprietário ou ter algum privilégio sobre o tipo) são mostrados.

**Tabela 35.4. Colunas `attributes`**



<table>
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
     <code>
      udt_catalog
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database containing the data type (always the current database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      udt_schema
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the schema containing the data type
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      udt_name
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the data type
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      attribute_name
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the attribute
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      ordinal_position
     </code>
     <code>
      cardinal_number
     </code>
    </p>
    <p>
     Ordinal position of the attribute within the data type (count starts at 1)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      attribute_default
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     Default expression of the attribute
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      is_nullable
     </code>
     <code>
      yes_or_no
     </code>
    </p>
    <p>
     <code>
      YES
     </code>
     if the attribute is possibly nullable,
     <code>
      NO
     </code>
     if it is known not nullable.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      data_type
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     Data type of the attribute, if it is a built-in type, or
     <code>
      ARRAY
     </code>
     if it is some array (in that case, see the view
     <code>
      element_types
     </code>
     ), else
     <code>
      USER-DEFINED
     </code>
     (in that case, the type is identified in
     <code>
      attribute_udt_name
     </code>
     and associated columns).
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      character_maximum_length
     </code>
     <code>
      cardinal_number
     </code>
    </p>
    <p>
     If
     <code>
      data_type
     </code>
     identifies a character or bit string type, the declared maximum length; null for all other data types or if no maximum length was declared.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      character_octet_length
     </code>
     <code>
      cardinal_number
     </code>
    </p>
    <p>
     If
     <code>
      data_type
     </code>
     identifies a character type, the maximum possible length in octets (bytes) of a datum; null for all other data types.  The maximum octet length depends on the declared character maximum length (see above) and the server encoding.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      character_set_catalog
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Applies to a feature not available in
     <span class="productname">
      PostgreSQL
     </span>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      character_set_schema
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Applies to a feature not available in
     <span class="productname">
      PostgreSQL
     </span>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      character_set_name
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Applies to a feature not available in
     <span class="productname">
      PostgreSQL
     </span>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      collation_catalog
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database containing the collation of the attribute (always the current database), null if default or the data type of the attribute is not collatable
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      collation_schema
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the schema containing the collation of the attribute, null if default or the data type of the attribute is not collatable
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      collation_name
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the collation of the attribute, null if default or the data type of the attribute is not collatable
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      numeric_precision
     </code>
     <code>
      cardinal_number
     </code>
    </p>
    <p>
     If
     <code>
      data_type
     </code>
     identifies a numeric type, this column contains the (declared or implicit) precision of the type for this attribute.  The precision indicates the number of significant digits.  It can be expressed in decimal (base 10) or binary (base 2) terms, as specified in the column
     <code>
      numeric_precision_radix
     </code>
     .  For all other data types, this column is null.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      numeric_precision_radix
     </code>
     <code>
      cardinal_number
     </code>
    </p>
    <p>
     If
     <code>
      data_type
     </code>
     identifies a numeric type, this column indicates in which base the values in the columns
     <code>
      numeric_precision
     </code>
     and
     <code>
      numeric_scale
     </code>
     are expressed.  The value is either 2 or 10.  For all other data types, this column is null.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      numeric_scale
     </code>
     <code>
      cardinal_number
     </code>
    </p>
    <p>
     If
     <code>
      data_type
     </code>
     identifies an exact numeric type, this column contains the (declared or implicit) scale of the type for this attribute.  The scale indicates the number of significant digits to the right of the decimal point.  It can be expressed in decimal (base 10) or binary (base 2) terms, as specified in the column
     <code>
      numeric_precision_radix
     </code>
     .  For all other data types, this column is null.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      datetime_precision
     </code>
     <code>
      cardinal_number
     </code>
    </p>
    <p>
     If
     <code>
      data_type
     </code>
     identifies a date, time, timestamp, or interval type, this column contains the (declared or implicit) fractional seconds precision of the type for this attribute, that is, the number of decimal digits maintained following the decimal point in the seconds value.  For all other data types, this column is null.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      interval_type
     </code>
     <code>
      character_data
     </code>
    </p>
    <p>
     If
     <code>
      data_type
     </code>
     identifies an interval type, this column contains the specification which fields the intervals include for this attribute, e.g.,
     <code>
      YEAR TO MONTH
     </code>
     ,
     <code>
      DAY TO SECOND
     </code>
     , etc.  If no field restrictions were specified (that is, the interval accepts all fields), and for all other data types, this field is null.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      interval_precision
     </code>
     <code>
      cardinal_number
     </code>
    </p>
    <p>
     Applies to a feature not available in
     <span class="productname">
      PostgreSQL
     </span>
     (see
     <code>
      datetime_precision
     </code>
     for the fractional seconds precision of interval type attributes)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      attribute_udt_catalog
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the database that the attribute data type is defined in (always the current database)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      attribute_udt_schema
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the schema that the attribute data type is defined in
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      attribute_udt_name
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Name of the attribute data type
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      scope_catalog
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Applies to a feature not available in
     <span class="productname">
      PostgreSQL
     </span>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      scope_schema
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Applies to a feature not available in
     <span class="productname">
      PostgreSQL
     </span>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      scope_name
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     Applies to a feature not available in
     <span class="productname">
      PostgreSQL
     </span>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      maximum_cardinality
     </code>
     <code>
      cardinal_number
     </code>
    </p>
    <p>
     Always null, because arrays always have unlimited maximum cardinality in
     <span class="productname">
      PostgreSQL
     </span>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      dtd_identifier
     </code>
     <code>
      sql_identifier
     </code>
    </p>
    <p>
     An identifier of the data type descriptor of the attribute, unique among the data type descriptors pertaining to the composite type.  This is mainly useful for joining with other instances of such identifiers.  (The specific format of the identifier is not defined and not guaranteed to remain the same in future versions.)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      is_derived_reference_attribute
     </code>
     <code>
      yes_or_no
     </code>
    </p>
    <p>
     Applies to a feature not available in
     <span class="productname">
      PostgreSQL
     </span>
    </p>
   </td>
  </tr>
 </tbody>
</table>










Veja também, sob [Seção 35.17](infoschema-columns.md), uma visão de estrutura semelhante, para obter mais informações sobre algumas das colunas.