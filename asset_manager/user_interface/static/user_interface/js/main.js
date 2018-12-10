new Vue({
  el: '#app',
  data: {
    showSearch: false
  },
  methods: {
    toggleSearch: function(e) {
      e.preventDefault();
      this.showSearch = !this.showSearch;
    }
  }
});
