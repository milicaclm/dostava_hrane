ALTER TABLE "myfirstmodule$order" DROP COLUMN "orderstatus";
ALTER TABLE "myfirstmodule$order" DROP COLUMN "paymentmethod";
ALTER TABLE "myfirstmodule$order" ADD "s" VARCHAR_IGNORECASE(9) NULL;
UPDATE "myfirstmodule$order" SET "s" = 'Pending';
ALTER TABLE "myfirstmodule$order" ADD "paymentmethod" VARCHAR_IGNORECASE(4) NULL;
UPDATE "mendixsystem$attribute" SET "entity_id" = 'a5baea4c-17c2-4f38-9dde-754dbfa493a4', "attribute_name" = 's', "column_name" = 's', "type" = 40, "length" = 9, "default_value" = 'Pending', "is_auto_number" = false WHERE "id" = '9e709603-e0cc-48f1-a95e-adc06701d978';
UPDATE "mendixsystem$attribute" SET "entity_id" = 'a5baea4c-17c2-4f38-9dde-754dbfa493a4', "attribute_name" = 'PaymentMethod', "column_name" = 'paymentmethod', "type" = 40, "length" = 4, "default_value" = '', "is_auto_number" = false WHERE "id" = '21635e09-2338-418a-afaf-e08664d55e1f';
UPDATE "mendixsystem$version" SET "versionnumber" = '4.2', "lastsyncdate" = '20260621 12:35:57';
