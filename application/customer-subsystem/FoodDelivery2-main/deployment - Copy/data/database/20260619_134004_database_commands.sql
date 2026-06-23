CREATE TABLE "myfirstmodule$restaurantapi" (
	"id" BIGINT NOT NULL,
	"name" VARCHAR_IGNORECASE(30) NULL,
	"address" VARCHAR_IGNORECASE(30) NULL,
	"phone" VARCHAR_IGNORECASE(13) NULL,
	"email" VARCHAR_IGNORECASE(30) NULL,
	"description" VARCHAR_IGNORECASE(100) NULL,
	"workinghours" VARCHAR_IGNORECASE(30) NULL,
	"acceptsorders" BOOLEAN NULL,
	"unavailablereason" VARCHAR_IGNORECASE(50) NULL,
	"status" VARCHAR_IGNORECASE(30) NULL,
	"restaurantid" VARCHAR_IGNORECASE(10) NULL,
	"category" VARCHAR_IGNORECASE(30) NULL,
	"rating" DECIMAL(28, 8) NULL,
	PRIMARY KEY("id"));
INSERT INTO "mendixsystem$entity" ("id", "entity_name", "table_name", "remote", "remote_primary_key") VALUES ('736d9d96-2957-47c9-becf-9293091b1532', 'MyFirstModule.RestaurantAPI', 'myfirstmodule$restaurantapi', false, false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('bc857963-3208-4f37-b684-7825948815bb', '736d9d96-2957-47c9-becf-9293091b1532', 'name', 'name', 30, 30, '', false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('c8672e39-633d-4da4-9bda-18e19c5f588d', '736d9d96-2957-47c9-becf-9293091b1532', 'address', 'address', 30, 30, '', false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('6b6777a0-6aa1-479e-af64-3327a6c1ab9b', '736d9d96-2957-47c9-becf-9293091b1532', 'phone', 'phone', 30, 13, '', false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('9fe7b041-3384-4416-94e8-01374e9be384', '736d9d96-2957-47c9-becf-9293091b1532', 'email', 'email', 30, 30, '', false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('ec1c1980-edc2-442e-b489-fad8d1d2c671', '736d9d96-2957-47c9-becf-9293091b1532', 'description', 'description', 30, 100, '', false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('cadcae39-729f-4831-b339-49eefeb6f9f3', '736d9d96-2957-47c9-becf-9293091b1532', 'workingHours', 'workinghours', 30, 30, '', false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('34a445ee-8bbd-43df-8775-a7ae4851f415', '736d9d96-2957-47c9-becf-9293091b1532', 'acceptsOrders', 'acceptsorders', 10, 0, 'false', false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('da89212c-ef7a-4815-98b6-40eaa9e7f86a', '736d9d96-2957-47c9-becf-9293091b1532', 'unavailableReason', 'unavailablereason', 30, 50, '', false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('a67b737a-e0c7-41c3-89db-a090acfa99f3', '736d9d96-2957-47c9-becf-9293091b1532', 'status', 'status', 30, 30, '', false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('81f4c622-3370-4c39-b2ab-76369c21a922', '736d9d96-2957-47c9-becf-9293091b1532', 'restaurantId', 'restaurantid', 30, 10, '', false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('4040aa5d-6359-4fd4-ad8f-b1e4f4b7453c', '736d9d96-2957-47c9-becf-9293091b1532', 'category', 'category', 30, 30, '', false);
INSERT INTO "mendixsystem$attribute" ("id", "entity_id", "attribute_name", "column_name", "type", "length", "default_value", "is_auto_number") VALUES ('c675032b-797f-493f-9a68-166b0dcf9984', '736d9d96-2957-47c9-becf-9293091b1532', 'rating', 'rating', 5, 0, '0', false);
UPDATE "mendixsystem$version" SET "versionnumber" = '4.2', "lastsyncdate" = '20260619 13:40:04';
