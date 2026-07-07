


CREATE
  (manager:User
    {
      id: 'user-mgr',
      name: 'Pera',
      surname: 'Menadžer',
      password: 'pass1234',
      account_type: 'manager',
      email: 'manager@dostava.com',
      phone_number: '+381640000000',
      is_active: true
    });


CREATE
  (admin:User
    {
      id: 'user-admin',
      name: 'Ana',
      surname: 'Admin',
      password: 'pass1234',
      account_type: 'admin',
      email: 'admin@dostava.com',
      phone_number: '+381640000001',
      is_active: true
    });


CREATE
  (d1:User
    {
      id: 'user-del-1',
      name: 'Marko',
      surname: 'Markovic',
      password: 'pass1234',
      account_type: 'courier',
      email: 'marko@dostava.com',
      phone_number: '+381641111111',
      is_active: true,
      motorcycle_license: true,
      car_license: false,
      salary: 60000.0,
      average_rating: 4.8
    });
CREATE
  (d2:User
    {
      id: 'user-del-2',
      name: 'Jovan',
      surname: 'Jovanovic',
      password: 'pass1234',
      account_type: 'courier',
      email: 'jovan@dostava.com',
      phone_number: '+381641111112',
      is_active: true,
      motorcycle_license: false,
      car_license: true,
      salary: 55000.0,
      average_rating: 4.5
    });
CREATE
  (d3:User
    {
      id: 'user-del-3',
      name: 'Lazar',
      surname: 'Lazarevic',
      password: 'pass1234',
      account_type: 'courier',
      email: 'lazar@dostava.com',
      phone_number: '+381641111113',
      is_active: true,
      motorcycle_license: true,
      car_license: true,
      salary: 65000.0,
      average_rating: 5.0
    });
CREATE
  (d4:User
    {
      id: 'user-del-4',
      name: 'Goran',
      surname: 'Gojkovic',
      password: 'pass1234',
      account_type: 'courier',
      email: 'goran@dostava.com',
      phone_number: '+381641111114',
      is_active: false,
      motorcycle_license: true,
      car_license: false,
      salary: 45000.0,
      average_rating: 3.9
    });


CREATE
  (c1:User
    {
      id: 'user-cust-1',
      name: 'Ivan',
      surname: 'Ivic',
      password: 'pass1234',
      account_type: 'customer',
      email: 'ivan@gmail.com',
      phone_number: '+381642222221',
      is_active: true
    });
CREATE
  (c2:User
    {
      id: 'user-cust-2',
      name: 'Milica',
      surname: 'Milic',
      password: 'pass1234',
      account_type: 'customer',
      email: 'milica@gmail.com',
      phone_number: '+381642222222',
      is_active: true
    });
CREATE
  (c3:User
    {
      id: 'user-cust-3',
      name: 'Nikola',
      surname: 'Nikolic',
      password: 'pass1234',
      account_type: 'customer',
      email: 'nikola@gmail.com',
      phone_number: '+381642222223',
      is_active: true
    });
CREATE
  (c4:User
    {
      id: 'user-cust-4',
      name: 'Petra',
      surname: 'Petrovic',
      password: 'pass1234',
      account_type: 'customer',
      email: 'petra@gmail.com',
      phone_number: '+381642222224',
      is_active: true
    });
CREATE
  (c5:User
    {
      id: 'user-cust-5',
      name: 'Dragan',
      surname: 'Dragic',
      password: 'pass1234',
      account_type: 'customer',
      email: 'dragan@gmail.com',
      phone_number: '+381642222225',
      is_active: true
    });
CREATE
  (c6:User
    {
      id: 'user-cust-6',
      name: 'Jovana',
      surname: 'Jovanovic',
      password: 'pass1234',
      account_type: 'customer',
      email: 'jovana@gmail.com',
      phone_number: '+381642222226',
      is_active: true
    });
