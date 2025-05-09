document.addEventListener('DOMContentLoaded', function () {

    function formatPrice(price) {
        return price.toLocaleString('is-IS'); // adds dots for thousands
    }

    function performSearch() {
        const query = document.getElementById('search-input').value;
        const postalCode = document.getElementById('postal-code').value;
        const minPrice = document.getElementById('min-price').value;
        const maxPrice = document.getElementById('max-price').value;
        const minSize = document.getElementById('min-size').value;
        const maxSize = document.getElementById('max-price').value;
        const propertyType = document.getElementById('property-type').value;
        const ordering = document.getElementById('order-by').value;


        const params = new URLSearchParams({
            property_search: query,
            postal_code: postalCode,
            min_price: minPrice,
            max_price: maxPrice,
            min_size: minSize,
            max_size: maxSize,
            property_type: propertyType,
            ordering: ordering
        });

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
                                <p class="card-text"><strong>Size:</strong> ${property.size_sqm} m²</p>
                                <a href="/properties/${property.id}/" class="btn btn-sm btn-outline-primary mt-2">View Details</a>
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
