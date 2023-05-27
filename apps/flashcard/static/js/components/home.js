const self = {
    components: {
        
    },
    data() {
        return {
            decksUrl: urlFromRoot('decks')
        }
    },
    created: () => {
        
    },
    template: (await axios.get('./js/components/home-template.html')).data
}

export default await self;