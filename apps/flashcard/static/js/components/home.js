import DeckItem from './deck-item.js';

export default await {
    components: {
        DeckItem
    },
    data() {
        return {
            decksUrl: urlFromRoot('decks'),
            decks: []
        }
    },
    methods: {
        async getDecks() {

            console.log("getting decks")

            try {
                
                const result = await axios.get(urlFromRoot('get_decks'), { params: { search: '' } });

                const decks = this.decks;
                
                const new_decks = result.data.decks;

                new_decks.forEach(deck => {
                    deck.modified = Sugar.Date(deck.modified + "Z").relative()
                });

                decks.splice(0, decks.length, ...new_decks);

            } catch (error) {
                console.error('getDecks error', error)
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
    template: await loadHtml('./js/components/home-template.html')
}
