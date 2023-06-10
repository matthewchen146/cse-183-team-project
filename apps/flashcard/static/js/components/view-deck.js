// view-deck.js
import cardItem from './card-item.js';


export default {
    components: {
        cardItem
    },
    props: {
    },
    data() {
        return {
            cards: [],
            deck: {},
            editUrl: "",
            addCardUrl:"",
            deleteDeckUrl:""
        };
    },
    methods: {
        async getCards() {
            try {
                //console.log(deckId)
                const currentUrl = window.location.href;

                // Extract information from the URL
                const urlParts = currentUrl.split('/');
                
                const deckId = urlParts[urlParts.length - 1];
                this.editUrl = urlFromRoot('edit/' + deckId)
                this.addCardUrl = urlFromRoot('add_card/' + deckId)
                this.deleteDeckUrl = urlFromRoot('delete/' + deckId)
                console.log(this.addCardUrl)
            const response = await axios.get('get_cards', { params: { deck_id: deckId } });
            const cards = response.data.cards;
            const response2 = await axios.get('get_deck', { params: { deck_id: deckId } });
            
            this.cards = cards;
            this.deck = response2.data.deck
            console.log(this.deck)
            } catch (error) {
            console.error('Error getting cards:', error);
            }
        },

        add(){
            console.log("adding");
        },
        toggleDropdown(){
            console.log("IM CALLED")
            const dropdownMenu = document.getElementById("dropdown-menu");
            if(dropdownMenu.style.display === "block"){
                dropdownMenu.style.display = "none";
            }else{
                dropdownMenu.style.display = "block";
            }
        
        },
        async toggleFavorite() {
            try {
                if (this.deck.is_favorited !== undefined) {
                    const result = await axios.post('set_favorite', {
                        is_favorite: !this.deck.is_favorited,
                        deck_id: this.deck.id
                    });

                    this.deck.is_favorited = result.data.is_favorite;
                }
            } catch (error) {
                console.error(`toggleFavorite error: `, error);
            }
        },

        // flip(card){
        //     card.isFront = !card.isFront
        // }

    },
    mounted() {
        this.getCards(); // Load the cards for the deck
        


    },
    template: await loadHtml('./static/js/components/view-deck.html')
};
