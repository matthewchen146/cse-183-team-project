import test from './test.js';

export default await (async () => {
    return {
        components: {
            test
        },
        data() {
            return {}
        },
        template: '<div>Hello <test></test></div>'
    }
})() 