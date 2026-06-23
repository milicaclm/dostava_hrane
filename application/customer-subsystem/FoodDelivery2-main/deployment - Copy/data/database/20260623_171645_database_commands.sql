ALTER TABLE "myfirstmodule$restaurantapi" ALTER COLUMN "restaurantid" SET DATA TYPE VARCHAR_IGNORECASE(40);
UPDATE "mendixsystem$attribute" SET "entity_id" = '736d9d96-2957-47c9-becf-9293091b1532', "attribute_name" = 'restaurantId', "column_name" = 'restaurantid', "type" = 30, "length" = 40, "default_value" = '', "is_auto_number" = false WHERE "id" = '81f4c622-3370-4c39-b2ab-76369c21a922';
UPDATE "mendixsystem$version" SET "versionnumber" = '4.2', "lastsyncdate" = '20260623 17:16:45';
