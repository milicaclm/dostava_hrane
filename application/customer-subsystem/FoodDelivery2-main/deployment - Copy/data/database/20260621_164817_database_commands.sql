ALTER TABLE "myfirstmodule$order" ALTER COLUMN "s" RENAME TO "status";
UPDATE "mendixsystem$attribute" SET "entity_id" = 'a5baea4c-17c2-4f38-9dde-754dbfa493a4', "attribute_name" = 'Status', "column_name" = 'status', "type" = 40, "length" = 9, "default_value" = 'Cart', "is_auto_number" = false WHERE "id" = '9e709603-e0cc-48f1-a95e-adc06701d978';
UPDATE "mendixsystem$version" SET "versionnumber" = '4.2', "lastsyncdate" = '20260621 16:48:17';
