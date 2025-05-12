document.addEventListener('DOMContentLoaded', function () {

    function formatPrice(price) {
        return price.toLocaleString('is-IS'); // adds dots for thousands
    }

    function parseRange(value) {
        if (!value || value === '') return [null, null];
        if (value.endsWith('+')) {
            return [parseInt(value), null];
        }
        const parts = value.split('-');
        return [parseInt(parts[0]), parseInt(parts[1])];
    }

    function performSearch() {
        const query = document.getElementById('search-input').value;
        const postalCode = document.getElementById('postal-code').value;
        const propertyType = document.getElementById('property-type').value;
        const ordering = document.getElementById('order-by').value;

        const [minPrice, maxPrice] = parseRange(document.getElementById('price-range').value);
        const [minSize, maxSize] = parseRange(document.getElementById('size-range').value);
        const [minRooms, maxRooms] = parseRange(document.getElementById('room-range').value);

        const params = new URLSearchParams({
            property_search: query,
            postal_code: postalCode,
            property_type: propertyType,
            ordering: ordering,
        });

        if (minPrice !== null) params.append('min_price', minPrice);
        if (maxPrice !== null) params.append('max_price', maxPrice);
        if (minSize !== null) params.append('min_size', minSize);
        if (maxSize !== null) params.append('max_size', maxSize);
        if (minRooms !== null) params.append('min_rooms', minRooms);
        if (maxRooms !== null) params.append('max_rooms', maxRooms);

        fetch(`/properties/api/search/?${params.toString()}`)
            .then(response => response.json())
            .then(data => {
                const container = document.getElementById('result-list');
                container.innerHTML = '';

                if (data.data.length === 0) {
                    container.innerHTML = '<p>No results found.</p>';
                    return;
                }

                data.data.forEach(property => {
                    const col = document.createElement('div');
                    col.className = 'col-12 col-sm-6 col-md-4 mb-4';

                    const imageUrl = property.thumbnail_url || '/static/images/property_placeholder.png';

                    col.innerHTML = `
                        <div class="card h-100">
                            <a href="/properties/${property.id}/">
                                <img src="${imageUrl}" class="card-img-top" alt="${property.title}">
                            </a>
                            <div class="card-body">
                                <h5 class="card-title">
                                    <a href="/properties/${property.id}/" class="text-decoration-none">${property.title}</a>
                                </h5>
                                <p class="card-text"><strong>Price:</strong> ${formatPrice(property.price)} kr</p>
                                <p class="card-text"><strong>Address:</strong> ${property.address}</p>
                                <p class="card-text"><strong>Rooms:</strong> ${property.num_rooms ?? '—'}</p>
                                <p class="card-text"><strong>Size:</strong> ${property.size_sqm ? Math.round(Number(property.size_sqm)) + ' m²' : '— m²'}</p>
                            </div>
                        </div>
                    `;

                    container.appendChild(col);
                });
            })
            .catch(error => {
                console.error("Search failed:", error);
                const container = document.getElementById('result-list');
                container.innerHTML = '<p>Error loading results.</p>';
            });
    }

    function registerSearchButtonHandler() {
        const searchButton = document.getElementById('search-icon');
        searchButton.addEventListener('click', performSearch);
    }

    registerSearchButtonHandler();
});
