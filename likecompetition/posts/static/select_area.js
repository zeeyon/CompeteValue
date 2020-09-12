Vue.component('select-area', {
	template: `<div><select name="sido" required id="id_sido" v-model="selected_sido">
		<option value>---------</option>
		<option v-for="sido in sidos" :value="sido.id">{{ sido.name }}</option>
	</select>
	<select name="area" required id="id_area" v-model="selected_sigungu">
		<option value>---------</option>
		<option v-for="sigungu in sigungus" :value="sigungu.id">{{ sigungu.name }}</option>
	</select></div>`,
	props: {
		'initial_selected_sido': {
			type: [String, Number],
			default: ''
		},
		'initial_selected_sigungu': {
			type: [String, Number],
			default: ''
		}
	},
	data: function() {
		return {
			sidos: {},
			sigungus: {},
			selected_sido: this.initial_selected_sido,
			selected_sigungu: this.initial_selected_sigungu
		}
	},
	methods: {
		update_sigungus: function() {
			this.sigungus = {};
			if (this.selected_sido === '') {
				return;
			}
			axios.get('/posts/sidos/' + this.selected_sido)
			.then(response => {
				this.sigungus = response.data.results;
			})
			.catch(error => {
				console.log(error);
			});
		}
	},
	watch: {
		selected_sido: function() {
			this.selected_sigungu = '';
			this.update_sigungus();
		}
	},
	created: function() {
		axios.get('/posts/sidos')
		.then(response => {
			this.sidos = response.data.results;
		})
		.catch(error => {
			console.log(error);
		});
		this.update_sigungus();
	}
});
