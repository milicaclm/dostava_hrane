ALTER TABLE "myfirstmodule$order" DROP CONSTRAINT "frn_myfirstmodule$order_myfirstmodule$order_restaurant";
ALTER TABLE "myfirstmodule$orderitem" DROP CONSTRAINT "frn_myfirstmodule$orderitem_myfirstmodule$orderitem_menuitem";
ALTER TABLE "myfirstmodule$restaurant" RENAME TO "4b180270ffc345459de199328532fe79";
DROP INDEX "idx_myfirstmodule$order_myfirstmodule$order_restaurant";
DROP INDEX "idx_myfirstmodule$orderitem_myfirstmodule$orderitem_menuitem";
ALTER TABLE "myfirstmodule$menuitem" DROP CONSTRAINT "frn_myfirstmodule$menuitem_myfirstmodule$menuitem_restaurant";
ALTER TABLE "myfirstmodule$menuitem" DROP CONSTRAINT "frn_myfirstmodule$menuitem_myfirstmodule$menuitem_order";
DROP INDEX "idx_myfirstmodule$menuitem_myfirstmodule$menuitem_order";
DROP INDEX "idx_myfirstmodule$menuitem_myfirstmodule$menuitem_restaurant";
ALTER TABLE "myfirstmodule$menuitem" RENAME TO "3955302ef5e946d784c3e362aa582293";
DELETE FROM "mendixsystem$entity"  WHERE "id" = '718e4aa1-e0e4-4211-924d-0c7df14ea272';
DELETE FROM "mendixsystem$entityidentifier"  WHERE "id" = '718e4aa1-e0e4-4211-924d-0c7df14ea272';
DELETE FROM "mendixsystem$sequence"  WHERE "attribute_id" IN ( SELECT "id" FROM "mendixsystem$attribute" WHERE "entity_id" = '718e4aa1-e0e4-4211-924d-0c7df14ea272' );
DELETE FROM "mendixsystem$remote_primary_key"  WHERE "entity_id" = '718e4aa1-e0e4-4211-924d-0c7df14ea272';
DELETE FROM "mendixsystem$attribute"  WHERE "entity_id" = '718e4aa1-e0e4-4211-924d-0c7df14ea272';
ALTER TABLE "myfirstmodule$restaurantapi" ADD "isrecommended" BOOLEAN NULL;
UPDATE "myfirstmodule$restaurantapi" SET "isrecommended" = false;
ALTER TABLE "myfirstmodule$restaurantapi" ADD "recommendationscore" DECIMAL(28, 8) NULL;
UPDATE "myfirstmodule$restaurantapi" SET "recommendationscore" = 0;
ALTER TABLE "myfirstmodule$restaurantapi" ADD "recommendationreason" VARCHAR_IGNORECASE(200) NULL;
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('b0b00d05-7af5-4656-9aa0-28ce8698721a', '736d9d96-2957-47c9-becf-9293091b1532', 'recommendationReason', 'recommendationreason', 30, 200, '', false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('098bc350-d69b-43c0-9049-31452eb157bb', '736d9d96-2957-47c9-becf-9293091b1532', 'recommendationScore', 'recommendationscore', 5, 0, '0', false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('16aabe9c-d9b8-4ab9-82ec-ff2c2865165a', '736d9d96-2957-47c9-becf-9293091b1532', 'isRecommended', 'isrecommended', 10, 0, 'false', false);
ALTER TABLE "myfirstmodule$order" DROP COLUMN "myfirstmodule$order_restaurant";
ALTER TABLE "myfirstmodule$order" ADD "myfirstmodule$order_restaurantapi" BIGINT NULL;
CREATE INDEX "idx_myfirstmodule$order_myfirstmodule$order_restaurantapi" ON "myfirstmodule$order" ("myfirstmodule$order_restaurantapi" ASC,"id" ASC);
DELETE FROM "mendixsystem$association"  WHERE "id" = 'fbf4e460-35ed-4e90-a485-d0a3c06e9391';
DELETE FROM "mendixsystem$index"  WHERE "id" = 'b891f259-6eca-3c80-a5b9-f8d73fd967d5';
DELETE FROM "mendixsystem$index_column"  WHERE "index_id" = 'b891f259-6eca-3c80-a5b9-f8d73fd967d5';
INSERT INTO "mendixsystem$index" ("id", "table_id", "index_name") VALUES ('8f7f3e4c-3b00-388d-ac58-a3f3438bbccd', 'a5baea4c-17c2-4f38-9dde-754dbfa493a4', 'idx_myfirstmodule$order_myfirstmodule$order_restaurantapi');
INSERT INTO "mendixsystem$index_column" ("index_id", "column_id", "sort_order", "ordinal") VALUES ('8f7f3e4c-3b00-388d-ac58-a3f3438bbccd', 'cedd8d16-e51a-40f7-aa2c-056173cc4745', false, 0);
UPDATE "mendixsystem$association" SET "association_name" = 'MyFirstModule.Order_User', "table_name" = 'myfirstmodule$order', "parent_entity_id" = 'a5baea4c-17c2-4f38-9dde-754dbfa493a4', "child_entity_id" = '5beea804-bb64-4ea9-9a15-732aa76e6ca7', "parent_column_name" = 'id', "child_column_name" = 'myfirstmodule$order_user', "pk_index_name" = NULL, "index_name" = NULL, "parent_fkc_name" = NULL, "child_fkc_name" = 'frn_myfirstmodule$order_myfirstmodule$order_user', "parent_fkc_action" = NULL, "child_fkc_action" = 2, "storage_format" = 1 WHERE "id" = '16f66703-8d7e-4e20-8e8f-f5068805951f';
INSERT INTO "mendixsystem$association" ("id", "association_name", "table_name", "parent_entity_id", "child_entity_id", "parent_column_name", "child_column_name", "child_fkc_name", "child_fkc_action", "storage_format") VALUES ('cedd8d16-e51a-40f7-aa2c-056173cc4745', 'MyFirstModule.Order_RestaurantAPI', 'myfirstmodule$order', 'a5baea4c-17c2-4f38-9dde-754dbfa493a4', '736d9d96-2957-47c9-becf-9293091b1532', 'id', 'myfirstmodule$order_restaurantapi', 'frn_myfirstmodule$order_myfirstmodule$order_restaurantapi', 2, 1);
ALTER TABLE "myfirstmodule$orderitem" DROP COLUMN "myfirstmodule$orderitem_menuitem";
DELETE FROM "mendixsystem$association"  WHERE "id" = '49d2f328-cec0-43e2-8751-2d6a26c2af40';
DELETE FROM "mendixsystem$index"  WHERE "id" = 'b3afb00d-9128-30ea-999f-265d3aad97a8';
DELETE FROM "mendixsystem$index_column"  WHERE "index_id" = 'b3afb00d-9128-30ea-999f-265d3aad97a8';
DELETE FROM "mendixsystem$entity"  WHERE "id" = 'e9aa1047-afa3-4dd0-88b3-541716571542';
DELETE FROM "mendixsystem$entityidentifier"  WHERE "id" = 'e9aa1047-afa3-4dd0-88b3-541716571542';
DELETE FROM "mendixsystem$sequence"  WHERE "attribute_id" IN ( SELECT "id" FROM "mendixsystem$attribute" WHERE "entity_id" = 'e9aa1047-afa3-4dd0-88b3-541716571542' );
DELETE FROM "mendixsystem$remote_primary_key"  WHERE "entity_id" = 'e9aa1047-afa3-4dd0-88b3-541716571542';
DELETE FROM "mendixsystem$attribute"  WHERE "entity_id" = 'e9aa1047-afa3-4dd0-88b3-541716571542';
DELETE FROM "mendixsystem$index"  WHERE "table_id" = 'e9aa1047-afa3-4dd0-88b3-541716571542';
DELETE FROM "mendixsystem$index_column"  WHERE "index_id" IN ('03cd4812-6a4e-303f-aa8f-e5c052a126a2', 'da103443-6170-3ad7-988e-9c0c9db21f24');
DELETE FROM "mendixsystem$association"  WHERE "id" = 'ceac46e3-ab71-42d1-8fb1-745c9bfc27fc';
DELETE FROM "mendixsystem$association"  WHERE "id" = '02bae1e3-ca14-49f8-8187-79e3f5e5ac34';
CREATE TABLE "myfirstmodule$itemapi" (
	"id" BIGINT NOT NULL,
	"itemid" INT NULL,
	"name" VARCHAR_IGNORECASE(200) NULL,
	"description" VARCHAR_IGNORECASE(200) NULL,
	"category" VARCHAR_IGNORECASE(200) NULL,
	"available" BOOLEAN NULL,
	"imageurl" VARCHAR_IGNORECASE(200) NULL,
	"price" DECIMAL(28, 8) NULL,
	"myfirstmodule$itemapi_restaurantapi" BIGINT NULL,
	"myfirstmodule$itemapi_orderitem" BIGINT NULL,
	"myfirstmodule$itemapi_order" BIGINT NULL,
	PRIMARY KEY("id"));
CREATE INDEX "idx_myfirstmodule$itemapi_myfirstmodule$itemapi_restaurantapi" ON "myfirstmodule$itemapi" ("myfirstmodule$itemapi_restaurantapi" ASC,"id" ASC);
CREATE INDEX "idx_myfirstmodule$itemapi_myfirstmodule$itemapi_orderitem" ON "myfirstmodule$itemapi" ("myfirstmodule$itemapi_orderitem" ASC,"id" ASC);
CREATE INDEX "idx_myfirstmodule$itemapi_myfirstmodule$itemapi_order" ON "myfirstmodule$itemapi" ("myfirstmodule$itemapi_order" ASC,"id" ASC);
INSERT INTO "mendixsystem$entity" ("id", "entity_name", "table_name", "remote", "remote_primary_key") VALUES ('537b28a9-dbca-4c42-b410-635e4c9ae32d', 'MyFirstModule.ItemAPI', 'myfirstmodule$itemapi', false, false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('b91b8cee-570c-4065-9556-3b4d03fe4af2', '537b28a9-dbca-4c42-b410-635e4c9ae32d', 'ItemId', 'itemid', 3, 0, '0', false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('03ba507a-c70d-42ae-9810-757517f267be', '537b28a9-dbca-4c42-b410-635e4c9ae32d', 'Name', 'name', 30, 200, '', false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('6c445e27-ec31-49e0-bb1f-2a01a3e2209c', '537b28a9-dbca-4c42-b410-635e4c9ae32d', 'description', 'description', 30, 200, '', false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('7ba5f819-2b4d-40f7-b9ac-d4bf867a4a72', '537b28a9-dbca-4c42-b410-635e4c9ae32d', 'category', 'category', 30, 200, '', false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('55afc14f-6f5f-45cc-adf4-6563a04afad4', '537b28a9-dbca-4c42-b410-635e4c9ae32d', 'available', 'available', 10, 0, 'false', false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('e9b3eede-c95a-4105-87bb-437f186c359e', '537b28a9-dbca-4c42-b410-635e4c9ae32d', 'imageUrl', 'imageurl', 30, 200, '', false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('d7cc2916-ec61-4d3c-83e5-923de7074de8', '537b28a9-dbca-4c42-b410-635e4c9ae32d', 'price', 'price', 5, 0, '0', false);
INSERT INTO "mendixsystem$index" ("id", "table_id", "index_name") VALUES ('640a7fc0-4297-36d0-843e-51b445a54866', '537b28a9-dbca-4c42-b410-635e4c9ae32d', 'idx_myfirstmodule$itemapi_myfirstmodule$itemapi_restaurantapi');
INSERT INTO "mendixsystem$index_column" ("index_id", "column_id", "sort_order", "ordinal") VALUES ('640a7fc0-4297-36d0-843e-51b445a54866', '6bce5ab9-250b-4c63-9ac1-7356a6efad76', false, 0);
INSERT INTO "mendixsystem$index" ("id", "table_id", "index_name") VALUES ('417b6c53-55b4-3dc6-b848-e0d3a49f7aee', '537b28a9-dbca-4c42-b410-635e4c9ae32d', 'idx_myfirstmodule$itemapi_myfirstmodule$itemapi_orderitem');
INSERT INTO "mendixsystem$index_column" ("index_id", "column_id", "sort_order", "ordinal") VALUES ('417b6c53-55b4-3dc6-b848-e0d3a49f7aee', 'f1d521ae-dc5f-4717-9b46-0a7719eb2d7c', false, 0);
INSERT INTO "mendixsystem$index" ("id", "table_id", "index_name") VALUES ('b57e7683-7a1b-3b54-85df-04bdd00d36fe', '537b28a9-dbca-4c42-b410-635e4c9ae32d', 'idx_myfirstmodule$itemapi_myfirstmodule$itemapi_order');
INSERT INTO "mendixsystem$index_column" ("index_id", "column_id", "sort_order", "ordinal") VALUES ('b57e7683-7a1b-3b54-85df-04bdd00d36fe', '0d7cfa75-0907-4552-81ec-69616672d432', false, 0);
INSERT INTO "mendixsystem$association" ("id", "association_name", "table_name", "parent_entity_id", "child_entity_id", "parent_column_name", "child_column_name", "child_fkc_name", "child_fkc_action", "storage_format") VALUES ('6bce5ab9-250b-4c63-9ac1-7356a6efad76', 'MyFirstModule.ItemAPI_RestaurantAPI', 'myfirstmodule$itemapi', '537b28a9-dbca-4c42-b410-635e4c9ae32d', '736d9d96-2957-47c9-becf-9293091b1532', 'id', 'myfirstmodule$itemapi_restaurantapi', 'frn_myfirstmodule$itemapi_myfirstmodule$itemapi_restaurantapi', 2, 1);
INSERT INTO "mendixsystem$association" ("id", "association_name", "table_name", "parent_entity_id", "child_entity_id", "parent_column_name", "child_column_name", "child_fkc_name", "child_fkc_action", "storage_format") VALUES ('f1d521ae-dc5f-4717-9b46-0a7719eb2d7c', 'MyFirstModule.ItemAPI_OrderItem', 'myfirstmodule$itemapi', '537b28a9-dbca-4c42-b410-635e4c9ae32d', 'c0fb1e35-e367-4403-a212-d1973ec3e7d3', 'id', 'myfirstmodule$itemapi_orderitem', 'frn_myfirstmodule$itemapi_myfirstmodule$itemapi_orderitem', 2, 1);
INSERT INTO "mendixsystem$association" ("id", "association_name", "table_name", "parent_entity_id", "child_entity_id", "parent_column_name", "child_column_name", "child_fkc_name", "child_fkc_action", "storage_format") VALUES ('0d7cfa75-0907-4552-81ec-69616672d432', 'MyFirstModule.ItemAPI_Order', 'myfirstmodule$itemapi', '537b28a9-dbca-4c42-b410-635e4c9ae32d', 'a5baea4c-17c2-4f38-9dde-754dbfa493a4', 'id', 'myfirstmodule$itemapi_order', 'frn_myfirstmodule$itemapi_myfirstmodule$itemapi_order', 2, 1);
CREATE TABLE "myfirstmodule$foodphoto" (
	"id" BIGINT NOT NULL,
	"myfirstmodule$foodphoto_itemapi" BIGINT NULL,
	PRIMARY KEY("id"),
	CONSTRAINT "uniq_myfirstmodule$foodphoto_myfirstmodule$foodphoto_itemapi" UNIQUE ("myfirstmodule$foodphoto_itemapi"));
CREATE INDEX "idx_myfirstmodule$foodphoto_myfirstmodule$foodphoto_itemapi" ON "myfirstmodule$foodphoto" ("myfirstmodule$foodphoto_itemapi" ASC,"id" ASC);
INSERT INTO "mendixsystem$entity" ("id", "entity_name", "table_name", "remote", "remote_primary_key") VALUES ('6d3cc67c-5238-4667-a622-fce911897071', 'MyFirstModule.FoodPhoto', 'myfirstmodule$foodphoto', false, false);
INSERT INTO "mendixsystem$index" ("id", "table_id", "index_name") VALUES ('202c732a-3425-3a07-b577-14698c252a14', '6d3cc67c-5238-4667-a622-fce911897071', 'idx_myfirstmodule$foodphoto_myfirstmodule$foodphoto_itemapi');
INSERT INTO "mendixsystem$index_column" ("index_id", "column_id", "sort_order", "ordinal") VALUES ('202c732a-3425-3a07-b577-14698c252a14', '3b00574e-5ccc-43cf-9d47-2a13943d9e99', false, 0);
INSERT INTO "mendixsystem$unique_constraint" ("name", "table_id", "column_id") VALUES ('uniq_myfirstmodule$foodphoto_myfirstmodule$foodphoto_itemapi', '6d3cc67c-5238-4667-a622-fce911897071', '3b00574e-5ccc-43cf-9d47-2a13943d9e99');
INSERT INTO "mendixsystem$association" ("id", "association_name", "table_name", "parent_entity_id", "child_entity_id", "parent_column_name", "child_column_name", "child_fkc_name", "child_fkc_action", "storage_format") VALUES ('3b00574e-5ccc-43cf-9d47-2a13943d9e99', 'MyFirstModule.FoodPhoto_ItemAPI', 'myfirstmodule$foodphoto', '6d3cc67c-5238-4667-a622-fce911897071', '537b28a9-dbca-4c42-b410-635e4c9ae32d', 'id', 'myfirstmodule$foodphoto_itemapi', 'frn_myfirstmodule$foodphoto_myfirstmodule$foodphoto_itemapi', 2, 1);
ALTER TABLE "myfirstmodule$order" ADD CONSTRAINT "frn_myfirstmodule$order_myfirstmodule$order_restaurantapi" FOREIGN KEY ( "myfirstmodule$order_restaurantapi" ) REFERENCES "myfirstmodule$restaurantapi" ( "id" ) ON DELETE SET NULL;
ALTER TABLE "myfirstmodule$itemapi" ADD CONSTRAINT "frn_myfirstmodule$itemapi_myfirstmodule$itemapi_orderitem" FOREIGN KEY ( "myfirstmodule$itemapi_orderitem" ) REFERENCES "myfirstmodule$orderitem" ( "id" ) ON DELETE SET NULL;
ALTER TABLE "myfirstmodule$itemapi" ADD CONSTRAINT "frn_myfirstmodule$itemapi_myfirstmodule$itemapi_restaurantapi" FOREIGN KEY ( "myfirstmodule$itemapi_restaurantapi" ) REFERENCES "myfirstmodule$restaurantapi" ( "id" ) ON DELETE SET NULL;
ALTER TABLE "myfirstmodule$itemapi" ADD CONSTRAINT "frn_myfirstmodule$itemapi_myfirstmodule$itemapi_order" FOREIGN KEY ( "myfirstmodule$itemapi_order" ) REFERENCES "myfirstmodule$order" ( "id" ) ON DELETE SET NULL;
ALTER TABLE "myfirstmodule$foodphoto" ADD CONSTRAINT "frn_myfirstmodule$foodphoto_myfirstmodule$foodphoto_itemapi" FOREIGN KEY ( "myfirstmodule$foodphoto_itemapi" ) REFERENCES "myfirstmodule$itemapi" ( "id" ) ON DELETE SET NULL;
DROP TABLE "4b180270ffc345459de199328532fe79";
DROP TABLE "3955302ef5e946d784c3e362aa582293";
UPDATE "mendixsystem$version" SET "versionnumber" = '4.2', "lastsyncdate" = '20260623 17:07:16';
