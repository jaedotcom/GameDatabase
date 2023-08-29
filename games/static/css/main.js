
    document.addEventListener("DOMContentLoaded", function () {
        const searchButton = document.querySelector("#search-button");

        searchButton.addEventListener("click", async function () {
            const searchInput = document.querySelector("#search-input").value;
            const selectedGenre = document.querySelector("#selected-genre").value;

            try {
                const response = await fetch(`/genreBar/${selectedGenre}?search=${searchInput}`);
                if (response.ok) {
                    const data = await response.json();
                    updateTable(data);
                } else {
                    console.error('Error fetching data:', response.statusText);
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        });

        function updateTable(data) {
            const tableBody = document.querySelector("#games-table-body");
            tableBody.innerHTML = "";  // Clear the existing content

            for (const game of data) {
                const row = document.createElement("tr");
                const titleCell = document.createElement("td");
                titleCell.textContent = game.title;
                const releaseDateCell = document.createElement("td");
                releaseDateCell.textContent = game.release_date;

                row.appendChild(titleCell);
                row.appendChild(releaseDateCell);
                tableBody.appendChild(row);
            }
        }
    });
