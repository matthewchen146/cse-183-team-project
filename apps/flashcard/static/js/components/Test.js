// export default await {
//   data() {
//     return {
//       count: 0
//     }
//   },
//   template: await loadHtml('./static/js/components/test-template.html')
// }

import DeckItem from './deck-item.js';

export default await {
    components: {
        DeckItem
    },
    data() {
        return {

            decks: [],
            search: "",
            searchTimeout: undefined,
            searchTimeoutMs: 1000
        }
    },
    methods: {
        async clearSearch() {
            // Clears the search bar.
            try {
                this.search = '';
                this.getLibrary();
            } catch (error) {
                console.error('clearSearch error:', error)
            }
        },
        async getLibrary() {
            // Clear the search timeout just in case it is still active (such as when pressing enter).
            clearTimeout(this.searchTimeout);
            try {
                // Make a GET request for decks depending on the search query and mode.
                const search = this.search;
                const mode = this.processMode();
                const result = await axios.get('get_library', { params: { search: search, mode: mode } });

                // Process results for display.
                const decks = this.decks;
                const new_decks = result.data.decks;
                new_decks.forEach(deck => {
                    deck.modified = Sugar.Date(deck.modified + "Z").relative()
                });
                decks.splice(0, decks.length, ...new_decks);
                console.log(decks)
            } catch (error) {
                console.error('getLibrary error:', error)
            }
        },
        processMode() {
            // Processes the current mode depending on what is checked.
            const mode_author = document.getElementById("mode-author").checked;
            const mode_tag = document.getElementById("mode-tag").checked;
            const mode_title = document.getElementById("mode-title").checked;
            

            // Create the mode string as necessary.
            var mode = "";
            if (mode_author) {
                mode += "author";
            }
            if (mode_tag) {
                mode += (mode.length ? "+tag" : "tag");
            }
            if (mode_title || !mode.length) {
                // Default to title search if no mode specified.
                mode += (mode.length ? "+title" : "title");
            }
            return mode;
        },
        resetSearchTimeout() {
            // Resets the search timeout.
            clearTimeout(this.searchTimeout);
            this.searchTimeout = setTimeout(() => {
                // When the timeout finishes, get decks with the current search string.
                this.getLibrary();
            }, this.searchTimeoutMs);
        }
    },
    setup(props, context) {
        return {
        }
    },
    mounted() {
        this.clearSearch();
        this.getLibrary();
        console.log(this.decks);
    },
    template: await loadHtml('./static/js/components/Test-template.html')
}
