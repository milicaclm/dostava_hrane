ALTER TABLE "myfirstmodule$address" ALTER COLUMN "streert" RENAME TO "street";
UPDATE "mendixsystem$attribute" SET "entity_id" = '95d2d9b2-b766-4045-bce0-c97cdda908a5', "attribute_name" = 'Street', "column_name" = 'street', "type" = 30, "length" = 200, "default_value" = '', "is_auto_number" = false WHERE "id" = '00ac828d-bf63-4278-b9eb-ed94205bbc06';
UPDATE "mendixsystem$version" SET "versionnumber" = '4.2', "lastsyncdate" = '20260613 19:03:04';
