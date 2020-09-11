Vue.component('select-area', {
	template: `<span><select v-model="selected_sido" name="sido" required id="id_sido">
		<option selected>---------</option>
		<option v-for="sido in sidos" :value="sido.id">{{ sido.name }}</option>
		</select>
		<select v-model="selected_area" name="area" required id="id_area">
		<option selected>---------</option>
		<option v-for="area in areas" :value="area.id">{{ area.name }}</option>
		</select></span>`,
	props: {
		initialSido: Number,
		initialArea: Number
	},
	data: function() {
		return {
			sidos: {},
			areas: {},
			selected_sido: this.initialSido,
			selected_area: this.initialArea
		}
	},
	methods: {
		update_areas: function() {
			axios.get('/posts/sidos/' + this.selected_sido)
			.then(response => {
				this.areas = response.data.results;
			})
			.catch(error => {
				console.log(error);
			});
		}
	},
	watch: {
		selected_sido: {
			handler: 'update_areas'
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
		this.update_areas();
	}
});
