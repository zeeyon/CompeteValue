var scrap = {
    delimiters: ['[[', ']]'],
    template: '<a class="scrap" v-bind:class="{ scrapped: this.isScrapped }" href="#" onclick="return false" v-on:click="toggle_scrap()"></a>',
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
            var scrap = this
            var method = scrap.isScrapped ? 'delete' : 'post';
            axios({
                method: method,
                url: scrap.url
            })
            .then(function(response) {
                scrap.isScrapped = !scrap.isScrapped;
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
