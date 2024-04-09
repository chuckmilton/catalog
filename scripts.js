/**
 * Data Catalog Project Starter Code - SEA Stage 2
 *
 * This file is where you should be doing most of your work. You should
 * also make changes to the HTML and CSS files, but we want you to prioritize
 * demonstrating your understanding of data structures, and you'll do that
 * with the JavaScript code you write in this file.
 * 
 * The comments in this file are only to help you learn how the starter code
 * works. The instructions for the project are in the README. That said, here
 * are the three things you should do first to learn about the starter code:
 * - 1 - Change something small in index.html or style.css, then reload your 
 *    browser and make sure you can see that change. 
 * - 2 - On your browser, right click anywhere on the page and select
 *    "Inspect" to open the browser developer tools. Then, go to the "console"
 *    tab in the new window that opened up. This console is where you will see
 *    JavaScript errors and logs, which is extremely helpful for debugging.
 *    (These instructions assume you're using Chrome, opening developer tools
 *    may be different on other browsers. We suggest using Chrome.)
 * - 3 - Add another string to the titles array a few lines down. Reload your
 *    browser and observe what happens. You should see a fourth "card" appear
 *    with the string you added to the array, but a broken image.
 * 
 */

let items = [];
let blocks = [];
let mobs = [];
let all = [];

// Sorts all data in alphabetical order
function sortAllData() {
    all.sort((a, b) => a.name.localeCompare(b.name));
}

// Load all items
function loadItems() {
    fetch('./data/items_data.json')
        .then(response => response.json())
        .then(data => {
            items = data.map(item => ({ ...item, category: 'Items' }));
            all.push(...items);
            if (all.length === items.length + blocks.length + mobs.length) {
                sortAllData();
                showCards(all);
            }
        })
        .catch(error => console.error('Error loading items:', error));
}

// Load all blocks
function loadBlocks() {
    fetch('./data/blocks_data.json')
        .then(response => response.json())
        .then(data => {
            blocks = data.map(block => ({ ...block, category: 'Blocks' }));
            all.push(...blocks);
            if (all.length === items.length + blocks.length + mobs.length) {
                sortAllData();
                showCards(all);
            }
        })
        .catch(error => console.error('Error loading blocks:', error));
}

// Load all mobs
function loadMobs() {
    fetch('./data/mobs_data.json')
        .then(response => response.json())
        .then(data => {
            mobs = data.map(mob => ({ ...mob, category: 'Mobs' }));
            all.push(...mobs);
            if (all.length === items.length + blocks.length + mobs.length) {
                sortAllData();
                showCards(all);
            }
        })
        .catch(error => console.error('Error loading mobs:', error));
}

// Display cards
function showCards(filteredItems = items) {
    const cardContainer = document.getElementById("card-container");
    cardContainer.innerHTML = "";
    const templateCard = document.querySelector(".card");
    
    for (let i = 0; i < filteredItems.length; i++) {
        let item = filteredItems[i];

        const nextCard = templateCard.cloneNode(true); // Copy the template card
        editCardContent(nextCard, item); // Pass the item object to editCardContent
        cardContainer.appendChild(nextCard); // Add new card to the container
    }
}

// Card content
function editCardContent(card, data) {
    card.style.display = "block";

    const cardHeader = card.querySelector("h2");
    cardHeader.textContent = data.name;

    const cardLink = card.querySelector(".item-link");
    cardLink.href = data.link;

    const cardImage = card.querySelector(".item-image");
    cardImage.src = `https://minecraft.wiki${data.image_url}`;
    cardImage.alt = data.name;
    cardImage.style.width = "auto";
    cardImage.style.height = "auto";

    const checkbox = card.querySelector(".favorite-checkbox");
    checkbox.checked = isFavorite(data.name);
    checkbox.addEventListener("change", (event) => {
        if (event.target.checked) {
            addToFavorites(data);
        } else {
            removeFromFavorites(data);
        }
    });
}

// Favorites Functions
function isFavorite(itemName) {
    const favorites = JSON.parse(localStorage.getItem("favorites")) || [];
    return favorites.some(fav => fav.name === itemName);
}

function addToFavorites(item) {
    const favorites = JSON.parse(localStorage.getItem("favorites")) || [];
    favorites.push(item);
    localStorage.setItem("favorites", JSON.stringify(favorites));
}


function removeFromFavorites(item) {
    let favorites = JSON.parse(localStorage.getItem("favorites")) || [];
    favorites = favorites.filter(fav => fav.name !== item.name);
    localStorage.setItem("favorites", JSON.stringify(favorites));
}

function showFavorites() {
    const favorites = JSON.parse(localStorage.getItem("favorites")) || [];
    showCards(favorites);
}

// Load content
document.addEventListener("DOMContentLoaded", () => {
    loadItems();
    loadBlocks();
    loadMobs();
});

// Filtering content
function filterByCategory(category) {
    let filteredData;
    if (category === "All") {
        filteredData = all;
    } else if (category === "Items") {
        filteredData = items;
    } else if (category === "Blocks") {
        filteredData = blocks;
    } else if (category === "Mobs") {
        filteredData = mobs;
    } else if (category === "Favorites") {
        showFavorites();
        return;
    } else {
        filteredData = all.filter(item => item.category === category);
    }
    filteredData.sort((a, b) => a.name.localeCompare(b.name));
    showCards(filteredData);
}


// Search in content
function searchItems() {
    const searchQuery = document.getElementById("search-input").value.toLowerCase();
    const filteredData = [...items, ...blocks, ...mobs].filter(data => data.name.toLowerCase().includes(searchQuery));
    showCards(filteredData);
}
