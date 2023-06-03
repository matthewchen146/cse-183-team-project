import DeckItem from './deck-item.js';

export default await {
    components: {
        DeckItem
    },
    data() {
        return {
            decksUrl: urlFromRoot('decks'),
            decks: [],
            search: ""
        }
    },
    methods: {
        async getDecks() {

            console.log("getting decks");

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
        }
    },
    setup(props, context) {
        return {
        }
    },
    mounted() {
        this.getDecks();
    },
    template: await loadHtml('./static/js/components/home-template.html')
}
