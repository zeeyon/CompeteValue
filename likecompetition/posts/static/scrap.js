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
            var vue = this;
            var method = this.isScrapped ? 'delete' : 'post';
            axios({
                method: method,
                url: this.url
            })
            .then(function(response) {
                vue.isScrapped = !vue.isScrapped;
            })
            .catch(function(error) {
                console.log(error);
            });
        }
    }
};