CREATE
  (c7:User
    {
      id: 'user-cust-7',
      name: 'Aleksa',
      surname: 'Aleksandric',
      password: 'pass1234',
      account_type: 'customer',
      email: 'aleksa@gmail.com',
      phone_number: '+381642222227',
      is_active: true
    });
CREATE
  (c8:User
    {
      id: 'user-cust-8',
      name: 'Slavka',
      surname: 'Slavkovic',
      password: 'pass1234',
      account_type: 'customer',
      email: 'slavka@gmail.com',
      phone_number: '+381642222228',
      is_active: true
    });
CREATE
  (c9:User
    {
      id: 'user-cust-9',
      name: 'Bojan',
      surname: 'Bojic',
      password: 'pass1234',
      account_type: 'customer',
      email: 'bojan@gmail.com',
      phone_number: '+381642222229',
      is_active: true
    });


CREATE
  (v1:Vehicle
    {
      id: 'v-1',
      owner_id: 'user-mgr',
      type: 'bike',
      license_plate: 'BG-1234',
      is_ready: true,
      brand: 'Yamaha',
      model: 'MT-07',
      color: 'Crvena',
      description: 'Brzi motor za dostavu'
    });
CREATE
  (v2:Vehicle
    {
      id: 'v-2',
      owner_id: 'user-mgr',
      type: 'car',
      license_plate: 'NS-5678',
      is_ready: true,
      brand: 'Fiat',
      model: 'Panda',
      color: 'Bela',
      description: 'Mali gradski auto'
    });


CREATE
  (p1:Product
    {
      id: 'prod-1',
      name: 'Pizza Margherita',
      description: 'Classic pizza with tomato and cheese',
      price: 6.5
    });
CREATE
  (p2:Product
    {
      id: 'prod-2',
      name: 'Salmon Roll',
      description: 'Fresh salmon with rice and seaweed',
      price: 8.99
    });
CREATE
  (p3:Product
    {
      id: 'prod-3',
      name: 'Cheese Burger',
      description: 'Juicy burger with melted cheese',
      price: 5.99
    });



CREATE
  (del1:Delivery
    {
      id: 'del-1',
      status: 'completed',
      from_location: 'Pizza Palace',
      to_location: 'Srpske Garde 15',
      order_time: datetime('2026-04-29T10:00:00'),
      start_time: datetime('2026-04-29T10:05:00'),
      pickup_time: datetime('2026-04-29T10:15:00'),
      delivery_time: datetime('2026-04-29T10:30:00'),
      rating: 5
    });
CREATE (c1)-[:PLACED_ORDER]->(del1);
CREATE (d1)-[:ASSIGNED_TO]->(del1);
CREATE (del1)-[:CONTAINS_PRODUCT]->(p1);
CREATE (d1)-[:USES_VEHICLE]->(v1);


CREATE
  (del2:Delivery
    {
      id: 'del-2',
      status: 'completed',
      from_location: 'Sushi House',
      to_location: 'Bulevar Oslobođenja 10',
      order_time: datetime('2026-04-29T11:00:00'),
      start_time: datetime('2026-04-29T11:05:00'),
      pickup_time: datetime('2026-04-29T11:15:00'),
      delivery_time: datetime('2026-04-29T11:40:00'),
      rating: 4
    });
CREATE (c2)-[:PLACED_ORDER]->(del2);
CREATE (d2)-[:ASSIGNED_TO]->(del2);
CREATE (del2)-[:CONTAINS_PRODUCT]->(p2);
CREATE (d2)-[:USES_VEHICLE]->(v2);


CREATE
  (del3:Delivery
    {
      id: 'del-3',
      status: 'in_transit',
      from_location: 'Burger Station',
      to_location: 'Terazije 45',
      order_time: datetime('2026-04-29T12:00:00'),
      start_time: datetime('2026-04-29T12:05:00'),
      pickup_time: datetime('2026-04-29T12:20:00')
    });
