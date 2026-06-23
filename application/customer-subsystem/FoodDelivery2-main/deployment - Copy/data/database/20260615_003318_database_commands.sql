CREATE TABLE "myfirstmodule$orderitem" (
	"id" BIGINT NOT NULL,
	"quantity" INT NULL,
	"price" DECIMAL(28, 8) NULL,
	"myfirstmodule$orderitem_menuitem" BIGINT NULL,
	"myfirstmodule$orderitem_order" BIGINT NULL,
	PRIMARY KEY("id"));
CREATE INDEX "idx_myfirstmodule$orderitem_myfirstmodule$orderitem_menuitem" ON "myfirstmodule$orderitem" ("myfirstmodule$orderitem_menuitem" ASC,"id" ASC);
CREATE INDEX "idx_myfirstmodule$orderitem_myfirstmodule$orderitem_order" ON "myfirstmodule$orderitem" ("myfirstmodule$orderitem_order" ASC,"id" ASC);
INSERT INTO "mendixsystem$entity" ("id", "entity_name", "table_name", "remote", "remote_primary_key") VALUES ('c0fb1e35-e367-4403-a212-d1973ec3e7d3', 'MyFirstModule.OrderItem', 'myfirstmodule$orderitem', false, false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('62c61ece-3476-46ac-895d-baae494116a8', 'c0fb1e35-e367-4403-a212-d1973ec3e7d3', 'Quantity', 'quantity', 3, 0, '0', false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('164a6474-b3fe-4d15-9414-e6de40baabf4', 'c0fb1e35-e367-4403-a212-d1973ec3e7d3', 'Price', 'price', 5, 0, '0', false);
INSERT INTO "mendixsystem$index" ("id", "table_id", "index_name") VALUES ('b3afb00d-9128-30ea-999f-265d3aad97a8', 'c0fb1e35-e367-4403-a212-d1973ec3e7d3', 'idx_myfirstmodule$orderitem_myfirstmodule$orderitem_menuitem');
INSERT INTO "mendixsystem$index_column" ("index_id", "column_id", "sort_order", "ordinal") VALUES ('b3afb00d-9128-30ea-999f-265d3aad97a8', '49d2f328-cec0-43e2-8751-2d6a26c2af40', false, 0);
INSERT INTO "mendixsystem$index" ("id", "table_id", "index_name") VALUES ('a7c57bbc-77d0-3c91-8388-607bd20b1908', 'c0fb1e35-e367-4403-a212-d1973ec3e7d3', 'idx_myfirstmodule$orderitem_myfirstmodule$orderitem_order');
INSERT INTO "mendixsystem$index_column" ("index_id", "column_id", "sort_order", "ordinal") VALUES ('a7c57bbc-77d0-3c91-8388-607bd20b1908', 'afa22815-5fb6-4dc4-a7a2-5d6490bbec80', false, 0);
INSERT INTO "mendixsystem$association" ("id", "association_name", "table_name", "parent_entity_id", "child_entity_id", "parent_column_name", "child_column_name", "child_fkc_name", "child_fkc_action", "storage_format") VALUES ('49d2f328-cec0-43e2-8751-2d6a26c2af40', 'MyFirstModule.OrderItem_MenuItem', 'myfirstmodule$orderitem', 'c0fb1e35-e367-4403-a212-d1973ec3e7d3', 'e9aa1047-afa3-4dd0-88b3-541716571542', 'id', 'myfirstmodule$orderitem_menuitem', 'frn_myfirstmodule$orderitem_myfirstmodule$orderitem_menuitem', 2, 1);
INSERT INTO "mendixsystem$association" ("id", "association_name", "table_name", "parent_entity_id", "child_entity_id", "parent_column_name", "child_column_name", "child_fkc_name", "child_fkc_action", "storage_format") VALUES ('afa22815-5fb6-4dc4-a7a2-5d6490bbec80', 'MyFirstModule.OrderItem_Order', 'myfirstmodule$orderitem', 'c0fb1e35-e367-4403-a212-d1973ec3e7d3', 'a5baea4c-17c2-4f38-9dde-754dbfa493a4', 'id', 'myfirstmodule$orderitem_order', 'frn_myfirstmodule$orderitem_myfirstmodule$orderitem_order', 2, 1);
ALTER TABLE "myfirstmodule$orderitem" ADD CONSTRAINT "frn_myfirstmodule$orderitem_myfirstmodule$orderitem_menuitem" FOREIGN KEY ( "myfirstmodule$orderitem_menuitem" ) REFERENCES "myfirstmodule$menuitem" ( "id" ) ON DELETE SET NULL;
ALTER TABLE "myfirstmodule$orderitem" ADD CONSTRAINT "frn_myfirstmodule$orderitem_myfirstmodule$orderitem_order" FOREIGN KEY ( "myfirstmodule$orderitem_order" ) REFERENCES "myfirstmodule$order" ( "id" ) ON DELETE SET NULL;
UPDATE "mendixsystem$version" SET "versionnumber" = '4.2', "lastsyncdate" = '20260615 00:33:18';
