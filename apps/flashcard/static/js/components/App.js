export default await {
    components: {
    },
    data() {
        return {
            homeUrl: urlFromRoot(''),
            // from global in layout.html
            authUrls,
            authUser
        }
    },
    template: await loadHtml('./static/js/components/app-template.html')
}