CREATE (c3)-[:PLACED_ORDER]->(del3);
CREATE (d3)-[:ASSIGNED_TO]->(del3);
CREATE (del3)-[:CONTAINS_PRODUCT]->(p3);
CREATE (d3)-[:USES_VEHICLE]->(v1);


CREATE
  (del4:Delivery
    {
      id: 'del-4',
      status: 'pending',
      from_location: 'Pizza Palace',
      to_location: 'Kosovska 20',
      order_time: datetime('2026-04-29T13:00:00')
    });
CREATE (c4)-[:PLACED_ORDER]->(del4);
CREATE (d4)-[:ASSIGNED_TO]->(del4);
CREATE (del4)-[:CONTAINS_PRODUCT]->(p1);
CREATE (d4)-[:USES_VEHICLE]->(v2);


CREATE
  (del5:Delivery
    {
      id: 'del-5',
      status: 'completed',
      from_location: 'Sushi House',
      to_location: 'Palmoticeva 8',
      order_time: datetime('2026-04-29T14:00:00'),
      start_time: datetime('2026-04-29T14:02:00'),
      pickup_time: datetime('2026-04-29T14:15:00'),
      delivery_time: datetime('2026-04-29T14:45:00'),
      rating: 5
    });
CREATE (c5)-[:PLACED_ORDER]->(del5);
CREATE (d1)-[:ASSIGNED_TO]->(del5);
CREATE (del5)-[:CONTAINS_PRODUCT]->(p2);
CREATE (d1)-[:USES_VEHICLE]->(v2);


CREATE
  (del6:Delivery
    {
      id: 'del-6',
      status: 'completed',
      from_location: 'Burger Station',
      to_location: 'Kneza Mihailova 55',
      order_time: datetime('2026-04-29T15:00:00'),
      start_time: datetime('2026-04-29T15:05:00'),
      pickup_time: datetime('2026-04-29T15:20:00'),
      delivery_time: datetime('2026-04-29T15:55:00'),
      rating: 3
    });
CREATE (c6)-[:PLACED_ORDER]->(del6);
CREATE (d2)-[:ASSIGNED_TO]->(del6);
CREATE (del6)-[:CONTAINS_PRODUCT]->(p3);
CREATE (d2)-[:USES_VEHICLE]->(v1);


CREATE
  (del7:Delivery
    {
      id: 'del-7',
      status: 'in_transit',
      from_location: 'Pizza Palace',
      to_location: 'Krunska 30',
      order_time: datetime('2026-04-29T16:00:00'),
      start_time: datetime('2026-04-29T16:10:00'),
      pickup_time: datetime('2026-04-29T16:30:00')
    });
CREATE (c7)-[:PLACED_ORDER]->(del7);
CREATE (d3)-[:ASSIGNED_TO]->(del7);
CREATE (del7)-[:CONTAINS_PRODUCT]->(p1);
CREATE (d3)-[:USES_VEHICLE]->(v2);


CREATE
  (del8:Delivery
    {
      id: 'del-8',
      status: 'pending',
      from_location: 'Sushi House',
      to_location: 'Nemanjina 12',
      order_time: datetime('2026-04-29T17:00:00')
    });
CREATE (c8)-[:PLACED_ORDER]->(del8);
CREATE
  (d4)-[:OFFERED {ts: datetime('2026-04-29T17:01:00'), status: 'offered'}]->
  (del8);
CREATE (del8)-[:CONTAINS_PRODUCT]->(p2);


CREATE
  (del9:Delivery
    {
      id: 'del-9',
      status: 'pending',
      from_location: 'Burger Station',
      to_location: 'Vukov Spomenar 3',
      order_time: datetime('2026-04-29T18:00:00')
    });
CREATE (c9)-[:PLACED_ORDER]->(del9);
CREATE
  (d1)-[:OFFERED {ts: datetime('2026-04-29T18:01:00'), status: 'offered'}]->
  (del9);
CREATE (del9)-[:CONTAINS_PRODUCT]->(p3);