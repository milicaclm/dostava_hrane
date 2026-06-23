CREATE TABLE "myfirstmodule$restaurant" (
	"id" BIGINT NOT NULL,
	"name" VARCHAR_IGNORECASE(200) NULL,
	"description" VARCHAR_IGNORECASE(200) NULL,
	"rating" DECIMAL(28, 8) NULL,
	PRIMARY KEY("id"));
INSERT INTO "mendixsystem$entity" ("id", "entity_name", "table_name", "remote", "remote_primary_key") VALUES ('718e4aa1-e0e4-4211-924d-0c7df14ea272', 'MyFirstModule.Restaurant', 'myfirstmodule$restaurant', false, false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('9bb4bedd-5012-424b-b2a5-f8c9eb8ce4d1', '718e4aa1-e0e4-4211-924d-0c7df14ea272', 'Name', 'name', 30, 200, '', false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('86ad2681-177a-4051-96d8-3cca9a5e7cfb', '718e4aa1-e0e4-4211-924d-0c7df14ea272', 'Description', 'description', 30, 200, '', false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('c2eaf69f-95b4-4d8b-bd7b-99c95aa5879f', '718e4aa1-e0e4-4211-924d-0c7df14ea272', 'Rating', 'rating', 5, 0, '0', false);
CREATE TABLE "myfirstmodule$menuitem" (
	"id" BIGINT NOT NULL,
	"name" VARCHAR_IGNORECASE(200) NULL,
	"price" DECIMAL(28, 8) NULL,
	"description" VARCHAR_IGNORECASE(200) NULL,
	"myfirstmodule$menuitem_order" BIGINT NULL,
	"myfirstmodule$menuitem_restaurant" BIGINT NULL,
	PRIMARY KEY("id"));
CREATE INDEX "idx_myfirstmodule$menuitem_myfirstmodule$menuitem_order" ON "myfirstmodule$menuitem" ("myfirstmodule$menuitem_order" ASC,"id" ASC);
CREATE INDEX "idx_myfirstmodule$menuitem_myfirstmodule$menuitem_restaurant" ON "myfirstmodule$menuitem" ("myfirstmodule$menuitem_restaurant" ASC,"id" ASC);
INSERT INTO "mendixsystem$entity" ("id", "entity_name", "table_name", "remote", "remote_primary_key") VALUES ('e9aa1047-afa3-4dd0-88b3-541716571542', 'MyFirstModule.MenuItem', 'myfirstmodule$menuitem', false, false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('869a1071-c24f-4c35-8bc3-d7ec9117692b', 'e9aa1047-afa3-4dd0-88b3-541716571542', 'Name', 'name', 30, 200, '', false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('ca0d03b8-8361-4457-8551-73d2d47cd51a', 'e9aa1047-afa3-4dd0-88b3-541716571542', 'Price', 'price', 5, 0, '0', false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('4d6e56aa-fadf-4ed0-8617-ac01a85a1d0e', 'e9aa1047-afa3-4dd0-88b3-541716571542', 'Description', 'description', 30, 200, '', false);
INSERT INTO "mendixsystem$index" ("id", "table_id", "index_name") VALUES ('03cd4812-6a4e-303f-aa8f-e5c052a126a2', 'e9aa1047-afa3-4dd0-88b3-541716571542', 'idx_myfirstmodule$menuitem_myfirstmodule$menuitem_order');
INSERT INTO "mendixsystem$index_column" ("index_id", "column_id", "sort_order", "ordinal") VALUES ('03cd4812-6a4e-303f-aa8f-e5c052a126a2', '02bae1e3-ca14-49f8-8187-79e3f5e5ac34', false, 0);
INSERT INTO "mendixsystem$index" ("id", "table_id", "index_name") VALUES ('da103443-6170-3ad7-988e-9c0c9db21f24', 'e9aa1047-afa3-4dd0-88b3-541716571542', 'idx_myfirstmodule$menuitem_myfirstmodule$menuitem_restaurant');
INSERT INTO "mendixsystem$index_column" ("index_id", "column_id", "sort_order", "ordinal") VALUES ('da103443-6170-3ad7-988e-9c0c9db21f24', 'ceac46e3-ab71-42d1-8fb1-745c9bfc27fc', false, 0);
INSERT INTO "mendixsystem$association" ("id", "association_name", "table_name", "parent_entity_id", "child_entity_id", "parent_column_name", "child_column_name", "child_fkc_name", "child_fkc_action", "storage_format") VALUES ('02bae1e3-ca14-49f8-8187-79e3f5e5ac34', 'MyFirstModule.MenuItem_Order', 'myfirstmodule$menuitem', 'e9aa1047-afa3-4dd0-88b3-541716571542', 'a5baea4c-17c2-4f38-9dde-754dbfa493a4', 'id', 'myfirstmodule$menuitem_order', 'frn_myfirstmodule$menuitem_myfirstmodule$menuitem_order', 2, 1);
INSERT INTO "mendixsystem$association" ("id", "association_name", "table_name", "parent_entity_id", "child_entity_id", "parent_column_name", "child_column_name", "child_fkc_name", "child_fkc_action", "storage_format") VALUES ('ceac46e3-ab71-42d1-8fb1-745c9bfc27fc', 'MyFirstModule.MenuItem_Restaurant', 'myfirstmodule$menuitem', 'e9aa1047-afa3-4dd0-88b3-541716571542', '718e4aa1-e0e4-4211-924d-0c7df14ea272', 'id', 'myfirstmodule$menuitem_restaurant', 'frn_myfirstmodule$menuitem_myfirstmodule$menuitem_restaurant', 2, 1);
ALTER TABLE "myfirstmodule$menuitem" ADD CONSTRAINT "frn_myfirstmodule$menuitem_myfirstmodule$menuitem_order" FOREIGN KEY ( "myfirstmodule$menuitem_order" ) REFERENCES "myfirstmodule$order" ( "id" ) ON DELETE SET NULL;
ALTER TABLE "myfirstmodule$menuitem" ADD CONSTRAINT "frn_myfirstmodule$menuitem_myfirstmodule$menuitem_restaurant" FOREIGN KEY ( "myfirstmodule$menuitem_restaurant" ) REFERENCES "myfirstmodule$restaurant" ( "id" ) ON DELETE SET NULL;
UPDATE "mendixsystem$version" SET "versionnumber" = '4.2', "lastsyncdate" = '20260613 19:44:42';
