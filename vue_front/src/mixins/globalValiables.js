export default {    // exportする
    created() {
        console.log('start! from mixins.') 
    },
 
    data() {
        return {
            serverPass: "https://localhost:10443/",   
        }
    },
 
    methods: {
        logging() {
            console.log('logging from mixins.')
        }
    },
 
    computed: {
        twoBytwo() {
            return 2 * 2
        }
    }
 }