var scrap = {
    delimiters: ['[[', ']]'],
    template: '<a class="scrap" v-bind:class="{ scrapped: this.isScrapped }" href="#" v-on:click="toggle_scrap()"></a>',
    props: {
        url: String,
        initialScrapped: Boolean
    },
    data: function() {
        return {
            isScrapped: this.initialScrapped
        }
    },
    methods: {
        toggle_scrap: function() {
            var method = this.isScrapped ? 'delete' : 'post';
            this.isScrapped = !this.isScrapped;
            axios({
                method: method,
                url: this.url
            })
            .catch(function(error) {
                console.log(error);
            })
        }
    }
}

var posts = new Vue({
    delimiters: ['[[', ']]'],
    el: '#posts',
    components: {
        'scrap': scrap
    }
})
