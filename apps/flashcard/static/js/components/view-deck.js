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
            cards: []
        };
    },
    methods: {
        async getCards() {
            try {
                //console.log(deckId)
                const currentUrl = window.location.href;

                // Extract information from the URL
                const urlParts = currentUrl.split('/');
                console.log(urlParts)
                const deckId = urlParts[urlParts.length - 1];
            const response = await axios.get('get_cards', { params: { deck_id: deckId } });
            const cards = response.data.cards;
            console.log(cards)
            this.cards = cards;
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
        
        }

        // flip(card){
        //     card.isFront = !card.isFront
        // }

    },
    mounted() {
        this.getCards(); // Load the cards for the deck

    },
    template: await loadHtml('./static/js/components/view-deck.html')
};
