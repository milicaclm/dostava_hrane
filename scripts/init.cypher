
CREATE CONSTRAINT user_id_unique IF NOT EXISTS
FOR (u:User)
REQUIRE u.id IS UNIQUE;

CREATE CONSTRAINT user_email_unique IF NOT EXISTS
FOR (u:User)
REQUIRE u.email IS UNIQUE;

CREATE CONSTRAINT delivery_id_unique IF NOT EXISTS
FOR (d:Delivery)
REQUIRE d.id IS UNIQUE;

CREATE CONSTRAINT vehicle_license_unique IF NOT EXISTS
FOR (v:Vehicle)
REQUIRE v.license_plate IS UNIQUE;

CREATE CONSTRAINT product_id_unique IF NOT EXISTS
FOR (p:Product)
REQUIRE p.id IS UNIQUE;