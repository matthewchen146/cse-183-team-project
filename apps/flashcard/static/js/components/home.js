import DeckItem from './deck-item.js';

export default await {
    components: {
        DeckItem
    },
    data() {
        return {
            decksUrl: urlFromRoot('decks'),
            decks: [],
            search: "",
            searchTimeout: undefined,
            searchTimeoutMs: 1000
        }
    },
    methods: {
        async clearSearch() {
            try {
                this.search = '';
                this.getDecks();
            } catch (error) {
                console.error('clearSearch error:', error)
            }
        },
        async getDecks() {
            // Clear the search timeout just in case it is still active (such as when pressing enter)
            clearTimeout(this.searchTimeout);

            try {
                // Make a GET request for decks depending on the search query and mode.
                const search = this.search;
                const mode = document.getElementById("mode").value;
                const result = await axios.get('get_decks', { params: { search: search, mode: mode } });

                // Process results for display.
                const decks = this.decks;
                const new_decks = result.data.decks;
                new_decks.forEach(deck => {
                    deck.modified = Sugar.Date(deck.modified + "Z").relative()
                });
                decks.splice(0, decks.length, ...new_decks);
            } catch (error) {
                console.error('getDecks error:', error)
            }
        },
        resetSearchTimeout() {
            // Resets the search timeout
            clearTimeout(this.searchTimeout);
            this.searchTimeout = setTimeout(() => {
                // When the timeout finishes, get decks with the current search string
                this.getDecks();
            }, this.searchTimeoutMs);
        }
    },
    setup(props, context) {
        return {
        }
    },
    mounted() {
        this.clearSearch();
        this.getDecks();
    },
    template: await loadHtml('./static/js/components/home-template.html')
}
