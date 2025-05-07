document.addEventListener('DOMContentLoaded', function () {
    function registerSearchButtonHandler() {
        const searchButton = document.getElementById('search-icon');
        searchButton.addEventListener('click', function () {
            const query = document.getElementById('search-input').value;

            fetch(`/properties/api/search/?property_search=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    const list = document.getElementById('result-list');
                    list.innerHTML = "";

                    data.data.forEach(item => {
                        const li = document.createElement('li');
                        li.textContent = `${item.title} – ${item.address} – ${item.price} kr`;
                        list.appendChild(li);
                    });

                    if (data.data.length === 0) {
                        list.innerHTML = "<li>No results found.</li>";
                    }
                });
        });
    }

    registerSearchButtonHandler();
});
