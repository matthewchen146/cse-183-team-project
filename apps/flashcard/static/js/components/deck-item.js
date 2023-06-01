export default await {
    props: {
        info: {
            type: Object,
            default: {}
        }
    },
    methods: {
        async toggleFavorite() {
            try {
                if (this.info.is_favorite !== undefined) {
                    const result = await axios.post(urlFromRoot('set_favorite'), {
                        is_favorite: !this.info.is_favorite,
                        deck_id: this.info.id
                    });

                    this.info.is_favorite = result.data.is_favorite;
                }
            } catch (error) {
                console.error(`toggleFavorite error: `, error);
            }
        }
    },
    data() {
        return {}
    },
    template: await loadHtml('./js/components/deck-item-template.html')
};