with
  root as (
    select 
      cit.name as city,
      safe_cast(ven2.vendor_code as int) as vendor_id,
      trim(regexp_replace(initcap(regexp_replace(translate(vendor.vendor_name, 'áéíóúâêîôûàèìòùãñõäëïöüç' || UPPER('áéíóúâêîôûàèìòùãñõäëïöüç') || '`´', 'aeiouaeiouaeiouanoaeiouc' || UPPER('aeiouaeiouaeiouanoaeiouc') || '\''), '[[:punct:]]', '')), '\\s{2,5}', ' ')) as vendor_name,
      ven2.vertical_type as vertical,
      ven2.location as location,
      row_number() over(partition by ven2.vendor_code order by ven2.vendor_code) as rn
    from `fulfillment-dwh-production.curated_data_shared.vendors_v2` ven2,
    unnest(vendor) vendor,
    unnest(delivery_areas) delivery_areas,
    unnest(delivery_areas_location) delivery_areas_location
    left join `fulfillment-dwh-production.curated_data_shared.countries` as con on delivery_areas_location.country_code=con.country_code
    left join unnest(cities) as cit on cit.id=delivery_areas_location.city_id
    where delivery_areas_location.country_code='pe'
    and ven2.is_active
    and delivery_areas.is_deleted = false
    and ven2.location is not null),
  partners as (
    select
      vendor_id,
      brand_name,
      vendor_name,
      vertical
    from `peya-peru.automated_tables_reports.peya_partner_base`)
select
  r.city,
  r.vendor_id,
  p.brand_name,
  r.vendor_name,
  r.vertical,
  ST_Y(r.location) as latitude,
  ST_X(r.location) as longitude
from root as r
left join partners as p on r.vendor_id = p.vendor_id
where r.rn = 1