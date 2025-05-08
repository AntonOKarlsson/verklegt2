document.addEventListener('DOMContentLoaded', function () {
    function performSearch() {
        const query = document.getElementById('search-input').value;
        const postalCode = document.getElementById('postal-code').value;
        const minPrice = document.getElementById('min-price').value;
        const maxPrice = document.getElementById('max-price').value;
        const propertyType = document.getElementById('property-type').value;
        const ordering = document.getElementById('order-by').value;

        const params = new URLSearchParams({
            property_search: query,
            postal_code: postalCode,
            min_price: minPrice,
            max_price: maxPrice,
            property_type: propertyType,
            ordering: ordering
        });

        fetch(`/properties/api/search/?${params.toString()}`)
            .then(response => response.json())
            .then(data => {
                const list = document.getElementById('result-list');
                list.innerHTML = "";

                if (data.data.length === 0) {
                    list.innerHTML = "<li>No results found.</li>";
                    return;
                }

                data.data.forEach(item => {
                    const li = document.createElement('li');
                    li.textContent = `${item.title} – ${item.address} – ${item.price.toLocaleString()} kr`;
                    list.appendChild(li);
                });
            })
            .catch(error => {
                console.error("Search failed:", error);
                document.getElementById('result-list').innerHTML = "<li>Error loading results.</li>";
            });
    }

    function registerSearchButtonHandler() {
        const searchButton = document.getElementById('search-icon');
        searchButton.addEventListener('click', performSearch);
    }

    registerSearchButtonHandler();
});
