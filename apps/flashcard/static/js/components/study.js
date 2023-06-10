export default await {
    data() {
        return {
            deckId: serverData.deck_id,
            deck: null,
            cards: [],
            cardIndex: 0,
            isFlipped: false,
            exitUrl: urlFromRoot('deck/' + serverData.deck_id)
        }
    },
    methods: {
        async getCards(deckId) {
            try {
                const response = await axios.get('get_cards', { params: { deck_id: deckId } });
                const cards = response.data.cards;
                const response2 = await axios.get('get_deck', { params: { deck_id: deckId } });
                
                this.cards = cards;
                this.deck = response2.data.deck
                this.cardIndex = 0
                console.log(cards)
            } catch (error) {
                console.error('Error getting cards:', error);
            }
        },
        goToCard(index, resetFlip = true) {
            if (index >= this.cards.length || index < 0) {
                return;
            }
            this.cardIndex = index;
            if (resetFlip) {
                this.isFlipped = false
            }
        },
        nextCard() {
            this.goToCard(this.cardIndex + 1);
        },
        prevCard() {
            this.goToCard(this.cardIndex - 1);
        },
        flip() {
            this.isFlipped = !this.isFlipped;
        }
    },
    mounted() {
        this.getCards(this.deckId)
    },
    template: await loadHtml('./static/js/components/study-template.html')
}