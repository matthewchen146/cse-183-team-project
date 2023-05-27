import Test from './Test.js';

export default await (async () => {
    return {
        components: {
            Test
        },
        data() {
            return {}
        },
        template: '<div>Hello <test></test></div>'
    }
})() 