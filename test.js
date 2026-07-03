
        const API_DELIVERIES_URL = 'http://localhost:8000/api/delivery-subsystem/deliveries';
        const API_USERS_URL = 'http://localhost:8000/api/delivery-subsystem/users';
        const API_LOCATIONS_URL = 'http://localhost:8000/api/delivery-subsystem/locations';

        let map = null;
        let courierMarker = null;
        let pickupMarker = null;
        let deliveryMarker = null;
        let routeLine = null;
        let currentDelivery = null;
        let currentStatus = null;
        let trackingInterval = null;
        let checkInterval = null;

        function getToken() { return localStorage.getItem('jwt_token') || parent.localStorage.getItem('jwt_token'); }
        function getUserId() {
            try { return JSON.parse(atob(getToken().split('.')[1].replace(/-/g, '+').replace(/_/g, '/'))).sub; } 
            catch (e) { return null; }
        }
        function getDeliveryIdFromUrl() { return new URLSearchParams(window.location.search).get('id'); }

        function showToast(msg) {
            const toast = document.getElementById('toast');
            toast.textContent = msg;
            toast.style.display = 'block';
            setTimeout(() => toast.style.display = 'none', 3000);
        }

        function formatDateTime(dtStr) {
            if (!dtStr) return '—';
            try { return new Date(dtStr.replace(' ', 'T')).toLocaleString('sr-Latn'); } 
            catch (e) { return dtStr; }
        }

        function statusLabel(status) {
            const map = { 'accepted': 'Prihvaćena', 'in transit': 'U dostavi', 'completed': 'Isporučena', 'cancelled': 'Otkazana' };
            return map[status] || status;
        }

        function updateStatusUI(status) {
            currentStatus = status;
            if (['accepted', 'in transit', 'completed', 'cancelled'].includes(status) && checkInterval) {
                clearInterval(checkInterval);
                checkInterval = null;
            }
            document.getElementById('status-text').textContent = statusLabel(status);
            renderActions(status);
        }

        function renderActions(status) {
            const section = document.getElementById('actions-section');
            if (['offered', 'pending', 'placed'].includes(status)) {
                section.innerHTML = `
                    <button onclick="doAcceptOffer()">Prihvati</button>
                    <button onclick="doRejectOffer()">Odbij</button>
                `;
            } else if (status === 'accepted') {
                section.innerHTML = `
                    <button onclick="doPickup()">Preuzeo sam</button>
                    <button onclick="doCancel()">Otkaži</button>
                `;
            } else if (status === 'in transit') {
                section.innerHTML = `
                    <button onclick="doDeliver()">Isporučeno</button>
                    <button onclick="doCancel()">Otkaži</button>
                `;
            } else {
                section.innerHTML = `<p>Ova dostava je završena ili otkazana.</p>`;
            }
        }

        async function doAcceptOffer() {
            try {
                const res = await fetch(`${API_DELIVERIES_URL}/${getDeliveryIdFromUrl()}/accept`, {
                    method: 'POST',
                    headers: { 'Authorization': `Bearer ${getToken()}`, 'Content-Type': 'application/json' },
                    body: JSON.stringify({ user_id: getUserId() })
                });
                if (res.ok) { showToast('Prihvaćeno!'); updateStatusUI('accepted'); } 
                else { showToast('Greška'); }
            } catch (e) { showToast('Mrežna greška'); }
        }

        async function doRejectOffer() {
            try {
                const res = await fetch(`${API_DELIVERIES_URL}/${getDeliveryIdFromUrl()}/reject`, {
                    method: 'POST',
                    headers: { 'Authorization': `Bearer ${getToken()}`, 'Content-Type': 'application/json' },
                    body: JSON.stringify({ courier_id: getUserId() })
                });
                if (res.ok) { showToast('Odbijeno'); updateStatusUI('cancelled'); }
            } catch (e) { showToast('Mrežna greška'); }
        }

        function initMap(restaurantLat, restaurantLon, customerLat, customerLon) {
            let centerLat = restaurantLat || customerLat || 45.25;
            let centerLon = restaurantLon || customerLon || 19.83;
            if (restaurantLat && customerLat) {
                centerLat = (restaurantLat + customerLat) / 2;
                centerLon = (restaurantLon + customerLon) / 2;
            }
            map = L.map('map').setView([centerLat, centerLon], 14);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(map);

            if (restaurantLat && restaurantLon) { pickupMarker = L.marker([restaurantLat, restaurantLon]).bindPopup('Restoran').addTo(map); }
            if (customerLat && customerLon) { deliveryMarker = L.marker([customerLat, customerLon]).bindPopup('Kupac').addTo(map); }
            if (restaurantLat && customerLat) {
                routeLine = L.polyline([[restaurantLat, restaurantLon], [customerLat, customerLon]], { color: 'blue' }).addTo(map);
                map.fitBounds(routeLine.getBounds());
            }

            map.on('click', function (e) { placeCourierMarker(e.latlng.lat, e.latlng.lng, true); });
        }

        function placeCourierMarker(lat, lon, fromClick = false) {
            if (courierMarker) { courierMarker.setLatLng([lat, lon]); } 
            else { courierMarker = L.marker([lat, lon]).bindPopup('Ti si ovde').addTo(map); }
            if (fromClick) showToast('Lokacija zabeležena');
            saveLocationToServer(lat, lon);
        }

        async function saveLocationToServer(lat, lon) {
            const userId = getUserId();
            const deliveryId = getDeliveryIdFromUrl();
            if (!userId || !deliveryId) return;
            try {
                await fetch(`${API_LOCATIONS_URL}/set_position?user_id=${userId}`, {
                    method: 'POST',
                    headers: { 'Authorization': `Bearer ${getToken()}`, 'Content-Type': 'application/json' },
                    body: JSON.stringify({ lat, lon, delivery_id: deliveryId })
                });
            } catch (e) { console.warn(e); }
        }

        function startPositionPolling() {
            const userId = getUserId();
            if (!userId || trackingInterval) return;
            trackingInterval = setInterval(async () => {
                try {
                    const res = await fetch(`${API_LOCATIONS_URL}/current_position?user_id=${userId}`, {
                        headers: { 'Authorization': `Bearer ${getToken()}` }
                    });
                    if (!res.ok) return;
                    const pos = await res.json();
                    if (!pos || pos.lat == null || pos.lon == null) return;
                    placeCourierMarker(parseFloat(pos.lat), parseFloat(pos.lon), false);
                } catch (e) { console.warn(e); }
            }, 4000);
        }

        async function doPickup() {
            try {
                const res = await fetch(`${API_DELIVERIES_URL}/${getDeliveryIdFromUrl()}/pickup`, {
                    method: 'POST',
                    headers: { 'Authorization': `Bearer ${getToken()}`, 'Content-Type': 'application/json' },
                    body: JSON.stringify({ courier_id: getUserId() })
                });
                if (res.ok) { showToast('Preuzeto!'); updateStatusUI('in transit'); }
            } catch (e) { showToast('Greška'); }
        }

        async function doDeliver() {
            try {
                const res = await fetch(`${API_DELIVERIES_URL}/${getDeliveryIdFromUrl()}/deliver`, {
                    method: 'POST',
                    headers: { 'Authorization': `Bearer ${getToken()}`, 'Content-Type': 'application/json' },
                    body: JSON.stringify({ courier_id: getUserId() })
                });
                if (res.ok) { 
                    showToast('Isporučeno!'); 
                    updateStatusUI('completed'); 
                    document.getElementById('delivery-time').textContent = formatDateTime(new Date().toISOString());
                }
            } catch (e) { showToast('Greška'); }
        }

        async function doCancel() {
            if (!confirm('Otkaži dostavu?')) return;
            try {
                const res = await fetch(`${API_DELIVERIES_URL}/${getDeliveryIdFromUrl()}/cancel`, {
                    method: 'POST',
                    headers: { 'Authorization': `Bearer ${getToken()}`, 'Content-Type': 'application/json' },
                    body: JSON.stringify({ courier_id: getUserId() })
                });
                if (res.ok) { showToast('Otkazano'); updateStatusUI('cancelled'); }
            } catch (e) { showToast('Greška'); }
        }

        async function loadDelivery() {
            const deliveryId = getDeliveryIdFromUrl();
            const token = getToken();
            if (!deliveryId || !token) { document.getElementById('actions-section').innerHTML = 'Greška.'; return; }

            document.getElementById('delivery-id-badge').textContent = '#' + deliveryId;
            try {
                const res = await fetch(`${API_DELIVERIES_URL}/${deliveryId}`, { headers: { 'Authorization': `Bearer ${token}` } });
                if (!res.ok) return;
                const d = await res.json();
                currentDelivery = d;
                
                document.getElementById('from-location').textContent = d.from_location || '—';
                document.getElementById('to-location').textContent = d.to_location || '—';
                document.getElementById('order-time').textContent = formatDateTime(d.order_time);
                document.getElementById('pickup-time').textContent = formatDateTime(d.pickup_time);
                document.getElementById('delivery-time').textContent = formatDateTime(d.delivery_time);

                const status = d.status || 'accepted';
                updateStatusUI(status);

                if (['offered', 'pending', 'placed'].includes(status)) {
                    checkInterval = setInterval(async () => {
                        try {
                            const offersRes = await fetch(`${API_DELIVERIES_URL}/offers`, { headers: { 'Authorization': `Bearer ${token}` } });
                            if (offersRes.ok) {
                                const offers = await offersRes.json();
                                if (!offers.some(o => o.id === deliveryId)) {
                                    clearInterval(checkInterval);
                                    showToast('Ponuda istekla');
                                }
                            }
                        } catch (err) {}
                    }, 3000);
                }

                initMap(parseFloat(d.restaurant_lat), parseFloat(d.restaurant_lon), parseFloat(d.customer_lat), parseFloat(d.customer_lon));
            } catch (e) { showToast('Greška učitavanja'); }
        }

        window.addEventListener('load', () => { loadDelivery(); startPositionPolling(); });
    